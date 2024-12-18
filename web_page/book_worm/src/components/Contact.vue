<template>
  <div class="ebook-reader">
    <!-- Header -->
    <header class="header">
      <h1 class="logo">📖 CozyBook Reader</h1>
      <div class="file-upload">
        <input type="file" @change="onFileChange" class="file-input" />
      </div>
    </header>

    <!-- Main Content -->
    <div class="content">
      <!-- EPUB Viewer -->
      <div ref="viewer" class="epub-viewer"></div>
    </div>

    <!-- Footer Navigation -->
    <footer class="footer">
      <button @click="goBack" class="nav-button back-button">🔙 Go Back</button>
      <button @click="goToPreviousPage" :disabled="currentPage === 1" class="nav-button">⬅ Prev</button>
      <p class="page-info">Page {{ currentPage }} of {{ totalPages }}</p>
      <button @click="goToNextPage" :disabled="currentPage === totalPages" class="nav-button">Next ➡</button>
    </footer>
  </div>
</template>

<script>
import ePub from "epubjs";

export default {
  data() {
    return {
      book: null,
      rendition: null,
      currentPage: 1, // Default to the first page
      totalPages: 0, // Total number of pages
      isLoading: false,
      errorMessage: "",
    };
  },
  methods: {
    // Handle EPUB file upload
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
        alert("Please upload a valid EPUB file.");
      }
    },

    // Load the EPUB book
    loadEpub(arrayBuffer) {
      this.isLoading = true;
      this.book = ePub(arrayBuffer);

      this.book.ready
        .then(() => {
          // Render the book in the viewer
          this.rendition = this.book.renderTo(this.$refs.viewer, {
            width: "100%",
            height: "100%",
            flow: "scrolled", // Use scrolled view for continuous reading
          });

          // Listen for location changes to update current page
          this.rendition.on("relocated", (location) => {
            this.updatePageCount(location);
          });

          // Display the first page
          this.rendition.display().then(() => {
            this.calculateTotalPages();
          });

          this.isLoading = false;
        })
        .catch((err) => {
          this.errorMessage = `Error loading EPUB: ${err.message}`;
          this.isLoading = false;
        });
    },

    // Update the current page based on the EPUB location
    updatePageCount(location) {
      const currentLocation = this.rendition.locations;
      const position = currentLocation.percentageFromTop(location.start);

      // Calculate the current page based on scroll position
      const currentPageNumber = Math.floor(position * currentLocation.total);

      // Update the page number
      this.currentPage = currentPageNumber + 1;
    },

    // Calculate total pages
    calculateTotalPages() {
      this.rendition.locations.generate().then(() => {
        this.totalPages = this.rendition.locations.total;
      });
    },

    // Navigate to the previous page
    goToPreviousPage() {
      this.currentPage--;
      this.rendition.prev();
    },

    // Navigate to the next page
    goToNextPage() {
      this.currentPage++;
      this.rendition.next();
    },

    // Go back to the upload screen
    goBack() {
      this.book = null;
      this.currentPage = 1;
      this.totalPages = 0;
      this.rendition = null;
    },
  },
};
</script>

<style scoped>
/* General Reset */
body {
  margin: 0;
  padding: 0;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: #f4f4f9;
  color: #333;
}

/* Ebook Reader Layout */
.ebook-reader {
  display: flex;
  flex-direction: column;
  height: 100vh;
  justify-content: space-between;
}

/* Header */
.header {
  background-color: #5c4033;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
}

.file-upload {
  margin-left: auto;
}

.file-input {
  background-color: #fff;
  border: 1px solid #5c4033;
  padding: 8px;
  border-radius: 5px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.file-input:hover {
  border-color: #a0522d;
}

/* Main Content */
.content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  overflow: hidden;
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

/* Footer */
.footer {
  background-color: #5c4033;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 30px;
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
  display: flex;
  align-items: center;
  gap: 5px;
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
</style>
