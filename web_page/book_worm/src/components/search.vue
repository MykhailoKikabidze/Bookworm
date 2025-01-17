<template>
  <div class="container">
    <!-- Search Bar -->
    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        @input="applyFilters"
        placeholder="Search for books..."
        class="search-input"
      />
      <button @click="getSubstrBooks(searchQuery)" class="search-button">🔍</button>

    </div>

    <div class="content">
      <!-- Filter Panel -->
      <div class="filter-panel">
        <h3>Filter Books</h3>

        <!-- Themes Selector -->
        <div class="filter-group">
          <h4 @click="toggleThemesDropdown" class="toggle-section">Themes</h4>
          <ul v-if="themesDropdownVisible" class="checkbox-list">
            <li
              v-for="(theme, index) in limitedThemes"
              :key="theme"
              v-show="index < visibleThemesCount"
            >
              <label>
                <input type="checkbox" :value="theme" v-model="selectedFilters.themes" />
                {{ theme }}
              </label>
            </li>
            <li v-if="availableThemes.length > visibleThemesCount">
              <button @click="toggleThemesVisibility" class="see-more-btn">
                {{ showMoreThemes ? "See Less" : "See More" }}
              </button>
            </li>
          </ul>
        </div>

        <!-- Genres Selector -->
        <div class="filter-group">
          <h4 @click="toggleGenresDropdown" class="toggle-section">Genres</h4>
          <ul v-if="dropdownVisible" class="checkbox-list">
            <li
              v-for="(genre, index) in limitedGenres"
              :key="genre"
              v-show="index < visibleGenresCount"
            >
              <label>
                <input type="checkbox" :value="genre" v-model="selectedFilters.genres" />
                {{ genre }}
              </label>
            </li>
            <li v-if="availableGenres.length > visibleGenresCount">
              <button @click="toggleGenresVisibility" class="see-more-btn">
                {{ showMoreGenres ? "See Less" : "See More" }}
              </button>
            </li>
          </ul>
        </div>

        <!-- Authors Selector -->
        <div class="filter-group">
          <h4 @click="toggleAuthorDropdown" class="toggle-section">Authors</h4>

          <!-- Display selected authors above the search bar -->
          <div v-if="selectedFilters.authors.length > 0" class="selected-authors">
            <span
              v-for="(author, index) in selectedFilters.authors"
              :key="author"
              class="selected-author-tag"
            >
            {{ author }}
              <button @click="removeAuthor(index)" class="remove-author-btn">X</button>
            </span>
          </div>

          <div class="search-bar">
            <input
              type="text"
              v-model="searchAuthorsQuery"
              @input="applyFilters"
              laceholder="Search for authors..."
              class="search-input"
            />
          </div>

          <ul v-if="authorDropdownVisible" class="checkbox-list">
            <li v-for="(author, index) in filteredAuthors" :key="author">
              <label>
                <input
                  type="checkbox"
                  :value="`${author.name} ${author.surname}`"
                  v-model="selectedFilters.authors"
                />
                {{ author.name }} {{ author.surname }}
              </label>
            </li>
            <li v-if="filteredAuthors.length === 0">
              <p>No authors found</p>
            </li>
            <li v-if="availableAuthors.length > visibleAuthorsCount">
              <button @click="toggleAuthorsVisibility" class="see-more-btn">
                {{ showMoreAuthors ? "See Less" : "See More" }}
              </button>
            </li>
          </ul>
        </div>

        <!-- Apply Filters Button -->
        <button @click="applyFilters" class="apply-filters-btn">Apply Filters</button>
      </div>

      <!-- Books Display -->
      <div class="library-container">
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
  </div>

    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      downloadedImageUrls: [], // Array of image URLs matching groupBooks
      groupBooks: [], 
      searchQuery: this.$route.query.query || "",
      searchAuthorsQuery: "", // Search for authors specifically
      selectedFilters: {
        themes: [],
        genres: [],
        authors: [],
      },
      availableGenres: [
        "Fiction",
        "Non-Fiction",
        "Mystery",
        "Romance",
        "Science Fiction",
        "Fantasy",
        "Historical",
        "Biography",
        "Thriller",
        "Adventure",
        "Horror",
        "Poetry",
        "Self-Help",
        "Philosophy",
        "Art",
        "Romance novel",
      ],
      availableThemes: [
        "Adventure",
        "Love",
        "Mystery",
        "Historical",
        "Science Fiction",
        "Fantasy",
        "Philosophy",
        "Life",
        "Technology",
        "Politics",
        "Nature",
      ],
      availableAuthors: [],
      filteredAuthors: [],
      books: [],
      visibleThemesCount: 5,
      visibleGenresCount: 5,
      visibleAuthorsCount: 5,
      showMoreThemes: false,
      showMoreGenres: false,
      showMoreAuthors: false,
      dropdownVisible: true,
      themesDropdownVisible: true,
      authorDropdownVisible: true,
     
      filteredBooks: [],
    };
  },
  computed: {
    limitedThemes() {
      return this.availableThemes;
    },
    limitedGenres() {
      return this.availableGenres;
    },
    limitedAuthors() {
      return this.availableAuthors;
    },
    selectedAuthorsText() {
      return this.selectedFilters.authors.length > 0
        ? this.selectedFilters.authors.join(", ")
        : "Select Author(s)";
    },
  },
  methods: {

      async searchBooks() {
    // Apply search filter first
    const searchQueryLower = this.searchQuery.toLowerCase();
    let filtered = this.groupBooks.filter((book) =>
      book.title.toLowerCase().includes(searchQueryLower)
    );

    // Then apply the filters to the already filtered books
    filtered = this.applyBookFilters(filtered);

    this.filteredBooks = filtered;  // Update the filtered books list
  },

  applyBookFilters(filteredBooks) {
    // Filter by selected authors
    if (this.selectedFilters.authors.length > 0) {
      filteredBooks = filteredBooks.filter(book =>
        this.selectedFilters.authors.some(author =>
          book.authors && book.authors.includes(author)
        )
      );
    }

    // Filter by selected themes
    if (this.selectedFilters.themes.length > 0) {
      filteredBooks = filteredBooks.filter(book =>
        this.selectedFilters.themes.some(theme =>
          book.themes && book.themes.includes(theme)
        )
      );
    }

    // Filter by selected genres
    if (this.selectedFilters.genres.length > 0) {
      filteredBooks = filteredBooks.filter(book =>
        this.selectedFilters.genres.some(genre =>
          book.genres && book.genres.includes(genre)
        )
      );
    }

    return filteredBooks;
  },

  async getSubstrBooks(substr) {
    const params = new URLSearchParams();
    params.append("substr", substr);

    try {
      const response = await fetch(`${this.$link_backend}/books/substr?${params.toString()}`, {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "anyValue",
        },
      });

      if (response.ok) {
        const data = await response.json();

        this.groupBooks = data.map(book => ({
          title: book.title,
          publisher: book.publisher,
          year_of_pub: book.year_of_pub,
          description: book.description || 'No description available.',
          authors: book.authors,  // Assuming authors are included
          genres: book.genres,    // Assuming genres are included
          themes: book.themes,    // Assuming themes are included
        }));

        // Fetch images for filtered books
        this.downloadedImageUrls = [];
        for (const book of this.groupBooks) {
          await this.downloadImage(book.title);
        }

        // After updating groupBooks, apply filters and search
        this.searchBooks();
      } else {
        const errorData = await response.json();
        console.error("Error fetching books:", errorData);
      }
    } catch (error) {
      console.error("Error fetching books:", error);
    }
  },

  applyFilters() {
    // Apply the filters and search after selecting filters
    console.log("Selected filters:", this.selectedFilters);
    this.searchBooks();  // Apply both the search and filters together
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
    async getSubstr(substr) {
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
      this.availableAuthors = data; // Lista autorów do wyświetlenia
    } else {
      const errorData = await response.json();
    }
  } catch (error) {
    console.error(`Error fetching authors:`, error);
  }

},
async getSubstrBooks(substr) {
      const params = new URLSearchParams();
      params.append("substr", substr);

      try {
        const response = await fetch(`${this.$link_backend}/books/substr?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();          

          this.groupBooks = data
        .map(book => ({
          title: book.title,
          publisher: book.publisher,
          year_of_pub: book.year_of_pub,
          description: book.description || 'No description available.',
        }));

      // Fetch images for filtered books
      this.downloadedImageUrls = [];
      for (const book of this.groupBooks) {
        await this.downloadImage(book.title);
      }

        } else {
          const errorData = await response.json();
        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);

      }

    },  
    async filterBooks(authors, themes, genres,substr){
      //all params is a list of strings. if you dont want to filter by smth just give []
      //example: ["Tom Shelby", "Anna Kawasaki"]

      const params = new URLSearchParams();
      params.append("substr", substr);

      const requestBody = {
        authors: authors,
        themes: themes,
        genres: genres,
      };

      try {
        const response = await fetch(`${this.$link_backend}/filter/books?${params.toString()}`, {
          method: "POST",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();

          this.groupBooks = data
        .map(book => ({
          title: book.title,
          publisher: book.publisher,
          year_of_pub: book.year_of_pub,
          description: book.description || 'No description available.',
        }));

      // Fetch images for filtered books
      this.downloadedImageUrls = [];
      for (const book of this.groupBooks) {
        await this.downloadImage(book.title);
      }

          return data; // You can write receive data (big json with books) into your local var
        } else {

          const error = await response.json();
          console.log("Error getting books from filters in response: ", error.detail);
        }

      } catch (error) {
        console.error("Error getting books from filters: ", error);
      }
    },
    
    
    async displayBookMetadata() {
      if (this.books.length === 0) {
        this.downloadImagesAndMetadata();
      }
      this.displayMetadata = true;
    },

    applyFilters() {
      console.log("Selected filters:", this.selectedFilters.authors);
      this.filterBooks(this.selectedFilters.authors,this.selectedFilters.themes,this.selectedFilters.genres,this.searchQuery);
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    toggleThemesDropdown() {
      this.themesDropdownVisible = !this.themesDropdownVisible;
    },
    toggleAuthorDropdown() {
      this.authorDropdownVisible = !this.authorDropdownVisible;
    },
    toggleThemesVisibility() {
      this.showMoreThemes = !this.showMoreThemes;
      this.visibleThemesCount = this.showMoreThemes
        ? this.availableThemes.length
        : 5;
    },
    toggleGenresVisibility() {
      this.showMoreGenres = !this.showMoreGenres;
      this.visibleGenresCount = this.showMoreGenres
        ? this.availableGenres.length
        : 5;
    },
    toggleAuthorsVisibility() {
      this.showMoreAuthors = !this.showMoreAuthors;
      this.visibleAuthorsCount = this.showMoreAuthors
        ? this.availableAuthors.length
        : 5;
    },
    searchBooks() {
      this.filteredBooks = this.books.filter((book) =>
        book.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    async filterAuthors() {
  const query = this.searchAuthorsQuery.trim(); // Ensure no leading/trailing whitespace

  if (query) {
    // Fetch authors from the backend using the query
    await this.getSubstr(query); // Call getSubstr to update availableAuthors based on query
    this.filteredAuthors = this.availableAuthors; // Update the filtered authors
  } else {
    // Reset filteredAuthors to all availableAuthors if the search query is empty
    this.filteredAuthors = [...this.availableAuthors];
  }
},

removeAuthor(index) {
  // Remove the selected author from the list
  this.selectedFilters.authors.splice(index, 1);
},

    
  },
  mounted() {
     if (this.searchQuery) {
      this.getSubstrBooks(this.searchQuery);
    }
    this.filteredBooks = this.books; // Show all books initially
    this.filteredAuthors = this.availableAuthors; // Show all authors initially
  },
};
</script>
<style scoped>
/* Overall page styling */
body {
  background-color: #f5e8d0;
  margin: 0;
  font-family: Arial, sans-serif;
}

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

/* Centered search bar */
.search-button {
  padding: 10px 15px;
  background-color: #ccc;
  color: white;
  border: none;
  border-radius: 5px;
  margin-left: 10px;
  cursor: pointer;
  font-size: 16px;
}

.search-button:hover {
  background-color: #ff6f61;
}

.search-bar {
  position: sticky; /* Keep search bar visible */
  top: 0;
  z-index: 10;
  background-color: #f8f8f8;
  padding: 10px;
}

.search-input {
  width: 50%;
  padding: 10px 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

/* Main container */
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

/* Filters and book list container */
.content {
  display: flex;
  gap: 20px;
}

/* Filter panel styling */
.filter-panel {
  width: 300px;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* See More / See Less Button */
.see-more-btn {
  background-color: #ff6f61;
  color: #fff;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.see-more-btn:hover {
  background-color: #e65c50;
}

/* Book list */
.books-list {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.book-item {
  width: 250px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Author dropdown section styling */
.checkbox-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.checkbox-list li {
  padding: 5px 0;
}

.checkbox-list label {
  display: flex;
  align-items: center;
}

.checkbox-list input {
  margin-right: 8px;
}

.checkbox-list li p {
  color: #888;
}

.filter-group h4 {
  cursor: pointer;
}

/* Consistent layout for filters */
.filter-group {
  margin-bottom: 20px;
}
/* Apply Filters Button */
.apply-filters-btn {
  display: block;
  width: 100%;
  padding: 15px 20px;
  margin-top: 20px;
  font-size: 13px;
  font-weight: bold;
  text-transform: uppercase;
  text-align: center;
  background: linear-gradient(90deg, #ff6f61, #ff905a);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.apply-filters-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
  background: linear-gradient(90deg, #ff905a, #ff6f61);
}

.apply-filters-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


/* Styling for selected authors */
.selected-authors {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.selected-author-tag {
  background-color: #ff6f61;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
}

.remove-author-btn {
  background: none;
  color: white;
  border: none;
  font-size: 12px;
  margin-left: 8px;
  cursor: pointer;
}

.remove-author-btn:hover {
  color: #e65c50;
}
</style>
