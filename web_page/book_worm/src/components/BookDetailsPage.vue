<template>
  <div id="app">
    <div class="library-container">
      <div class="book-details-container">
        <div v-if="book">
          <h1 class="book-title">{{ book.title }}</h1>
          <p><strong>Description:</strong> {{ book.description || "No description available." }}</p>
          <p><strong>Year of Publication:</strong> {{ book.year_of_pub || "Unknown" }}</p>
          <p><strong>Publisher:</strong> {{ book.publisher || "Unknown" }}</p>
          
          <h3>Authors</h3>
    <ul v-if="authors.length">
      <li v-for="(author, index) in authors" :key="index">
        {{ author.name }} {{ author.surname }}
      </li>
    </ul>
    <p v-else>No authors available.</p>

    <!-- Display genres -->
    <h3>Genres</h3>
    <ul v-if="genres.length">
      <li v-for="(genre, index) in genres" :key="index">{{ genre }}</li>
    </ul>
    <p v-else>No genres available.</p>

    <!-- Display themes -->
    <h3>Themes</h3>
    <ul v-if="book.themes && book.themes.length">
      <li v-for="(theme, index) in book.themes" :key="index">{{ theme }}</li>
    </ul>
    <p v-else>No themes available.</p>
          
          <div class="image-list" v-if="displayImages">
            <div v-for="(imageUrl, index) in downloadedImageUrls" :key="index" class="image-item">
              <img :src="imageUrl" alt="Book Cover" class="book-cover-image" />
            </div>
          </div>
        </div>
        <div v-else>
          <p>Loading book details...</p>
        </div>
      </div>
    </div>

    <header class="header">
      <h1>Book Reader</h1>
      <button @click="downloadBookFile(this.book.title)">Download EPUB</button>
    </header>

    <!-- Main Content -->
    <div class="main-container">
      <!-- Fixed Frame Reader -->
      <div class="reader-frame">
        <div class="viewer" ref="viewer"></div>
      </div>

      <!-- Toolbar -->
      <div class="footer-toolbar">
        <button @click="goPrevious" :disabled="currentPage <= 0">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <div></div>
       
        <button @click="goNext" :disabled="currentPage >= totalPages">Next</button>
        <button @click="handleHighlightAndPost" :disabled="!book">Add Highlight</button>
        <input type="color" v-model="selectedColor" title="Choose Highlight Color" />
      </div>

      <!-- Bookmarks Section -->
      <div class="bookmarks" v-if="bookmarks.length">
        <h3>Bookmarks</h3>
        <ul>
          <li
            v-for="(bookmark, index) in bookmarks"
            :key="index"
            @click="goToBookmark(bookmark.cfi)"
            class="bookmark-item"
          >
            <span>Page {{ bookmark.page }}: </span>
            <span
              class="highlighted-text"
              :style="{ backgroundColor: bookmark.color }"
            >
              {{ bookmark.text }}
            </span>
          </li>
        </ul>
      </div>

      <!-- Notes Section -->
      <button @click="getNotes(this.book.title)" class="get-notes-button">Show all my Notes</button>
      <div v-if="hz.length > 0">
        <h3>Notes for {{ this.book.title || 'Unknown Book' }}:</h3>
        <ul class="notes-list">
          <li v-for="note in hz" :key="note.id" class="note-item">
            <strong>Page {{ note.page }}:</strong> {{ note.description }}
            <button @click="deleteNotes(this.book.title, note.page, note.description)" class="delete-note-button">Delete Note</button>
          </li>
        </ul>
      </div>
    
    </div>
    <Toast ref="toastRef" />
  </div>
</template>



