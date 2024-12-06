<template>
  
    <div id="app">
      <!-- Add Book Section -->
      <section id="add-book" class="background-section">
        
        <br>
        <form @submit.prevent="addBook">
          
  
          
          
            <div class="authors-section">
  <h3>Author</h3>
  <input type="text" v-model="newBook.name" placeholder="Author's First Name" required />
  <input type="text" v-model="newBook.surname" placeholder="Author's Last Name" required />
  <button type="button" @click="addAuthor" class="add-author-btn">Add Author</button>
</div>

        

       
  
          
          
          

         
        </form>
      </section>
  
      <!-- My Books Section -->
      
      <Toast ref="toastRef" />

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
    availableGenres: ['Fantasy', 'Sci-Fi', 'Mystery'],
    availableThemes: ['Adventure', 'Drama', 'Horror'],
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
      surname: this.newBook.surname.trim(),
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

    // Clear the form or reset fields after author is added
    this.newBook.name = "";
    this.newBook.surname = "";

    // Opóźnione przekierowanie
    setTimeout(() => {
      this.$router.push({ name: 'Add' }); // Przekierowanie na Add.vue po 2 sekundach
    }, 2000); // 2000 ms = 2 sekundy

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

  // Ensure genres are selected
  if (this.newBook.genres.length === 0) {
    toastRef.message = "Please select at least one genre.";
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
    formData.append("authors", JSON.stringify(this.newBook.authors)); // Serialize authors array
    formData.append("themes", JSON.stringify(this.newBook.themes));   // Serialize themes array
    formData.append("genres", JSON.stringify(this.newBook.genres));   // Serialize genres array
    formData.append("file_img_book", this.newBook.cover); // Add image file
    formData.append("file_book", this.newBook.file); // Add EPUB file

    console.log("data received:", formData); // Debugging line
    for (let [key, value] of formData.entries()) {
    console.log(key, value);
}
const iterator = formData.entries();
console.log([...iterator]);

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
  .dropdown-show {
  display: block;
}
.dropdown {
  display: none;
}

  .dropdown-authors {
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  background-color: #fff;
  z-index: 1000;
}

.dropdown-authors li {
  padding: 10px;
  cursor: pointer;
}

.dropdown-authors li:hover {
  background-color: #f0f0f0;
}

  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@300&display=swap');
  
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%; /* Ustaw wysokość na 100% dla całej strony */
    overflow-x: hidden; /* Zapobiega przewijaniu poziomemu */
}

.background-section {
    background-image: url('src/components/pictures/books1.jpeg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    width: 100%;
    height: 100vh; /* Ustaw wysokość na 100% widoku */
    position: relative; /* Dodaj pozycjonowanie dla overlay */
    z-index: 0;
}

/* Overlay for background */
.background-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(231, 225, 225, 0.203); /* Semi-transparent overlay */
    z-index: 1; /* Overlay nad tłem, ale pod zawartością */
}

