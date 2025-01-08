<template>
    <div class="container">
      <!-- Panel filtrów -->
      <div class="filter-panel">
        <h3>Filter Books</h3>
  
        <!-- Themes Selector -->
        <div class="themes-selector">
          <button type="button" @click="toggleThemesDropdown" class="select-themes-btn">
            {{ newBook.themes.length > 0 ? newBook.themes.join(', ') : 'Select Themes' }}
          </button>
          <ul :class="{'dropdown-show': themesDropdownVisible}" class="dropdown">
            <li v-for="theme in availableThemes" :key="theme">
              <label>
                <input type="checkbox" :value="theme" v-model="newBook.themes" />
                {{ theme }}
              </label>
            </li>
          </ul>
        </div>
  
        <!-- Genre Selector -->
        <div class="genre-selector">
          <button type="button" @click="toggleDropdown" class="select-genre-btn">
            {{ newBook.genres.length > 0 ? newBook.genres.join(', ') : 'Select Genre' }}
          </button>
          <ul :class="{'dropdown-show': dropdownVisible}" class="dropdown">
            <li v-for="genre in availableGenres" :key="genre">
              <label>
                <input type="checkbox" :value="genre" v-model="newBook.genres" />
                {{ genre }}
              </label>
            </li>
          </ul>
        </div>
  
        <!-- Authors Display -->
        <div v-if="newBook.authors.length > 0">
          <h4>Authors</h4>
          <ul>
            <li v-for="(author, index) in newBook.authors" :key="index">
              {{ author.name }} {{ author.surname }}
              <button type="button" @click="removeAuthor(index)" class="remove-author-btn">Remove</button>
            </li>
          </ul>
        </div>
  
        <!-- Search for Authors -->
        <div class="authors-search">
          <input
            type="text"
            v-model="authorSearch"
            @input="searchAuthors"
            placeholder="Search for authors"
          />
          <ul v-if="authorsForSearching.length > 0" class="dropdown-authors">
            <li
              v-for="(author, index) in authorsForSearching"
              :key="index"
              @click="selectAuthor(author)"
            >
              {{ author.name }} {{ author.surname }}
            </li>
          </ul>
        </div>
  
        <!-- Author Selector -->
        <div class="author-selector">
          <button type="button" @click="toggleAuthorDropdown" class="select-author-btn">
            {{ newBook.authors.length > 0 ? newBook.authors.join(', ') : 'Select Author(s)' }}
          </button>
          <ul :class="{'dropdown-show': authorDropdownVisible}" class="dropdown">
            <li v-for="author in availableAuthors" :key="author">
              <label>
                <input type="checkbox" :value="author" v-model="newBook.authors" />
                {{ author }}
              </label>
            </li>
          </ul>
        </div>
  
        <!-- Button to apply filters -->
        <button @click="applyFilters" class="apply-filters-btn">Apply Filters</button>
      </div>
  
      <!-- Display filtered books -->
      <div class="books-list">
        <div v-for="book in books" :key="book.title" class="book-item">
          <h4>{{ book.title }}</h4>
          <p>{{ book.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
import Toast from './Toast.vue';
export default {
  data() {
return {
  newBook: {
    title: '',
    genres: [],
    themes: [],
    authors: [],
    name: '',
    surname: '',
    publicationYear: '',
    numberOfPages: '',
    publishingHouse: '',
    description: '',
    cover: null,
    file: null,
  },
  availableGenres: [
        'Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy',
        'Historical', 'Biography', 'Thriller', 'Adventure', 'Horror', 'Poetry', 'Self-Help', 'Philosophy', 'Art', 'Romance novel'
      ],
      availableThemes: [
        'Adventure', 'Love', 'Mystery', 'Historical', 'Science Fiction', 'Fantasy', 'Philosophy', 'Life', 'Technology', 'Politics', 'Nature'
      ],
  availableAuthors: [],
  authorSearch: '',
  authorsForSearching: [],
  books: [],
  dropdownVisible: false,
  themesDropdownVisible: false,
  authorDropdownVisible: false,
};
},
  components: {
  Toast,
},
  methods: {
    handleImageUpload(event) {
  this.selectedImage = event.target.files[0];
},
applyFilters() {
    const title = "Your Title Here";  // Możesz ustawić odpowiednią nazwę książki lub dynamicznie pobrać ją z formularza
    this.getBooksFilter(title);
  },
async getBooksFilter(title) {
  const toastRef = this.$refs.toastRef; // Reference for notifications

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    // Create the JSON object for the request body
    const requestBody = {
      authors : this.authors,
      themes: this.themes,
      genres: this.genres,
      group_props: this.group_props
    };

    // Execute the POST request with JSON body
    const response = await fetch(`${this.$link_backend}/filter/books?${params.toString()}`, {
      method: "GET",
      headers: {
       // "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
        "Content-Type": "application/json", // Set content type to JSON
      },
      body: JSON.stringify(requestBody), // Use JSON.stringify to send the body as JSON
    });

    // Handle response
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response:", JSON.stringify(errorData.detail, null, 2));
      toastRef.notificationClass = "error-toast";
      this.$refs.toastRef.showNotificationMessage();
      return;
    }

    const data = await response.json();

          // Store the fetched books
          this.books = data.map(book => ({
            title: book.title,
            publisher: book.publisher,
            year_of_pub: book.year_of_pub,
            description: book.description,
            url: book.url,
            url_img: book.url_img,
            num_of_pages: book.num_of_pages
          }));

    toastRef.message = "The book has been successfully added!";
    toastRef.notificationClass = "success-toast";
    this.$refs.toastRef.showNotificationMessage();
    console.log(result);
  } catch (error) {
    console.error("Error:", error);
    toastRef.message = `Error: ${error.message}`;
    toastRef.notificationClass = "error-toast";
    this.$refs.toastRef.showNotificationMessage();
  }
}
,
    toggleDropdown() {
  this.dropdownVisible = !this.dropdownVisible;
},
toggleThemesDropdown() {
  this.themesDropdownVisible = !this.themesDropdownVisible;
},
addAuthor() {
  if (this.newBook.name && this.newBook.surname) {
    this.newBook.authors.push({
      name: this.newBook.name,
      surname: this.newBook.surname,
    });
    this.newBook.name = '';
    this.newBook.surname = '';
  }
},
removeAuthor(index) {
  this.newBook.authors.splice(index, 1);
},

    async getSubstr(substr) {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("substr", substr);

  try {
    const response = await fetch(`${this.$link_backend}/author/substr?${params.toString()}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (response.ok) {
      const data = await response.json();
      this.authorsForSearching = data; // Lista autorów do wyświetlenia

      toastRef.message = `Successfully fetched authors.`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error fetching authors: ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error fetching authors:`, error);
    toastRef.message = `Network error. Could not fetch authors: ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage();
},

searchAuthors() {
  if (this.authorSearch.trim()) {
    this.getSubstr(this.authorSearch.trim());
  } else {
    this.authorsForSearching = [];
  }
},

selectAuthor(author) {
  // Dodaj autora do listy w książce
  this.newBook.authors.push(`${author.name} ${author.surname}`);
  // Wyczyść listę wyszukiwania i pole wyszukiwania
  this.authorsForSearching = [];
  this.authorSearch = "";
},

    
    async addAuthor() {
const toastRef = this.$refs.toastRef;
const token = localStorage.getItem("authToken");

// Check if the user is logged in
if (!token) {
  console.error("Token is missing or expired");
  toastRef.message = "You are not authenticated. Please log in.";
  toastRef.notificationClass = "error-toast";
  toastRef.showNotificationMessage();
  window.location.href = "/login";
  return;
}

// Validate if both name and surname are provided
if (!this.newBook.name.trim() || !this.newBook.surname.trim()) {
  toastRef.message = "Please provide both the author's name and surname.";
  toastRef.notificationClass = "error-toast";
  toastRef.showNotificationMessage();
  return;
}

try {
  // Build URL with query parameters
  const query = new URLSearchParams({
    name: this.newBook.name.trim(),
    surname: this.newBook.surname.trim()
  });

  // Log the query to check data before sending
  console.log("Sending Query:", query.toString());

  // Send GET request to backend with query parameters
  const response = await fetch(`${this.$link_backend}/authors?${query.toString()}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  // Check if the response is successful
  if (!response.ok) {
    const errorData = await response.json();
    console.error("Error details:", errorData); // Log error details
    toastRef.message = errorData.detail || "Error adding the author.";
    toastRef.notificationClass = "error-toast";
    toastRef.showNotificationMessage();
    return;
  }

  // Display success message
  toastRef.message = "Author added successfully!";
  toastRef.notificationClass = "success-toast";
  toastRef.showNotificationMessage();

  // Optionally, clear the form or reset fields after author is added
  this.newBook.name = "";
  this.newBook.surname = "";

} catch (error) {
  console.error("Error:", error);
  toastRef.message = `Error: ${error.message}`;
  toastRef.notificationClass = "error-toast";
  toastRef.showNotificationMessage();
}
},


  addBook() {
    if (this.newBook.title && this.newBook.authors.length > 0 && this.newBook.description && this.newBook.genres.length > 0) {
      this.books.push({ ...this.newBook });
      this.resetNewBook(); // Reset the form after adding the book
    }
  },
  removeBook(index) {
    this.books.splice(index, 1);
    this.resetNewBook(); // Reset the form after removing a book
  },
  toggleDropdown() {
    this.dropdownVisible = !this.dropdownVisible;
  },
  toggleAuthorDropdown() {
    this.authorDropdownVisible = !this.authorDropdownVisible;
  },
  toggleThemesDropdown() {
    this.themesDropdownVisible = !this.themesDropdownVisible;
  },
  resetNewBook() {
    this.newBook = {
      title: '',
      authors: [],
      displayCover: [],
      description: '',
      genres: [],
      themes: [],
      cover: null,
      publicationYear: '',
      numberOfPages: '',
      publishingHouse: '',
      file: null, // Reset file as well
    };
  },
  onCoverFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      // Create URL for the selected file
      this.newBook.cover = file;
      this.displayCover = URL.createObjectURL(file);

    }
  },
  removeBookCover() {
    this.newBook.cover = null; // Removes the selected cover
  },
  onBookFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      this.newBook.file = file; // Handle book file selection
    }
  },
  removeBookFile() {
    this.newBook.file = null; // Removes the selected book file
  }
