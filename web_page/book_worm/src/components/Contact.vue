<template>
  <div class="epub-page">
    <h1>EPUB File Viewer</h1>

    <!-- Download Button -->
    <button @click="downloadBookFile('Coraline')">
      Download EPUB
    </button>

    <!-- File input for EPUB -->
    <input type="file" @change="onFileChange" />

    <!-- Div container for rendering the EPUB -->
    <div ref="viewer" style="width: 100%; height: 600px; overflow: auto;"></div>

    <!-- Navigation Buttons -->
    <button @click="goToPreviousPage" :disabled="currentPage === 0" aria-label="Previous Page">Previous Page</button>
    <button @click="goToNextPage" :disabled="currentPage === totalPages - 1" aria-label="Next Page">Next Page</button>

    <!-- Display All Pages Button -->
    <button @click="displayAllPages()">Display All Pages</button>

    <!-- Loading and Error Display -->
    <p v-if="isLoading" class="loading-message">Loading content...</p>
    <p v-if="errorMessage" class="error-message">Error: {{ errorMessage }}</p>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="firstWord" class="first-word-message">First word: {{ firstWord }}</p>
  </div>
</template>

<script>
import ePub from "epubjs"; // Importing the epub.js library

export default {
  data() {
    return {
      isLoading: false,       // To track if content is loading
      errorMessage: "",       // To store error messages
      message: "",            // Message for feedback
      firstWord: "",          // To store the first word of the first chapter
      book: null,             // The loaded EPUB book
      rendition: null,        // The EPUB rendition for rendering
      currentPage: 0,         // Current page index
      totalPages: 0,          // Total pages in the EPUB
      spineItems: [],         // Store the spine items for navigation
      bookUrl: null,          // URL of the EPUB file
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

      // Wait for the book to be fully loaded before rendering
      this.book.ready.then(() => {
        console.log("EPUB loaded successfully");

        // Render the book to the div container
        this.rendition = this.book.renderTo(this.$refs.viewer, {
          width: "100%",
          height: "100%",
          flow: "scrolled", // Continuous scrolling layout
        });

        // Set up the spine (collection of pages)
        this.spineItems = this.book.spine.items;
        this.totalPages = this.spineItems.length;
        console.log(`Total pages in the EPUB: ${this.totalPages}`);

        // Initialize the current page index and display the first page
        if (this.totalPages > 0) {
          this.currentPage = 0;
          this.navigateToPage(this.currentPage);
        }

        // Extract the first word of the first chapter
        this.extractFirstWord();
        this.isLoading = false;
      }).catch((err) => {
        this.isLoading = false;
        this.errorMessage = `Error loading EPUB: ${err.message}`;
      });
    },

    // Navigate to a specific page
    navigateToPage(index) {
      const spineItem = this.spineItems[index];

      // Ensure we are navigating to a valid page
      if (spineItem) {
        console.log(`Rendering page: ${spineItem.id}`);
        this.rendition.display(spineItem.href).then(() => {
          this.currentPage = index;
        }).catch((err) => {
          console.error("Error displaying the page:", err);
        });
      } else {
        console.error(`Page not found in the spine: ${index}`);
      }
    },

    // Go to the previous page
    goToPreviousPage() {
      if (this.currentPage > 0) {
        this.navigateToPage(this.currentPage - 1);
      }
    },

    // Go to the next page
    goToNextPage() {
      if (this.currentPage < this.totalPages - 1) {
        this.navigateToPage(this.currentPage + 1);
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
  },

  beforeDestroy() {
    // Clean up resources when the component is destroyed
    if (this.rendition) {
      this.rendition.destroy();
    }
    if (this.book) {
      this.book.destroy();
    }
    if (this.bookUrl) {
      URL.revokeObjectURL(this.bookUrl);
    }
  },
};
</script>

<style scoped>
.epub-page {
  padding: 20px;
  font-family: Arial, sans-serif;
}

button {
  margin: 10px 0;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
}

button:hover {
  background-color: #45a049;
}

.loading-message {
  color: #555;
  margin-top: 10px;
}

.error-message {
  color: #f44336;
  margin-top: 10px;
}

.message {
  color: #4caf50;
  margin-top: 10px;
}

.first-word-message {
  font-weight: bold;
  margin-top: 20px;
}
</style>