/* Ensure content is above overlay */
.background-section > * {
    position: relative;
    z-index: 2;
}

  
  
  /* Set a stylish background and center everything */
  body {
    background-image: url('src/components/pictures/books1.jpeg');
    background-size: cover;
    background-position: center;
    color: #333;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    flex-direction: column;
    padding: 20px;
    background-attachment: fixed;
  }
  
  /* Heading Styling */
  h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #4a3c3a;
    margin-bottom: 1.5rem;
    font-weight: 700;
    text-align: center;
  }
  
  /* Form Styling */
  form {
    background: #ffffff;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    max-width: 600px;
    width: 100%;
    margin: 0 auto;
  }
  
  /* Form Input and Button Styling */
  form input,
  form textarea,
  form select,
  form button {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    transition: all 0.3s ease-in-out;
  }
  
  /* Focus Effects for Inputs */
  form input:focus,
  form textarea:focus,
  form select:focus {
    border-color: #b97c6b;
    outline: none;
  }
  
  /* Submit Button Styling */
  form button.submit-btn {
    background: linear-gradient(135deg, #4a3c3a, #6f4f4a);
    color: #fff;
    border: none;
    padding: 0.8rem 1.8rem;
    font-size: 1.1rem;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.3s ease;
  }
  
  form button.submit-btn:hover {
    background: linear-gradient(135deg, #6f4f4a, #4a3c3a);
  }
  
  
  
  /* Book Image Styling */
  .book-image {
    max-width: 150px;
    max-height: 220px;
    object-fit: cover;
    margin-top: 1rem;
    border-radius: 10px;
  }
  
  
  /* Genre and Author Selector Styles */
  
  .genre-selector, .author-selector, .themes-selector {
    position: relative;
    width: 100%;
  }
  
  .select-genre-btn,
  .select-author-btn,
  .themes-selector-btn {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    cursor: pointer;
    text-align: left;
    transition: all 0.3s ease;
  }
  
  .select-genre-btn:hover,
  .select-author-btn:hover,
  .themes-selector:hover {
    background-color: #f0f0f0;
  }
  
  /* Dropdown Visibility and Transition */
  .dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    max-height: 200px;
    overflow-y: auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
  }
  
  .dropdown-show {
    opacity: 1;
    visibility: visible;
    transform: translateY(10px);
  }
  
  .dropdown li {
    list-style: none;
  }
  
  .dropdown li label {
    font-size: 1rem;
    cursor: pointer;
  }
  
  .dropdown li input {
    margin-right: 0.6rem;
  }
  
  /* Custom Checkbox Styles */
  input[type="checkbox"] {
    position: relative;
    width: 18px;
    height: 18px;
    border: 2px solid #ddd;
    border-radius: 3px;
    appearance: none;
    background-color: #fafafa;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  input[type="checkbox"]:checked {
    background-color: #4a3c3a;
    border-color: #4a3c3a;
  }
  
  input[type="checkbox"]:checked::before {
    content: '✔';
    position: absolute;
    top: 1px;
    left: 4px;
    font-size: 12px;
    color: white;
  }
  
  /* Smooth Transition for Dropdown */
  .dropdown-show {
    opacity: 1;
    visibility: visible;
    transform: translateY(10px);
  }
  
  /* Form Textarea Styling */
  form textarea {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    transition: all 0.3s ease-in-out;
    resize: vertical;
    min-height: 100px;
  }
  
  /* Focus Effects for Textarea */
  form textarea:focus {
    border-color: #b97c6b;
    outline: none;
  }
  
  /* Responsive Media Queries */
  @media (max-width: 1200px) {
    body {
      font-size: 16px;
    }
  }
  
  @media (max-width: 768px) {
    h2 {
      font-size: 1.5rem;
    }
  
    .background-section {
      background-position: top center;
    }
  
    .my-books {
      grid-template-columns: 1fr;
    }
  }
  
  #add-book {
    padding: 20px;
    background-color: #f5f5f5;
  }
  
  #add-book h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  input[type="text"], textarea, .select-genre-btn, .select-author-btn {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  textarea {
    height: 100px;
  }
  
  select-genre-btn, select-author-btn {
    text-align: left;
  }
  
  input[type="file"] {
    margin-top: 20px;
  }
  
  .upload-btn {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    display: inline-block;
    text-align: center;
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .upload-btn:hover {
    background-color: #45a049;
  }
  
  input[type="file"] {
    display: none;
  }
  
  .book-cover-preview-container {
    margin-top: 10px;
    text-align: center;
  }
  
  .book-cover-preview {
    width: 150px;
    height: auto;
    margin-top: 10px;
    border: 1px solid #ddd;
    padding: 5px;
    background-color: #f4f4f4;
    display: block; /* ensures the image is block level so it can be centered */
    margin-left: auto; /* auto margin to center it */
    margin-right: auto; /* auto margin to center it */
  }
  
  .remove-cover-btn {
    background-color: #FF6347;
    color: white;
    padding: 5px 10px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    margin-top: 10px;
  }
  
  .remove-cover-btn:hover {
    background-color: #FF4500;
  }
  
  .file-upload {
    margin-bottom: 1px;
  }
  
  /* Themes Selector Styles */
  .themes-selector {
    position: relative;
    width: 100%;
  }
  
  .select-themes-btn {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    cursor: pointer;
    text-align: left;
    transition: all 0.3s ease;
  }
  
  .select-themes-btn:hover {
    background-color: #f0f0f0;
  }
  
  /* Ensure the dropdown aligns with the other selectors */
  .dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    max-height: 200px;
    overflow-y: auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
  }
  
  .dropdown-show {
    opacity: 1;
    visibility: visible;
    transform: translateY(10px);
  }
  
  .dropdown li {
    list-style: none;
  }
  
  .dropdown li label {
    font-size: 1rem;
    cursor: pointer;
  }
  
  .dropdown li input {
    margin-right: 0.6rem;
  }
  
  /* Custom Checkbox Styles */
  input[type="checkbox"] {
    position: relative;
    width: 18px;
    height: 18px;
    border: 2px solid #ddd;
    border-radius: 3px;
    appearance: none;
    background-color: #fafafa;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  input[type="checkbox"]:checked {
    background-color: #4a3c3a;
    border-color: #4a3c3a;
  }
  
  input[type="checkbox"]:checked::before {
    content: '✔';
    position: absolute;
    top: 1px;
    left: 4px;
    font-size: 12px;
    color: white;
  }
  
  
  /* Style for the remove button (Delete File / Delete Cover) */
  .remove-file-btn, .remove-cover-btn {
    background-color: #e74c3c;  /* Red background */
    color: white;  /* White text */
    border: none;  /* No border */
    padding: 8px 16px;  /* Padding around the text */
    font-size: 14px;  /* Font size */
    cursor: pointer;  /* Pointer cursor */
    border-radius: 4px;  /* Rounded corners */
    transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
  }
  
  .remove-file-btn:hover, .remove-cover-btn:hover {
    background-color: #c0392b;  /* Darker red on hover */
  }
  
  .remove-file-btn:focus, .remove-cover-btn:focus {
    outline: none;  /* Remove the outline on focus */
  }
  </style>
  