,
async fetchWithRedirect(url, options = {}) {
let response = await fetch(url, options);

// Проверяем, есть ли код 307 (или другой код редиректа, если нужно)
if (response.status === 307) {
  const location = response.headers.get('Location');
  if (location) {
    // Выполняем повторный запрос по новому URL
    console.log(`Redirecting to: ${location}`);
    response = await fetch(location, options);
  } else {
    throw new Error('Redirect without Location header');
  }
}

return response;
},
  handleImageUpload(event) {
this.selectedImage = event.target.files[0];
},

handleFileUpload(event) {
this.selectedFile = event.target.files[0];
},
async addBooks() {
const toastRef = this.$refs.toastRef; // Reference for notifications

// Check if files are selected
if (!this.newBook.file || !this.newBook.cover) {
  toastRef.message = "File(s) are missing.";
  toastRef.notificationClass = "error-toast";
  this.$refs.toastRef.showNotificationMessage();
  return;
}

try {
  // Define query parameters
  const params = {
    title: this.newBook.title,
    year_of_pub: this.newBook.publicationYear,
    num_of_pages: this.newBook.numberOfPages,
    description: this.newBook.description,
    publisher: this.newBook.publishingHouse,
  };

  // Construct the query string
  const queryPar = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    queryPar.append(key, String(value)); // Convert all values to strings
  }

  // Create FormData object for files and additional JSON body data
  const formData = new FormData();

  // Convert authors array to JSON string
  const authorsJSON = JSON.stringify(
    this.newBook.authors.map(author => ({
      name: author.name,
      surname: author.surname,
    }))
  );
  formData.append("authors", authorsJSON);

  // Convert themes and genres to JSON strings (if needed)
  formData.append("themes", JSON.stringify(this.newBook.themes));
  formData.append("genres", JSON.stringify(this.newBook.genres));

  // Add files
  formData.append("file_img_book", this.newBook.cover); // Add image file
  formData.append("file_book", this.newBook.file); // Add EPUB file

  // Execute the POST request
  const response = await fetch(`${this.$link_backend}/books/?${queryPar.toString()}`, {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("authToken"),
      "ngrok-skip-browser-warning": "anyValue",
    },
    body: formData, // Use FormData as the request body
  });

  // Handle response
  if (!response.ok) {
    const errorData = await response.json();
    toastRef.message = errorData.detail || "Error adding the book.";
    toastRef.notificationClass = "error-toast";
    this.$refs.toastRef.showNotificationMessage();
    return;
  }

  const result = await response.json();
  toastRef.message = "The book has been successfully added!";
  toastRef.notificationClass = "success-toast";
  this.$refs.toastRef.showNotificationMessage();
  console.log(result);
} catch (error) {
  console.error("Error:", error);
  toastRef.message = `Error: ${error.message}`;
  toastRef.notificationClass = "error-toast";
  this.$refs.toastRef.showNotificationMessage();
}
}