<script>
import ePub from "epubjs"; // Importing the epub.js library
import Toast from './Toast.vue';
export default {
  data() {
    return {
      book: null, // EPUB.js book instance
      rendition: null, // EPUB.js rendition instance
      currentPage: 1, // Current page number
      totalPages: 0, // Total pages
      bookmarks: [], // List of bookmarks {page, text, cfi, color}
      selectedColor: "#ffd966", // Default highlight color
      isLoading: false,
      errorMessage: "",
      authors: [],
      genres: [],
      themes: [],  // Stores the book themes
      downloadedImageUrls: [],  // Stores the URLs of downloaded images
      displayImages: false,
      message: "",            // Message for feedback
      firstWord: "",          // To store the first word of the first chapter
      spineItems: [],         // Store the spine items for navigation
      bookUrl: null,   
      hz: [], // Store the notes fetched from backend
      currentDescription: "",
    };
  },
  components: {
    Toast,

  },
  mounted() {
  // Pobranie tytułu z parametrów ścieżki, jeśli nie jest ustawiony
  this.book = this.book || { title: this.$route.params.title || "Unknown Title" };
  console.log("Loaded book title from route:", this.book.title);
},
  
  methods: {
    
    
    async deleteNotes(title, page, description,quote,character) {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("title", title);
  params.append("page", page);
  params.append("description", description);
  params.append("quote", quote);
  params.append("character", character);


  try {
    const response = await fetch(`${this.$link_backend}/notes?${params.toString()}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (response.ok) {
      // Usunięcie notatki z listy
      this.hz = this.hz.filter(note => note.id !== note.id);

      toastRef.message = `Note successfully deleted.`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error deleting note: ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error deleting note:`, error);
    toastRef.message = `Network error. Could not delete note. ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage();
},
    viewBookDetails(book) {
    this.$router.push({
      name: 'BookDetails',
      params: { title: book.title },
      query: { imageUrl: this.downloadedImageUrls[this.books.indexOf(book)] } // Pass the image URL as a query
    });
  },
    highlightSelection() {
    if (!this.book || !this.rendition) {
      alert("Book or rendition not ready.");
      return;
    }

    const iframe = this.$refs.viewer.querySelector("iframe");
    const iframeWindow = iframe.contentWindow;
    const selection = iframeWindow.getSelection();
    const selectedText = selection.toString().trim();

    if (selectedText) {
      const cfi = this.rendition.currentLocation().start.cfi;
      const color = this.selectedColor || "#FFD700";

      this.bookmarks.push({
        page: this.currentPage,
        text: selectedText,
        cfi,
        color,
      });

      this.rendition.annotations.add("highlight", cfi, {
        fill: color,
        fillOpacity: 0.5,
      });

      // Update currentDescription for note-saving
      this.currentDescription = selectedText;

      alert(`Highlighted: "${selectedText}" on Page ${this.currentPage}`);
    } else {
      alert("Please select text to highlight.");
    }
  },

  handleHighlightAndPost() {
    this.highlightSelection(); // Dodanie podświetlenia
    const bookTitle = this.book?.title || this.$route.params.title;
    if (this.currentDescription && bookTitle) {
      this.postNotes(bookTitle, this.currentPage, this.currentDescription);
    } else {
      alert("No text highlighted or book title missing.");
    }
  },

  async postNotes(title, page, description,quote,character) {
    const toastRef = this.$refs.toastRef;
    const params = new URLSearchParams();
    params.append("title", title);
    params.append("page", page);
    params.append("description", description);
    params.append("quote", quote);
    params.append("character", character);

    try {
      const response = await fetch(`${this.$link_backend}/notes?${params.toString()}`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
        },
      });

      if (response.ok) {
        toastRef.message = `Successfully added highlight for "${title}".`;
        toastRef.notificationClass = "success-toast";
      } else {
        const errorData = await response.json();
        toastRef.message = `Error adding highlight: ${errorData.detail || "Unknown error"}`;
        toastRef.notificationClass = "error-toast";
      }
    } catch (error) {
      console.error(`Error adding highlight:`, error);
      toastRef.message = `Network error. Could not add highlight for "${title}". ${error.message}`;
      toastRef.notificationClass = "error-toast";
    }

    this.$refs.toastRef.showNotificationMessage();
  },

  
  async getNotes(title) {
  const params = new URLSearchParams();
  params.append("title", title);

  try {
    const response = await fetch(`${this.$link_backend}/notes?${params.toString()}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Fetched notes:", data);
      this.hz = Array.isArray(data) ? data : []; // Przypisanie notatek, jeśli istnieją
    } else {
      console.error(`Error fetching notes for "${title}": ${response.statusText}`);
    }
  } catch (error) {
    console.error(`Error fetching notes for "${title}":`, error);
  }
},
    async loadEpub(blob) {
    try {
      const reader = new FileReader();
      reader.onload = (e) => {
        const arrayBuffer = e.target.result;
        this.book = ePub(arrayBuffer);

        // Render book into fixed frame
        const viewer = this.$refs.viewer;
        this.rendition = this.book.renderTo(viewer, {
          width: "100%",
          height: "100%",
        });

        // Ensure the rendition is properly displayed before setting total pages
        this.rendition.display().then(() => {
          this.book.ready.then(() => {
            this.book.locations.generate(1000).then(() => {
              this.totalPages = this.book.locations.length();
              console.log(`Total Pages: ${this.totalPages}`);
            }).catch((error) => {
              console.error("Error generating locations:", error);
            });
          }).catch((error) => {
            console.error("Error initializing book:", error);
          });
        }).catch((error) => {
          console.error("Error displaying rendition:", error);
        });

        this.rendition.on("relocated", (location) => {
          this.currentPage = this.book.locations.locationFromCfi(location.start.cfi);
        });
      };
      reader.readAsArrayBuffer(blob);
    } catch (error) {
      console.error("Error loading EPUB:", error);
    }
  },

    goPrevious() {
      if (this.rendition) this.rendition.prev();
    },
    goNext() {
      console.log("Blat");
      if (this.rendition) this.rendition.next();
    },

    

    goToBookmark(cfi) {
      // Navigate to the CFI location in the book
      this.rendition.display(cfi);

      // Optionally, you can also highlight the text again when you navigate to it
      this.rendition.annotations.add("highlight", cfi, {
        fill: "#FFD700",        // Default highlight color (can be dynamic)
        "fill-opacity": 0.5     // Set the opacity of the highlight color
      });
    },
    // Function to download the EPUB file
    async downloadBookFile(title) {
      try {
        this.errorMessage = ""; // Reset error message
        this.message = "Fetching EPUB file for download..."; // Initial message

        const response = await fetch(
          `${this.$link_backend}/books/file?title=${title}`,
          {
            method: "GET",
            headers: {
              "ngrok-skip-browser-warning": "anyValue", // Example custom header
            },
          }
        );

        if (response.ok) {
          const blob = await response.blob();
          this.bookUrl = URL.createObjectURL(blob); // Store the URL for the EPUB file

          // Trigger the download
          const link = document.createElement("a");
          link.href = this.bookUrl;
          link.download = `${title}.epub`;
          link.click();

          this.message = "EPUB file downloaded successfully.";

          // Load and display the downloaded EPUB file immediately after downloading
          this.loadEpub(blob);
        } else {
          const errorData = await response.json();
          this.errorMessage =
            errorData.detail || "Failed to download the EPUB file.";
        }
      } catch (error) {
        this.errorMessage = `An error occurred while downloading: ${error.message}`;
      }
    },

    // Extract the first word from the first chapter
    async extractFirstWord() {
      try {
        const spine = await this.book.loaded.spine;
        const firstItem = spine.items[0];
        const firstText = await firstItem.load(this.book.load.bind(this.book));
        const content = new DOMParser().parseFromString(firstText, "text/html");
        this.firstWord = content.body.textContent.split(/\s+/)[0];
      } catch (error) {
        this.errorMessage = `An error occurred while extracting the first word: ${error.message}`;
      }
    },
    
    async getBookInfo(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/info?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.book = {
            title: data.title,
            description: data.description || "No description available.",
            year_of_pub: data.year_of_pub || "Unknown",
            publisher: data.publisher || "Unknown",
            authors: data.authors || [],
            genres: data.genres || [],
            cover: data.cover_url || 'placeholder-image.jpg',
          };

          toastRef.message = `Successfully fetched details for "${title}"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching details for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error fetching details for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch details for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },

    async getThemes(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/themes?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.book.themes = Array.isArray(data) ? data : [];

          toastRef.message = `Successfully fetched themes for "${title}"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching themes for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error fetching themes for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch themes for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },

    async downloadImages() {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", this.book.title); // Use the current book's title to fetch images

      try {
        const response = await fetch(`${this.$link_backend}/books/images?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.downloadedImageUrls = data.images.map(img => img.url);
          this.displayImages = true;
          toastRef.message = `Successfully downloaded images for "${this.book.title}"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error downloading images for "${this.book.title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error downloading images for "${this.book.title}":`, error);
        toastRef.message = `Network error. Could not download images for "${this.book.title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },
  },
  created() {
    const title = this.$route.params.title;
    if (title) {
      this.getBookInfo(title);
      this.getThemes(title); // Fetch themes when the component is created
    }

    // Retrieve image URL from the query
    const imageUrl = this.$route.query.imageUrl;
    if (imageUrl) {
      this.downloadedImageUrls = [imageUrl]; // Set the image URL for display
      this.displayImages = true;
    }
  },
};
</script>

<style>
.notes-section {
  margin: 1em 0;
}

.get-notes-button {
  background-color: #5c4033;
  color: white;
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.get-notes-button:hover {
  background-color: #8b735e;
}

.notes-list {
  list-style-type: none;
  padding: 0;
}

.note-item {
  margin: 0.5em 0;
  padding: 0.5em;
  background: #f4f4f4;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.delete-note-button {
  background-color: #ff3d3d;
  color: white;
  border: none;
  padding: 0.25em 0.5em;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-note-button:hover {
  background-color: #ff6f6f;
}

.no-notes {
  color: #888;
}
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0.5em 0;
  padding: 0.5em;
  background: #f4f4f4;
  border-radius: 4px;
}

h3 {
  color: #333;
}

p {
  color: #888;
}
body {
  margin: 0;
  font-family: "Arial", sans-serif;
  background-color: #fdf8f0;
  color: #5c4033;
}

/* Header */
.header {
  background-color: #d2b48c;
  color: #fff;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}

.header button {
  background-color: #8b4513;
  border: none;
  padding: 10px;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
}

.header button:hover {
  background-color: #a0522d;
}

/* Main Container */
.main-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
}

/* Reader Frame */
.reader-frame {
  width: 100%;
  height: 500px;
  border: 2px solid #8b4513;
  border-radius: 5px;
  overflow: hidden;
  background-color: #fff;
}

.viewer {
  width: 100%;
  height: 100%;
  overflow: auto;
}

/* Toolbar */
.footer-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-toolbar button {
  background-color: #8b4513;
  border: none;
  padding: 8px 12px;
  color: #fff;
  border-radius: 5px;
  cursor: pointer;
}

.footer-toolbar button:hover {
  background-color: #a0522d;
}

.footer-toolbar input[type="color"] {
  width: 40px;
  height: 40px;
  border: none;
  cursor: pointer;
}

/* Bookmarks */
.bookmarks {
  margin-top: 10px;
}

.bookmarks h3 {
  margin: 0;
}

.bookmarks ul {
  list-style: none;
  padding: 0;
}

.bookmark-item {
  margin: 5px 0;
  padding: 5px;
  cursor: pointer;
  border: 1px solid #8b4513;
  border-radius: 5px;
  background-color: #fff7e6;
  transition: background-color 0.3s;
}

.bookmark-item:hover {
  background-color: #ffefd5;
}

.highlighted-text {
  padding: 0 5px;
  border-radius: 3px;
  color: #5c4033;
  font-weight: bold;
}

/* Footer */
.bottom-footer {
  text-align: center;
  padding: 10px;
  background-color: #d2b48c;
  color: #fff;
}
/* Ebook Reader Layout */
.ebook-reader {
  display: flex;
  flex-direction: column;
  height: 100vh;
  justify-content: space-between;
}



.file-upload {
  margin-left: auto;
}



.nav-button {
  background-color: #8b4513;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.nav-button:hover:not(:disabled) {
  background-color: #a0522d;
}

/* Page Info */
.page-info {
  font-size: 1.1rem;
  font-weight: 500;
  text-align: center;
  color: #fff;
}

/* Back Button */
.back-button {
  background-color: #a0522d;
  font-weight: bold;
}

/* Loading/Error Messages */
.error-message {
  color: red;
  text-align: center;
  margin: 10px 0;
}

.book-details-container {
  display: flex; /* Ustawienie kontenera na flexbox */
  flex-direction: row; /* Układ poziomy */
  justify-content: space-between; /* Rozdzielenie elementów */
  align-items: flex-start; /* Wyrównanie do góry */
  width: 90%; /* Dopasowanie szerokości */
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  box-sizing: border-box;
}


.library-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f5f5;
  box-sizing: border-box; /* Ensure padding doesn't add to total width */
}

.book-details-container {
  width: 90%; /* Adjust for smaller screens */
  max-width: 800px; /* Limit size on larger screens */
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  box-sizing: border-box;
}

.book-title {
  font-size: 1.8em;
  margin-bottom: 10px;
  text-align: center;
}

p {
  margin: 5px 0;
  font-size: 1em;
  line-height: 1.5;
}

.image-list {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  margin-top: 20px; /* Add some spacing from the text */
  height: 300px; /* Define a fixed height for the container */
}

.image-item {
  display: flex;
  justify-content: center; /* Center image inside the container */
  align-items: center; /* Center image inside the container */
}

.book-cover-image {
  max-width: 200px; /* Ensure the image scales proportionally */
  max-height: 100%; /* Prevent overflow beyond the container */
  border: 1px solid #ddd; /* Optional: Add a border around the image */
  border-radius: 4px; /* Optional: Slightly rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Add a shadow for styling */
}

.epub-page {
  width: 100%;
  max-width: 800px;
  margin-top: 20px;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

.header {
  background-color: #5c4033;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.download-button, .nav-button {
  padding: 10px 15px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  background-color:  hsla(0, 38%, 60%, 0.418);
  color: white;
  cursor: pointer;
  margin: 5px;
}

.download-button:hover, .nav-button:hover {
  background-color:  hsla(0, 30%, 47%, 0.418);
}

.file-input {
  margin: 10px 0;
  width: 100%;
}

.epub-viewer {
  width: 100%; /* Full width without frame */
  height: 100%;
  background-color: #fff;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-message, .error-message, .message, .first-word-message {
  font-size: 1em;
  margin: 10px 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .book-title {
    font-size: 2.5em;
  }

  .book-details-container, .epub-page {
    padding: 15px;
  }

  p {
    font-size: 1.2em;
  }

  .download-button, .nav-button {
    font-size: 0.9em;
    padding: 8px 12px;
  }
}

@media (max-width: 480px) {
  .book-title {
    font-size: 1.2em;
  }

  p {
    font-size: 0.8em;
  }

  .download-button, .nav-button {
    font-size: 0.8em;
    padding: 6px 10px;
  }
}

</style>
