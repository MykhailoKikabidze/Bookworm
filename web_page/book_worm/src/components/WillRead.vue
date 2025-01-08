<template>
  <div class="library-container">
    <!-- Button to fetch and display book metadata -->
    <!-- Przycisk do wyświetlania książek -->

    <!-- Book List -->
    <div class="book-list" v-if="displayMetadata">
      <div
        v-for="(book, index) in filteredBooks"
        :key="index"
        class="book-item"
        @click="viewBookDetails(book, downloadedImageUrls[index])"
      >
        <img :src="downloadedImageUrls[index]" alt="Book Cover" class="book-cover" />
        <br>
        <h2>{{ book.title }}</h2>
        <p><strong>Year of Publication:</strong> {{ book.year_of_pub }}</p>
        <p><strong>Publisher:</strong> {{ book.publisher }}</p>
      </div>
    </div>

    <Toast ref="toastRef" />
  </div>
</template>

<script>
import Toast from './Toast.vue';

export default {
  data() {
    return {
      downloadedImageUrls: [],
      displayImages: false,
      imageSrc: null,
      books: [],
      book: [],
      imageUrl: null,
      responseData: "",
      displayMetadata: false,
      selectedImage: null,
      selectedFile: null,
      bookPdfUrl: null,
      displayPdf: false,
    };
  },
  components: {
    Toast,
  },
  mounted() {
    // Automatically fetch and display books when the component is mounted
    this.displayBookMetadata();
  },
  methods: {
    viewBookDetails(book) {
      this.$router.push({
        name: 'BookDetails',
        params: { title: book.title },
        query: { imageUrl: this.downloadedImageUrls[this.books.indexOf(book)] } // Pass the image URL as a query
      });
    },

    async displayBookMetadata() {
  if (this.books.length === 0) {
    this.downloadImagesAndMetadata();
  }
  this.displayMetadata = true;
},

async downloadImagesAndMetadata() {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("page", 1);
  params.append("page_size", 10);

  try {
    const response = await fetch(`${this.$link_backend}/books/all?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-type": "application/json",
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (response.ok) {
      const data = await response.json();

      // Filtrowanie książek tylko z grupy "want_to_read"
      this.books = data.filter(book => book.groupa === "want_to_read").map(book => ({
        title: book.title,
        publisher: book.publisher,
        year_of_pub: book.year_of_pub,
        description: book.description || "No description available.",
        genres: book.genres || [],
      }));

      // Fetch images for each book
      for (const book of this.books) {
        await this.downloadImage(book.title);
      }

      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = "Error fetching books: " + (errorData.detail || "Unknown error");
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error("Error fetching book data:", error);
    toastRef.message = "Network error. Please try again. " + error.message;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage();
},


    async downloadImage(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/img?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
          },
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);

          // Store the image URL
          this.downloadedImageUrls.push(url);

          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch image for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },
  },
  computed: {
    // Filter books to show only those in the "want_to_read" group
    filteredBooks() {
      return this.books.filter(book => book.group === 'want_to_read');
    },
  },
};
</script>

<style scoped>
h2 {
  color: #2c0404;
}

p {
  color: #5e5c5c;
}

.library-container {
  position: relative;
  width: 100%; /* Ensure it takes up the full width */
  height: 100%; /* Make the container take the full screen height */
  margin: 0;
  padding: 20px;
  font-family: 'Roboto', Arial, sans-serif;
  color: #333;
  /* Background image with opacity */
  background-image: url('/src/components/icons/background.jpg');
  background-size: cover; /* Ensure the background covers the entire container */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Prevent the image from repeating */
  opacity: 0.85; /* Apply opacity to the background */
}

.library-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4); /* Darker overlay for better readability */
  z-index: -1; /* Ensures overlay is behind the content */
}

.fetch-btn {
  display: block;
  margin: 20px auto;
  padding: 12px 25px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.fetch-btn:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

.book-list {
  display: grid; /* Używamy grid zamiast flex */
  grid-template-columns: repeat(4, 1fr); /* Cztery kolumny */
  gap: 30px; /* Przestrzeń między książkami */
  justify-content: center; /* Wyśrodkowanie listy książek */
}

.book-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%; /* Szerokość 100% w ramach kontenera */
  height: 330px; /* Zmniejszona wysokość */
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.book-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.book-cover {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #e0e0e0;
}

.book-info {
  padding: 15px;
  flex-grow: 1;
}

.book-info h3 {
  margin: 0;
  font-size: 20px;
  color: #222;
  font-weight: bold;
}

.book-info p {
  margin: 8px 0;
  font-size: 15px;
  color: #555;
  line-height: 1.5;
}

.book-info p strong {
  color: #002f5b;
}
</style>