,

  
}

};
</script>
<style scoped>
.container {
  display: flex;
  gap: 30px; /* Distance between filter panel and books */
}

.filter-panel {
  width: 250px;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 15px;
  font-size: 1.2em;
  font-weight: bold;
}

.filter-panel .dropdown {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: none;
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 5px;
  max-height: 200px;
  overflow-y: auto;
}

.filter-panel .dropdown-show {
  display: block;
}

.filter-panel button {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: left;
  font-size: 1em;
}

.filter-panel button:hover {
  background-color: #e6e6e6;
}

.apply-filters-btn {
  background-color: #ff0000; /* Czerwony kolor tła */
  color: rgb(0, 0, 0); /* Biały kolor tekstu */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.apply-filters-btn:hover {
  background-color: #e60000; /* Ciemniejszy czerwony przy najechaniu */
}

.authors-search input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.authors-search ul {
  list-style-type: none;
  padding: 0;
}

.authors-search li {
  padding: 5px;
  cursor: pointer;
}

.authors-search li:hover {
  background-color: #f0f0f0;
}

.books-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  flex: 1;
}

.book-item {
  width: 200px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-item h4 {
  font-size: 1.1em;
  margin: 0;
}

.book-item p {
  font-size: 0.9em;
  color: #555;
}

.remove-author-btn {
  background-color: #e74c3c;
  color: rgb(255, 0, 0);
  padding: 3px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.remove-author-btn:hover {
  background-color: #c0392b;
}

</style>