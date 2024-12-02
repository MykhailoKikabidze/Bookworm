<template>
    <div id="app">
      <!-- Add Book Section -->
      <section id="add-book" class="background-section">
        <h1>Add a Book</h1>
        <br>
        <form @submit.prevent="addBook">
          <input type="text" v-model="newBook.title" placeholder="Book Title" required />
  
          <!-- Custom Genre Selector -->
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
  
          <!-- Custom Author Selector -->
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
  
          <!-- New Fields -->
  
          <!-- Year of Publication -->
          <input type="number" v-model="newBook.publicationYear" placeholder="Year of Publication" min="1500" max="2099" />
  
          <!-- Number of Pages -->
          <input type="number" v-model="newBook.numberOfPages" placeholder="Number of Pages" min="1" />
  
          <!-- Publishing House -->
          <input type="text" v-model="newBook.publishingHouse" placeholder="Publishing House" />
  
          <!-- Book Description Field -->
          <textarea v-model="newBook.description" placeholder="Book Description" required></textarea>
  
          <!-- Add Book Cover Section -->
          <div class="file-upload">
            <label v-if="!newBook.cover" for="cover-upload" class="upload-btn">
              Add Book Cover
            </label>
            <input v-if="!newBook.cover" type="file" id="cover-upload" @change="onCoverFileChange" accept="image/*" />
  
            <!-- Display Book Cover Image and Remove Button -->
            <div v-if="newBook.cover">
              <img :src="displayCover" alt="Book Cover" class="book-cover-preview" />
              <button type="button" @click="removeBookCover" class="remove-cover-btn">Remove Cover</button>
            </div>
          </div>
          
          <!-- Book File (PDF/EPUB) -->
  <div class="file-upload">
    <label v-if="!newBook.file" for="file-upload" class="upload-btn">
      Add Book File (PDF/EPUB)
    </label>
    <input v-if="!newBook.file" type="file" id="file-upload" @change="onBookFileChange" accept=".pdf, .epub" />
  
    <!-- Display Book File and Remove Button -->
    <div v-if="newBook.file">
      <p>File: {{ newBook.file.name }}</p>
      <button type="button" @click="removeBookFile" class="remove-file-btn">Delete File</button>
    </div>
  </div>

          <button @click="addBooks()" type="submit" class="submit-btn">Add Book</button>
        </form>
      </section>
  
      <!-- My Books Section -->
      <section id="my-books">
        <ul>
          <li v-for="(book, index) in books" :key="index">
            <div>
              <strong>{{ book.title }}</strong> by {{ book.authors.join(', ') }} <br />
              <em>Genres:</em> {{ book.genres.join(', ') }} <br />
              <em>Themes:</em> {{ book.themes.join(', ') }} <br />
              <p>{{ book.description }}</p>
              <div v-if="book.cover">
                <img :src="displayCover" alt="Book Cover" class="book-cover-preview" />
                <button @click="removeBookCover(book)" class="remove-btn">Remove Cover</button>
              </div>
              <p><strong>Year of Publication:</strong> {{ book.publicationYear }}</p>
              <p><strong>Number of Pages:</strong> {{ book.numberOfPages }}</p>
              <p><strong>Publishing House:</strong> {{ book.publishingHouse }}</p>
            </div>
            <button @click="removeBook(index)" class="remove-btn">Remove</button>
          </li>
        </ul>
      </section>
      <Toast ref="toastRef" />

    </div>
  </template>
  
  <script>
  import Toast from './Toast.vue';
  export default {
    data() {
      return {
        books: [],
        newBook: {
          title: '',
          authors: [],
          description: '',
          genres: [],
          themes: [],
          cover: null,
          displayCover: [],
          publicationYear: '',
          numberOfPages: '',
          publishingHouse: '',
          file: null,
        },
        availableGenres: [
          'Fiction', 'Non-Fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy',
          'Historical', 'Biography', 'Thriller', 'Adventure', 'Horror', 'Poetry', 'Self-Help', 'Philosophy', 'Art', 'Romance novel'
        ],
        availableAuthors: [
          'William Shakespeare', 'Agatha Christie', 'Danielle Steel', 'J. K. Rowling', 'Tom Clancy', 'Stephen King', 'Masashi Kishimoto', 'J. R. R. Tolkien', 'C. S. Lewis', 'Anne Rice', 'Charles Dickens', 'Mark Twain', 'Fyodor Dostoevsky', 'Haruki Murakami',  
        ],
        availableThemes: [
          'Adventure', 'Love', 'Mystery', 'Historical', 'Science Fiction', 'Fantasy', 'Philosophy', 'Life', 'Technology', 'Politics', 'Nature'
        ],
        dropdownVisible: false,
        authorDropdownVisible: false,
        themesDropdownVisible: false,
      };
    },
    components: {
    Toast,
  },
    methods: {
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
    formData.append("authors", this.newBook.authors);
    formData.append("themes", this.newBook.themes);
    formData.append("genres", this.newBook.genres);
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
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@300&display=swap');
  
  html, body {
    height: 100%;
    margin: 7;
    font-family: 'Roboto', sans-serif;
  }
  
  /* Adjust the background section */
  #add-book h1 {
    color: white; /* Biały kolor tekstu */
    font-size: 2.5rem; /* Zwiększony rozmiar czcionki */
    font-weight: bold; /* Opcjonalnie, aby nagłówek był pogrubiony */
    text-align: center; /* Opcjonalnie, aby wyśrodkować tekst */
  }
  
  
  #add-book {
    position: relative;
    width: 100%; /* Ensure it takes full width of its parent container */
    height: auto; /* Adjust based on content size */
  }
  
  .background-section {
    background-image: url('src/components/pictures/books1.jpeg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    width: 100%;
    height: 100%; /* Ensures it fills the parent container */
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
    z-index: 0;
  }
  
  .background-section > * {
    position: relative;
    z-index: 2; /* Ensure content is above overlay */
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
  