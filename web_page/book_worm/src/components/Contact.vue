<template>
  <div class="epub-page">
    <h1>EPUB File Viewer</h1>

    <!-- Download Button -->
    <button @click="downloadBookFile('Play')">
      Download EPUB
    </button>

    <!-- Display Button -->
    <button @click="displayBookFile">
      Display EPUB
    </button>
    
    <!-- Loading and Error Display -->
    <p v-if="isLoading" class="loading-message">Loading content...</p>
    <p v-if="errorMessage" class="error-message">Error: {{ errorMessage }}</p>
    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="firstWord" class="first-word-message">First word: {{ firstWord }}</p>

    <!-- Viewer Container -->
    <div id="viewer" v-if="isDisplaying" class="epub-viewer"></div>
  </div>
</template>

<script>
import ePub from "epubjs"; // Import ePub.js library

export default {
  data() {
    return {
      isDisplaying: false, // To track if the EPUB is being displayed
      isLoading: false, // To track if content is loading
      errorMessage: "", // To store error messages
      message: "", // Message for feedback
      book: null, // Reference to the ePub.js book instance
      rendition: null, // Reference to the ePub.js rendition
      bookUrl: null, // To store the URL of the fetched EPUB file
      firstWord: "", // To store the first word of the first chapter
    };
  },
  methods: {
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
        } else {
          const errorData = await response.json();
          this.errorMessage =
            errorData.detail || "Failed to download the EPUB file.";
        }
      } catch (error) {
        this.errorMessage = `An error occurred while downloading: ${error.message}`;
      }
    },

    // Function to display the EPUB content in the viewer
    async displayBookFile() {
      if (!this.bookUrl) {
        this.errorMessage = "No EPUB file available to display.";
        return;
      }

      try {
        this.errorMessage = ""; // Reset error message
        this.isDisplaying = false; // Reset displaying state
        this.message = "Fetching EPUB content..."; // Initial message
        this.isLoading = true; // Start loading state

        // Initialize the ePub.js book instance
        this.book = ePub(this.bookUrl);

        // Render the EPUB content in the viewer
        const viewerElement = document.getElementById("viewer");
        this.rendition = this.book.renderTo(viewerElement, {
          width: "100%",
          height: "100%",
        });

        // Display the first page
        this.rendition.display();

        this.rendition.on("rendered", (section) => {
          console.log("Page rendered:", section);
          this.message = "EPUB content loaded successfully.";
          this.isDisplaying = true;
        });

        // Extract the first word
        const spine = await this.book.loaded.spine;
        const firstItem = spine.items[0];
        const firstText = await firstItem.load(this.book.load.bind(this.book));
        const content = new DOMParser().parseFromString(firstText, "text/html");
        this.firstWord = content.body.textContent.split(/\s+/)[0];
      } catch (error) {
        this.errorMessage = `An error occurred while displaying the book: ${error.message}`;
      } finally {
        this.isLoading = false; // End loading state
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

.epub-viewer {
  margin-top: 20px;
  border: 1px solid #ccc;
  height: 500px; /* Set height for better display */
  overflow: auto;
  background-color: #f9f9f9;
  padding: 15px;
  font-size: 16px;
  color: black;
}

.loading-message {
  color: #555;
  margin-top: 20px;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.message {
  color: #333;
  margin-top: 10px;
}

.first-word-message {
  color: #2c6bc2;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
}
</style>
