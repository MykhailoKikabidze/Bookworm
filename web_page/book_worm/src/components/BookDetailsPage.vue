<template>
  <div class="library-container">
    <div class="book-details-container">
      <div v-if="book">
        <h1 class="book-title">{{ book.title }}</h1>
        
        <p><strong>Description:</strong> {{ book.description || "No description available." }}</p>
        <p><strong>Year of Publication:</strong> {{ book.year_of_pub || "Unknown" }}</p>
        <p><strong>Publisher:</strong> {{ book.publisher || "Unknown" }}</p>
        <p><strong>Authors:</strong> {{ book.authors.join(", ") || "No authors available." }}</p>
        <p><strong>Genres:</strong> {{ book.genres.join(", ") || "No genres available." }}</p>
        <p><strong>Themes:</strong> {{ themes.join(", ") || "No themes available." }}</p>

        

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
    
    <div class="epub-page">
    <h1>EPUB File Viewer</h1>

    <!-- Download Button -->
    <button @click="downloadBookFile('Coraline')" class="download-button">
      Download EPUB
    </button>

    <!-- File input for EPUB -->
    <input type="file" @change="onFileChange" class="file-input" />

    <!-- Div container for rendering the EPUB -->
    <div ref="viewer" class="epub-viewer"></div>

    <!-- Navigation Buttons -->
    <div class="nav-buttons">
      <button @click="goToPreviousPage" :disabled="currentPage === 0" class="nav-button">
        Previous Page
      </button>
      <button @click="goToNextPage" :disabled="currentPage === totalPages - 1" class="nav-button">
        Next Page
      </button>
    </div>

    <!-- Loading and Error Display -->
    <p v-if="isLoading" class="loading-message">Loading content...</p>
    <p v-if="errorMessage" class="error-message">Error: {{ errorMessage }}</p>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="firstWord" class="first-word-message">First word: {{ firstWord }}</p>
  </div>
  </div>
</template>


<script>
import ePub from "epubjs"; // Importing the epub.js library
export default {
  data() {
    return {
      book: null,
      themes: [],  // Stores the book themes
      downloadedImageUrls: [],  // Stores the URLs of downloaded images
      displayImages: false,
      isLoading: false,       // To track if content is loading
      errorMessage: "",       // To store error messages
      message: "",            // Message for feedback
      firstWord: "",          // To store the first word of the first chapter
      rendition: null,        // The EPUB rendition for rendering
      currentPage: 1,         // Current page index
      totalPages: 0,          // Total pages in the EPUB
      spineItems: [],         // Store the spine items for navigation
      bookUrl: null,   
    };
  },
  methods: {
    // Handle file change event when a file is selected
    onFileChange(event) {
      const file = event.target.files[0];
      if (file && file.type === "application/epub+zip") {
        const reader = new FileReader();

        reader.onload = (e) => {
          const arrayBuffer = e.target.result;
          this.loadEpub(arrayBuffer);
        };

        reader.readAsArrayBuffer(file);
      } else {
        alert("Please select a valid EPUB file.");
      }
    },


    // Load EPUB book into the viewer
    loadEpub(arrayBuffer) {
      this.isLoading = true;
      this.errorMessage = "";
      this.message = "";

      this.book = ePub(arrayBuffer);

      this.book.ready.then(() => {
        console.log("EPUB loaded successfully");

        this.rendition = this.book.renderTo(this.$refs.viewer, {
          width: "100%",
          height: "100%",
          flow: "scrolled", // Continuous scrolling layout
        });

        this.spineItems = this.book.spine.items;
        this.totalPages = this.spineItems.length;
        console.log(`Total pages in the EPUB: ${this.totalPages}`);

        if (this.totalPages > 0) {
          this.currentPage = 0;
          this.navigateToPage(this.currentPage);
        }

        this.extractFirstWord();
        this.isLoading = false;
      }).catch((err) => {
        this.isLoading = false;
        this.errorMessage = `Error loading EPUB: ${err.message}`;
      });
    },


   // Updated navigateToPage method
navigateToPage(index) {
  const spineItem = this.spineItems[index];
  if (spineItem) {
    console.log(`Navigating to page: ${index}, href: ${spineItem.href}`);
    this.rendition.display(spineItem.href)
      .then(() => {
        this.currentPage = index; // Update the current page index
        console.log(`Successfully displayed page: ${index}`);
      })
      .catch((err) => {
        console.error("Error displaying the page:", err);
      });
  } else {
    console.error(`Invalid spine item index: ${index}`);
  }
},


   // Go to the previous page
goToPreviousPage() {
  if (this.currentPage > 0) {
    console.log("Navigating to previous page. Current page:", this.currentPage);
    this.navigateToPage(this.currentPage - 1);
  } else {
    console.warn("Already on the first page. Cannot go back further.");
  }
},

// Go to the next page
goToNextPage() {
  if (this.currentPage < this.totalPages - 1) {
    this.navigateToPage(this.currentPage + 1);
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to the top
  }
},


    // Display all pages (for debugging purposes)
    displayAllPages() {
      for (let i = 0; i < this.totalPages; i++) {
        this.navigateToPage(i);
      }
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
          this.themes = Array.isArray(data) ? data : [];

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

.book-details-text {
  flex: 2; /* Tekst zajmuje większą część */
  margin-right: 20px; /* Odstęp od okładki */
}

.book-cover-container {
  flex: 1; /* Okładka zajmuje mniejszą część */
  display: flex; /* Flexbox dla centrowania */
  justify-content: center; /* Centrowanie poziome */
  align-items: center; /* Centrowanie pionowe */
}

.book-cover-image {
  max-width: 100%; /* Obraz skaluje się proporcjonalnie */
  max-height: 300px; /* Maksymalna wysokość */
  border: 1px solid #ddd; /* Styl ramki */
  border-radius: 4px; /* Lekko zaokrąglone rogi */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Cień */
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
  width: 100%;
  height: 600px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 5px;
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
