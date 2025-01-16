<template>
  <div class="library-container">
    <!-- Book List -->
    <div class="book-list" v-if="groupBooks.length > 0">
      <div
        v-for="(book, index) in groupBooks"
        :key="index"
        class="book-item"
        @click="viewBookDetails(book, downloadedImageUrls[index])"
      >
        <img :src="downloadedImageUrls[index]" alt="Book Cover" class="book-cover" />
        <h2>{{ book.title }}</h2>
        <p><strong>Year of Publication:</strong> {{ book.year_of_pub }}</p>
        <p><strong>Publisher:</strong> {{ book.publisher }}</p>
      </div>
    </div>

    <!-- Fallback message -->
    <p v-else>No books available in this group.</p>

    <Toast ref="toastRef" />
  </div>
</template>


<script>
import Toast from './Toast.vue';

export default {
  data() {
    return {
      downloadedImageUrls: [], // Array of image URLs matching groupBooks
      groupBooks: [], // Store books filtered by group
      books: [], // All books fetched
    };
  },
  components: {
    Toast,
  },
  mounted() {
    // Wywołanie fetchGroupBooks od razu po załadowaniu komponentu
    this.fetchGroupBooks('is_favourite');
  },
  methods: {
    async fetchGroupBooks(group) {
      const toastRef = this.$refs.toastRef;

      try {
        const param = new URLSearchParams();
        param.append('group', group);

        const response = await fetch(`${this.$link_backend}/filter/books/groups?${param.toString()}`, {
          method: 'GET',
          headers: {
            'ngrok-skip-browser-warning': 'anyValue',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          },
        });

        if (response.ok) {
          const data = await response.json();

          // Filtracja książek na podstawie grupy
          this.groupBooks = data
            .filter(book => !book.is_favourite)  // Tylko książki, które nie są ulubionymi
            .map(book => ({
              title: book.title,
              publisher: book.publisher,
              year_of_pub: book.year_of_pub,
              description: book.description || 'No description available.',
            }));

          // Pobranie obrazów dla przefiltrowanych książek
          this.downloadedImageUrls = [];
          for (const book of this.groupBooks) {
            await this.downloadImage(book.title);
          }
        } else {
          const error = await response.json();
          toastRef.message = `Error fetching books: ${error.detail || 'Unknown error'}`;
          toastRef.notificationClass = 'error-toast';
          toastRef.showNotificationMessage();
        }
      } catch (error) {
        console.error('Error fetching group books:', error);
        toastRef.message = 'Network error. Please try again.';
        toastRef.notificationClass = 'error-toast';
        toastRef.showNotificationMessage();
      }
    },

    async downloadImage(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append('title', title);

      try {
        const response = await fetch(`${this.$link_backend}/books/img?${params.toString()}`, {
          method: 'GET',
          headers: {
            'ngrok-skip-browser-warning': 'anyValue',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
          },
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);

          // Store the image URL in the same order as groupBooks
          this.downloadedImageUrls.push(url);
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching image for "${title}": ${errorData.detail || 'Unknown error'}`;
          toastRef.notificationClass = 'error-toast';
          toastRef.showNotificationMessage();
        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch image for "${title}". ${error.message}`;
        toastRef.notificationClass = 'error-toast';
        toastRef.showNotificationMessage();
      }
    },

    viewBookDetails(book, imageUrl) {
      this.$router.push({
        name: 'BookDetails',
        params: { title: book.title },
        query: { imageUrl }, // Pass the image URL as a query
      });
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
  width: 100%; /* Zapewnia, że kontener zajmuje całą szerokość */
  height: 100vh; /* Ustala wysokość kontenera na 100% wysokości okna przeglądarki */
  margin: 0;
  padding: 20px;
  font-family: 'Roboto', Arial, sans-serif;
  color: #333;
  /* Background image with opacity */
  background-image: url('/src/components/icons/stena.webp');
  background-size: cover; /* Zapewnia, że tło pokrywa cały kontener */
  background-position: center; /* Ustawia tło na środku */
  background-repeat: no-repeat; /* Zapobiega powtarzaniu się tła */
  opacity: 0.85; /* Ustawia pełną widoczność tła */
}

.library-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4); /* Przyciemniony overlay dla lepszej widoczności tekstu */
  z-index: -1; /* Zapewnia, że overlay jest pod zawartością */
}

/* Reszta stylów pozostaje bez zmian */




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
