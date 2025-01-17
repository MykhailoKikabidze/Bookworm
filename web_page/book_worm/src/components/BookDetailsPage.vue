
<template>
   <div class="library-container">
 <div class="book-details-container1">
    <!-- Informacje o książce po lewej stronie -->
    <div class="book-info1">
      <h1 class="book-title1">
  {{ book.title }}
  <button @click="toggleFavorite(book.title)" class="favorite-btn">
    <span v-if="isFavorite(book.title)" class="favorite-active">❤️</span>
    <span v-else class="favorite-inactive">🤍</span>
  </button>
</h1>

      <div class="info-item1">
        <div class="info-title1">Description:</div>
        <div class="info-content1">{{ book.description || "No description available." }}</div>
      </div>

      <div class="info-item1">
        <div class="info-title1">Authors:</div>
        <div class="info-content1">
          <ul v-if="book.authors && book.authors.length">
            <li v-for="(author, index) in book.authors" :key="index">{{ author.name }} {{ author.surname }}</li>
          </ul>
          <p v-else>No authors available.</p>
        </div>
      </div>

      
      
      <div class="info-item1">
        <div class="info-title1">Genres:</div>
        <div class="info-content1">
          <ul v-if="book.genres && book.genres.length">
            <li v-for="(genre, index) in book.genres" :key="index">{{ genre }}</li>
          </ul>
          <p v-else>No genres available.</p>
        </div>
      </div>

      <div class="info-item1">
        <div class="info-title1">Themes:</div>
        <div class="info-content1">
          <ul v-if="book.themes && book.themes.length">
            <li v-for="(theme, index) in book.themes" :key="index">{{ theme }}</li>
          </ul>
          <p v-else>No themes available.</p>
        </div>
      </div>
      
      <div class="info-item1">
        <div class="info-title1">Year of Publication:</div>
        <div class="info-content1">{{ book.year_of_pub || "Unknown" }}</div>
      </div>
      
      <div class="info-item1">
        <div class="info-title1">Publisher:</div>
        <div class="info-content1">{{ book.publisher || "Unknown" }}</div>
      </div>
      
      
    </div>

    <!-- Obrazki książki po prawej stronie -->
    <div class="image-list1" v-if="displayImages">
      <div 
        v-for="(imageUrl, index) in downloadedImageUrls" 
        :key="index"
        class="image-item1"
      >
        <img :src="imageUrl" alt="Book Cover" class="book-cover-image1" />
      </div>
    </div>
  </div>
</div>
  
  
  <header class="header">
    <!-- Button to Add to Favorites and Want to Read -->
   

  <h1>Book Reader</h1>

  <div class="actions">
    <!-- Dropdown to Select Group -->
    <div class="select-group-container">
      <select v-model="selectedGroup" class="group-select">
        <option value="want_to_read">Want to Read</option>
        <option value="now_reading">Now Reading</option>
        <option value="have_read">Have Read</option>
      </select>
    </div>

    <!-- Button to Delete Group -->
    <button @click="deleteGroups(book.title)" class="action-button delete-button">
      Remove from Group
    </button>

    <!-- Button to Add Book to Group (based on the selected group) -->
    <button @click="addToGroup(book.title, selectedGroup)" class="action-button add-to-group-button">
      Add to Group
    </button>
  </div>
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
      <span>Page {{ currentPage+1 }} of {{ totalPages }}</span>
      <div></div>

      <button @click="goNext" :disabled="currentPage >= totalPages">Next</button>

      <button @click="goToCheckpoint">Go to checkpoint</button>

      <!-- <button @click="handleHighlightAndPost" :disabled="!book">Add Highlight</button> -->
      <input type="color" v-model="selectedColor" title="Choose Highlight Color" />

      <!-- Mini window for writing description -->
      <div v-if="showDescriptionModal" class="modal">
        <div class="modal-content">
          <h3>Add a Description</h3>
          <textarea v-model="userDescription" placeholder="Write your description here..."></textarea>
          <button @click="saveHighlightAndDescription">Save</button>
          <button @click="closeModal">Cancel</button>
        </div>
      </div>
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
    <button @click="getNotes(book.title)" class="get-notes-button">Show all my Notes</button>
    <div v-if="hz.length > 0">
      <h3>Notes for {{ this.book.title || 'Unknown Book' }}:</h3>
      <ul class="notes-list">
        <li v-for="note in hz" :key="note.id" class="note-item" @click="goToNote(note)">
          <strong>Page {{ note.page }}:</strong> {{ note.description }}
          <button @click="deleteNotes(this.book.title, note.page, note.description, note.quote, note.character)" class="delete-note-button">
            Delete Note
          </button>
        </li>
      </ul>
    </div>

  </div>
  <Toast ref="toastRef" />
</template>

<script>
import ePub from "epubjs"; // Importing the epub.js library
import Toast from './Toast.vue';

export default {
  data() {
    return {
      favorites: [], // Lista ulubionych książek
      isFormVisible: false,
      title: '',
      page: '',
      description: '',
      quote: '',
      character: '',
      isFavourite: false,
      wantToRead:false,
      nowReading: true,
      haveRead: false,
      selectedGroup: 'want_to_read', 


      currentPage: -1,
      checkPointPage: 0,
      book: null, // EPUB.js book instance
      epubBook: null,
      rendition: null, // EPUB.js rendition instance
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
      message: "", // Message for feedback
      firstWord: "", // To store the first word of the first chapter
      spineItems: [], // Store the spine items for navigation
      bookUrl: null,
      hz: [], // Store the notes fetched from backend
      group: null, // Store the group fetched from backend
      currentDescription: "",
      userDescription: "",
      showDescriptionModal: false,

      // <-- Изменено для cfiRange
      currentCfiRange: null, // Будем хранить здесь полный cfiRange выделенного текста
    };
  },
  components: {
    Toast,
  },

  mounted() { 
       // Załaduj ulubione książki z localStorage po załadowaniu komponentu
       const savedFavorites = JSON.parse(localStorage.getItem('favorites')) || [];
    this.favorites = savedFavorites;
    // Если book.title не задан в data, берём его из параметров роутинга
    this.book = this.book || { title: this.$route.params.title || "Unknown Title" };
    console.log("Loaded book title from route:", this.book.title);

    // Fetch book information (authors, genres, and themes) based on the title
    if (this.book.title) {
      this.getBookInfo(this.book.title); // To get general book info
      this.getAuthors(this.book.title);   // To get authors
      this.getGenres(this.book.title);    // To get genres
      this.getThemes(this.book.title);    // To get themes
    }
  },

  methods: {
    
     // Sprawdza, czy książka jest w ulubionych
     isFavorite(title) {
      return this.favorites.includes(title);
    },

    // Zmieniamy stan książki w ulubionych
    async toggleFavorite(title) {
  const toastRef = this.$refs.toastRef;

  if (this.isFavorite(title)) {
    // Usuwamy książkę z ulubionych
    await this.removeFromFavorites(title);
  } else {
    try {
      // Dodajemy książkę do ulubionych
      await this.addToFavorites(title);
    } catch (error) {
      // Wyświetlamy komunikat błędu, jeśli książka nie została dodana
      console.error(error.message);
      toastRef.message = `Error: ${error.message}`;
      toastRef.notificationClass = "error-toast";
      toastRef.showNotificationMessage();
    }
  }
}
,
async removeFromFavorites(title) {
  const toastRef = this.$refs.toastRef;

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    const getResponse = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (getResponse.ok) {
      const existingGroup = await getResponse.json();
      
      const updateRequestBody = {
        ...existingGroup,
        is_favourite: false,
      };

      const param = new URLSearchParams();
      param.append("title", title);

      const response = await fetch(`${this.$link_backend}/groups?${param.toString()}`, {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + localStorage.getItem("authToken"),
          "ngrok-skip-browser-warning": "anyValue",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updateRequestBody),
      });

      if (response.ok) {
        const index = this.favorites.indexOf(title);
        if (index !== -1) {
          this.favorites.splice(index, 1);
          this.updateFavoritesInLocalStorage(); // Upewnij się, że zaktualizujesz localStorage
        }

        toastRef.message = "Removed from favorites!";
        toastRef.notificationClass = "success-toast";
      } else {
        const data = await response.json();
        throw new Error(data.detail || "Failed to update favorites.");
      }
    } else if (getResponse.status === 404) {
      const index = this.favorites.indexOf(title);
      if (index !== -1) {
        this.favorites.splice(index, 1);
        this.updateFavoritesInLocalStorage();
        toastRef.message = "Removed from favorites!";
        toastRef.notificationClass = "success-toast";
      } else {
        throw new Error("Book not found in favorites.");
      }
    } else {
      throw new Error("Error fetching group data.");
    }
  } catch (error) {
    console.error("Error removing from favorites:", error.message);
    toastRef.message = `Error: ${error.message}`;
    toastRef.notificationClass = "error-toast";
  } finally {
    toastRef.showNotificationMessage();
  }
},

async addToFavorites(title) {
  const toastRef = this.$refs.toastRef;

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    const getResponse = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (getResponse.ok) {
      const existingGroup = await getResponse.json();

      const updateRequestBody = {
        ...existingGroup,
        is_favourite: true,
      };

      const param = new URLSearchParams();
      param.append("title", title);

      const response = await fetch(`${this.$link_backend}/groups?${param.toString()}`, {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + localStorage.getItem("authToken"),
          "ngrok-skip-browser-warning": "anyValue",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updateRequestBody),
      });

      if (!response.ok) {
        const data = await response.json();
        toastRef.message = "Failed to update favorites"; // Tutaj zamiast rzucać błąd, wyświetlamy komunikat
        toastRef.notificationClass = "error-toast";
        toastRef.showNotificationMessage();
      } else {
        // Operacja się powiodła, aktualizujemy stan lokalny
        this.favorites.push(title);
        this.updateFavoritesInLocalStorage();
        toastRef.message = "Added to favorites!";
        toastRef.notificationClass = "success-toast";
        toastRef.showNotificationMessage();
      }
    } else {
      // Wyświetlamy komunikat o braku książki w grupie, zamiast rzucać wyjątek
      toastRef.message = "Please, add a book to one of the groups.";
      toastRef.notificationClass = "error-toast";
      toastRef.showNotificationMessage();
    }
  } catch (error) {
    console.error("Error:", error.message);
    toastRef.message = `Error: ${error.message}`;
    toastRef.notificationClass = "error-toast";
    toastRef.showNotificationMessage();
  }
},


    // Funkcja do dodawania książki do ulubionych, którą podałeś
    async postGroupsF(title) {
      const toastRef = this.$refs.toastRef;

      try {
        const params = new URLSearchParams();
        params.append("title", title);

        const getResponse = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
          method: "GET",
          headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (getResponse.ok) {
          const existingGroup = await getResponse.json();

          const updateRequestBody = {
            ...existingGroup,
            is_favourite: true, // Ustawiamy na true, aby dodać do ulubionych
          };
          const param = new URLSearchParams();
          param.append("title", title);
          console.log("bla", updateRequestBody);

          const response = await fetch(`${this.$link_backend}/groups?${param.toString()}`, {
            method: "PUT",
            headers: {
              "Authorization": "Bearer " + localStorage.getItem("authToken"),
              "ngrok-skip-browser-warning": "anyValue",
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateRequestBody),
          });

          if (!response.ok) {
            const data = await response.json();
            throw new Error("Failed to update favorites", data.detail);
          }

          toastRef.message = "Added to favorites!";
          toastRef.notificationClass = "success-toast";
        } else {
          throw new Error("Please, add a book to one of the groups.");
        }
      } catch (error) {
        console.error(error.message);
        toastRef.message = `Error: ${error.message}`;
        toastRef.notificationClass = "error-toast";
      } finally {
        toastRef.showNotificationMessage();
      }
    },

    // Funkcja do aktualizacji ulubionych w localStorage
    updateFavoritesInLocalStorage() {
      localStorage.setItem('favorites', JSON.stringify(this.favorites));
    },
  

async addToGroup(title, groupType) {
  const toastRef = this.$refs.toastRef;

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    // Fetch the current group info
    const getResponse = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (getResponse.ok) {
      const existingGroup = await getResponse.json();

      // Check if the book is already in the desired group
      if (
        ( existingGroup.want_to_read) ||
        (existingGroup.now_reading) ||
        ( existingGroup.have_read) 
      ) {
        // Book is already in the group, show the appropriate message
        toastRef.message = `You already have this book in another group.`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();
        return; // Exit early to avoid adding the book again
      }

      // Log the existing group data for debugging
      console.log("Existing Group:", existingGroup);

      // Remove the book from the current group (set all flags to false)
      const updateRequestBody = {
        ...existingGroup,
        want_to_read: false,
        now_reading: false,
        have_read: false,
        is_favourite: existingGroup.is_favourite || false,
      };

      // Send the PUT request to remove the book from the previous group
      const putResponse = await fetch(`${this.$link_backend}/groups/${existingGroup.id}`, {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + localStorage.getItem("authToken"),
          "ngrok-skip-browser-warning": "anyValue",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updateRequestBody),
      });

      // Log the PUT response for debugging
      console.log("PUT Response:", putResponse.status, await putResponse.text());

      if (!putResponse.ok) {
        toastRef.message = `You already have this book in the ${groupType} group.`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();
        return;
      }
    } else if (getResponse.status === 404) {
      console.log("No existing group found, adding a new group.");
    } else {
      throw new Error("Failed to fetch group");
    }

    // Add the book to the new group using the postGroups method
    await this.postGroups(title, groupType);

  } catch (error) {
    console.error(error.message);
    toastRef.message = `Error: ${error.message}`;
    toastRef.notificationClass = "error-toast";
  } finally {
    toastRef.showNotificationMessage();
  }
}
,

async postGroups(title, groupType) {
  const toastRef = this.$refs.toastRef;

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    // Create the JSON object for the request body
    const requestBody = {
      is_favourite: false,
      want_to_read: groupType === "want_to_read",
      now_reading: groupType === "now_reading",
      have_read: groupType === "have_read"
    };

    // Execute the POST request with JSON body
    const response = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
        "Content-Type": "application/json", // Set content type to JSON
      },
      body: JSON.stringify(requestBody), // Use JSON.stringify to send the body as JSON
    });

    // Handle response
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response:", JSON.stringify(errorData.detail, null, 2));
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


    toggleForm() {
      this.isFormVisible = !this.isFormVisible;
    },

    submitNote() {
      // Submit logic
      this.postNotes(this.title, this.page, this.description, this.quote, this.character);
    },

    async checkPoint() {
  if (!this.epubBook || !this.epubBook.locations) {
    console.error("EPUB book or locations are not loaded yet.");
    return;
  }

  try {

    await this.getCheckpoints('Coraline');
    const pageCfi = this.epubBook.locations.cfiFromLocation(this.checkPointPage);

    if (pageCfi) {
      // Navigate to the 5th page using the CFI
      this.rendition.display(pageCfi)
        .then(() => {
          console.log("Navigated to the 5th page.");
        })
        .catch((error) => {
          console.error("Error navigating to the 5th page:", error);
        });
    } else {
      console.error("Could not determine the location for the 5th page.");
    }
  } catch (error) {
    console.error("Error navigating to the 5th page:", error);
  }
},

    handleImageUpload(event) {
      this.selectedImage = event.target.files[0];
    },

    async getCheckpoints(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/checkpoints?${params.toString()}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();          
          this.checkPointPage= data;
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch image for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },  
    async sendEpubContentToBackend() {
      try {
        if (!this.book) {
          console.error("Book is not loaded");
          return;
        }

        const spine = await this.book.loaded.spine; // Get spine items (chapters/sections)
        const chapters = spine.items; // All sections in the book
        
        for (let i = 0; i < chapters.length; i++) {
          const chapter = chapters[i];
          const chapterContent = await chapter.load(this.book.load.bind(this.book)); // Load the content
          const parsedContent = new DOMParser().parseFromString(chapterContent, "text/html"); // Parse HTML

          // Extract text content
          const textContent = parsedContent.body.textContent || "";

          // Split text into sentences for easier management
          const sentences = textContent.split(/\.\s+/);

          for (let j = 0; j < sentences.length; j++) {
            const description = sentences[j].trim(); // Description (sentence-level text)

            if (description) {
              // Prepare data to send to backend
              const page = this.book.locations.locationFromCfi(chapter.cfiBase) + j; // Approximate page number
              const title = this.book.title || "Untitled"; // Book title
              const quote = description.length > 30 ? description.substring(0, 30) + "..." : description; // Optional short quote
              const character = description.length; // Optional: character count

              // Send note to backend
              await this.postNotes(title, page, description, quote, character);
            }
          }
          // Unload chapter content to free memory
          chapter.unload();
        }

        alert("EPUB content has been sent to the backend successfully!");

      } catch (error) {
        console.error("Error processing EPUB content:", error);
        alert("An error occurred while sending EPUB content to the backend. Check console for details.");
      }
    },

    async postNotes(title, page, description, quote, character) {
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
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          toastRef.message = `Successfully submitted note for "${title}"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          console.error('Error response:', errorData);  
          toastRef.message = `Error submitting note for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error submitting note for "${title}":`, error);
        toastRef.message = `Network error. Could not submit note for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },

    submitNote() {
      this.postNotes(this.title, this.page, this.description, this.quote, this.character);
    },

    async putGroups(title) {
      const toastRef = this.$refs.toastRef; // Reference for notifications

      try {
        const params = new URLSearchParams();
        params.append("title", title);

        // Create the JSON object for the request body
        const requestBody = {
          is_favourite: false,
          want_to_read: false,
          now_reading: true,
          have_read: false
        };

        // Execute the POST request with JSON body
        const response = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "ngrok-skip-browser-warning": "anyValue",
            "Content-Type": "application/json", 
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error response:", JSON.stringify(errorData.detail, null, 2));
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
    },

    async deleteGroups(title) {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("title", title);

  try {
    const response = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (response.ok) {
      const data = await response.json();

      // Po usunięciu książki z grupy, usuń ją również z ulubionych
      await this.removeFromFavorites(title); // Wywołanie usunięcia z ulubionych

      toastRef.message = `Book was deleted and removed from favorites`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `You don't have any book in groups`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error downloading image for "${title}":`, error);
    toastRef.message = `You don't have any book in groups`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage();
},


    async getGroups(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();          
          this.group = data;

          toastRef.message = `Successfull"${data.have_read}`;
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

    async postGroups(title) {
  const toastRef = this.$refs.toastRef; // Reference for notifications

  try {
    const params = new URLSearchParams();
    params.append("title", title);

    // Dynamically set the group based on the selectedGroup value
    const requestBody = {
      is_favourite: this.selectedGroup === "is_favourite",
      want_to_read: this.selectedGroup === "want_to_read",
      now_reading: this.selectedGroup === "now_reading",
      have_read: this.selectedGroup === "have_read",
    };

    // Execute the POST request with JSON body
    const response = await fetch(`${this.$link_backend}/groups?${params.toString()}`, {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response:", JSON.stringify(errorData.detail, null, 2));
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
},



    async getGenres(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/genres?${params.toString()}`, {
          method: "GET",
          headers: { "ngrok-skip-browser-warning": "anyValue" },
        });

        if (response.ok) {
          const data = await response.json();
          this.book.genres = Array.isArray(data) ? data : [];

        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching genres for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error fetching genres for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch genres for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },

    async getAuthors(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/authors?${params.toString()}`, {
          method: "GET",
          headers: { "ngrok-skip-browser-warning": "anyValue" },
        });

        if (response.ok) {
          const data = await response.json();
          this.book.authors = Array.isArray(data) ? data : [];

        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching authors for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error fetching authors for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch authors for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

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

          this.downloadImages();

        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching details for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error fetching details for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch details for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

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

        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching themes for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error fetching themes for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch themes for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },

    async deleteNotes(title, page, description, quote, character) {
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
          // 1) Удаляем заметку из массива hz
          this.hz = this.hz.filter(note => {
            // Фильтруем по совпадению параметров
            // или по note.id, если он у вас есть
            return !(note.title === title &&
                    note.page === page &&
                    note.description === description &&
                    note.quote === quote &&
                    note.character === character);
          });

          // 2) Убираем highlight из книги
          //    Считаем, что "character" = CFI Range
          if (this.rendition && character) {
            this.rendition.annotations.remove(character, "highlight");
          }
        } else {
          const errorData = await response.json();
          toastRef.message = `Error deleting note: ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error deleting note:`, error);
        toastRef.message = `Network error. Could not delete note. ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },

    viewBookDetails(book) {
      this.$router.push({
        name: 'BookDetails',
        params: { title: book.title },
        query: { imageUrl: this.downloadedImageUrls[this.books.indexOf(book)] } 
      });
    },

    // 1) Выделяем текст и берем cfiRange
    // highlightSelection() {
    //   if (!this.book || !this.rendition) {
    //     alert("Book or rendition not ready.");
    //     return;
    //   }

    //   const iframe = this.$refs.viewer.querySelector("iframe");
    //   if (!iframe) {
    //     return;
    //   }
    //   const iframeWindow = iframe.contentWindow;
    //   const selection = iframeWindow.getSelection();
    //   const selectedText = selection.toString().trim();

    //   if (selectedText) {
    //     // Получаем стандартный cfi (начала страницы) — но он не даёт точного диапазона
    //     // const cfi = this.rendition.currentLocation().start.cfi;

    //     // <-- Изменено для cfiRange
    //     // Для точного cfiRange нам нужно взять range через epub.js
    //     if (selection.rangeCount > 0) {
    //       const range = selection.getRangeAt(0);
    //       // Проверяем, что у rendition есть метод getRangeCfi
    //       if (this.rendition.getRangeCfi) {

    //         console.log("Selected text = ", selection.toString());
    //         console.log("rangeCount = ", selection.rangeCount);
    //         if (selection.rangeCount > 0) {
    //           const range = selection.getRangeAt(0);
    //           console.log("range start = ", range.startContainer, "end = ", range.endContainer);
    //         }

    //         const cfiRange = this.rendition.getRangeCfi(range);
    //         this.currentCfiRange = cfiRange; // Запоминаем его для дальнейшей отправки
    //       } else {
    //         console.warn("this.rendition.getRangeCfi is not available.");
    //       }
    //     }

    //     const color = this.selectedColor || "#FFD700";
    //     this.currentDescription = selectedText;

    //     // Сохраняем «закладку» локально (не обязательно, но чтобы видели выделение)
    //     this.bookmarks.push({
    //       page: this.currentPage,
    //       text: selectedText,
    //       cfi: this.rendition.currentLocation().start.cfi, // можно хранить и «начальный cfi»
    //       color,
    //     });

    //     // Добавляем визуальное выделение
    //     this.rendition.annotations.add("highlight", this.rendition.currentLocation().start.cfi, {
    //       fill: color,
    //       fillOpacity: 0.5,
    //     });

    //     // Открываем модальное окно, чтобы пользователь внёс описание
    //     this.showDescriptionModal = true;
    //   } else {
    //     alert("Please select text to highlight.");
    //   }
    // },

    // handleHighlightAndPost() {
    //   console.log(ePub.VERSION);
    //   this.highlightSelection();
    // },

    //Миша писал
    async goToCheckpoint() {
      try {
        // Шлём запрос на сервер, чтобы узнать, есть ли сохранённый cfi
        const savedCfi = await this.getCheckpoint(this.book.title);
        if (!savedCfi) {
          alert("Нет сохранённого чекпоинта для этой книги!");
          return;
        }
        console.log("Переходим к сохранённому месту cfi:", savedCfi);
        // Пытаемся отобразить
        await this.rendition.display(savedCfi, { ignoreMissingRef: true });
      } catch (error) {
        console.error("Error going to checkpoint:", error);
      }
    },


    //Миша писал
    onSelected(cfiRange, contents) {
      // 1) Если почему-то cfiRange пустой, выходим
      if (!cfiRange) return;

      // 2) Получаем выделенный текст через contents.document
      const iframeDoc = contents.document;
      const selectedText = iframeDoc.defaultView.getSelection().toString().trim();
      if (!selectedText) {
        console.warn("No actual text in selection");
        return;
      }

      // 3) Подсвечиваем сразу
      this.rendition.annotations.add("highlight", cfiRange, {
        fill: this.selectedColor || "#FFD700",
        fillOpacity: 0.5,
      });

      // 4) Сохраняем cfiRange и выделенный текст во временные переменные
      this.currentCfiRange = cfiRange;
      this.currentDescription = selectedText;

      // 5) Добавляем «закладку» в bookmarks, если хотите видеть в списке
      this.bookmarks.push({
        page: this.currentPage,
        text: selectedText,
        cfi: cfiRange, // здесь сохраним именно cfiRange
        color: this.selectedColor,
      });

      // 6) Показываем модальное окно с textarea
      this.showDescriptionModal = true;
    },

    //Миша писал
    goToNote(note) {
      // Убедимся, что rendition и note.character есть
      if (!this.rendition || !note.character) {
        console.warn("Rendition not ready или note.character отсутствует");
        return;
      }

      // 1) Переходим к нужному фрагменту по CFI
      this.rendition.display(note.character).then(() => {
        // 2) После отображения делаем highlight
        this.rendition.annotations.add("highlight", note.character, {
          fill: this.selectedColor || "#ffd966", // или любой цвет, который хотите
          fillOpacity: 0.5,
        });
      });
    },

    async getCheckpoint(title) {
  try {
    const params = new URLSearchParams();
    params.append("title", title);

    const response = await fetch(
      `${this.$link_backend}/checkpoints?${params.toString()}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          "ngrok-skip-browser-warning": "anyValue",
        },
      }
    );

    if (!response.ok) {
      console.warn("No checkpoint found (or error) for", title);
      return null;
    }
    // Теперь сервер возвращает строку cfi
    const cfi = await response.text(); // или await response.json(), если сервер отдает { cfi: "..." }
    // Если это просто raw string, лучше response.text().
    // Если сервер отдает JSON-объект, например { cfi: "..."} – используйте response.json().
    return cfi;
  } catch (error) {
    console.error("Error fetching checkpoint:", error);
    return null;
  }
},

async postCheckpoint(title, cfi) {
  try {
    const params = new URLSearchParams();
    params.append("title", title);
    params.append("cfi", cfi);  // <-- вместо page

    const response = await fetch(
      `${this.$link_backend}/checkpoints?${params.toString()}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
          "ngrok-skip-browser-warning": "anyValue",
        },
      }
    );

    if (!response.ok) {
      console.warn("Error posting checkpoint for", title, "cfi=", cfi);
    }
  } catch (error) {
    console.error("Error posting checkpoint:", error);
  }
},




    // 2) Сохраняем заметку, отправляя на бекенд cfiRange как character
    saveHighlightAndDescription() {
      const bookTitle = this.book?.title || this.$route.params.title;
      if (this.currentDescription && bookTitle) {
        // В качестве quote отправляем сам выделенный текст,
        // а в поле character — наш cfiRange
        const quote = this.currentDescription;
        const cfiRange = this.currentCfiRange;

        if (!cfiRange) {
          alert("No valid CFI range found.");
          return;
        }

        const page=this.currentPage+1;
        // Отправляем на бэкенд
        this.postNotes(
          bookTitle,
          page,
          this.userDescription, // Описание от пользователя
          quote,
          cfiRange // cfiRange вместо старого "characterOffset"
        );

        // Очищаем и закрываем модал
        this.userDescription = "";
        this.showDescriptionModal = false;
        alert(`Saved highlight with description: "${this.userDescription}"`);
      } else {
        alert("No text highlighted or book title missing.");
      }
    },

    async getNotes(title) {
      const toastRef = this.$refs.toastRef;
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
          this.hz = Array.isArray(data) ? data : [];

          this.applyHighlights();

        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();

        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch image for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },

    applyHighlights() {
      if (!this.book || !this.rendition || !this.hz.length) {
        console.warn("Book, rendition, or highlights are not ready.");
        return;
      }

      const iframe = this.$refs.viewer.querySelector("iframe");
      const iframeWindow = iframe.contentWindow;

      // Loop through each note and apply highlights
      this.hz.forEach((note) => {
        const { page, quote, character } = note;

        // Здесь character = cfiRange, если мы ранее так сохранили
        // Можно снова добавить highlight, например:
        this.rendition.display(page).then(() => {
          if (!character) {
            console.warn(`No cfiRange found for page ${page}`);
            return;
          }
          // Пример добавления выделения напрямую через ePub.js
          // annotationType, cfiRange, data = {}, cb, className, styles
          this.rendition.annotations.add("highlight", character, {
            fill: "#FFD700",
            fillOpacity: 0.5,
          });
        });
      });
    },

    async loadEpub(blob) {
  try {
    const reader = new FileReader();
    reader.onload = (e) => {
      const arrayBuffer = e.target.result;
      this.epubBook = ePub(arrayBuffer);

      // рендерим во viewer
      const viewer = this.$refs.viewer;
      this.rendition = this.epubBook.renderTo(viewer, {
        width: "100%",
        height: "100%",
      });

      // Подписка на выделение текста
      this.rendition.on("selected", this.onSelected);

      // 1) Отображаем первую страницу
      this.rendition.display({ ignoreMissingRef: true })
        .then(() => {
          // 2) После окончания отображения
          this.epubBook.ready.then(async () => {
            // Сгенерировать locations для постраничной навигации
            await this.epubBook.locations.generate(1000);
            this.totalPages = this.epubBook.locations.length();
            console.log(`Total Pages: ${this.totalPages}`);
            console.log("Spine items:", this.epubBook.package.spine);
            
            // 5) Теперь подписываемся на relocated, чтобы сохранять свежий cfi
            this.rendition.on("relocated", async (location) => {
              const range = await this.rendition.getRange(location.start.cfi);
              const cfi = this.rendition.getRangeCfi(range);
              this.postCheckpoint(this.book.title, cfi);
            });
            await this.checkPoint();


            // const savedCfi = await this.getCheckpoint(this.book.title);
            // if (savedCfi) {
            //   // Окно подтверждения
            //   const answer = window.confirm(
            //     "Мы нашли сохранённое место в книге. Перейти туда?"
            //   );
            //   if (answer) {
            //     console.log("Goto saved page:", savedCfi);
            //     // Перемещаемся
            //     this.rendition.display(savedCfi, { ignoreMissingRef: true })
            //     .catch(err => {
            //       console.error("Error displaying savedCfi:", err);
            //     });
            //   }
            // }

          });
        })
        .catch((error) => {
          console.error("Error displaying rendition:", error);
        });

      // Ещё одна подписка, чтобы обновлять currentPage
      this.rendition.on("relocated", (location) => {
        this.currentPage = this.epubBook.locations.locationFromCfi(location.start.cfi);
      });
    };
    reader.readAsArrayBuffer(blob);
  } catch (error) {
    console.error("Error loading EPUB:", error);
  }
},
async postcheckpoints(title,page) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();

      params.append("title", title);
      params.append("cfi", page);

      try {
        const response = await fetch(`${this.$link_backend}/checkpoints?${params.toString()}`, {
          method: "POST",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,

          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
          this.$refs.toastRef.showNotificationMessage();
        }
        else{
          const data =await response.json();
        }
      } catch (error) {
        console.error(`Error downloading image for "${title}":`, error);
        toastRef.message = `Network error. Could not fetch image for "${title}". ${error.message}`;
        toastRef.notificationClass = "error-toast";
        this.$refs.toastRef.showNotificationMessage();

      }

    },

    async goPrevious() {
      if (this.rendition) this.rendition.prev();
      const page=this.currentPage -1;
      await this.postcheckpoints('Coraline',page.toString());
    },

    async goNext() {
      if (this.rendition) this.rendition.next();
      const page=this.currentPage +1;
      await this.postcheckpoints('Coraline',page.toString()); 
       },

    goToBookmark(cfi) {
      // Navigate to the CFI location in the book
      this.rendition.display(cfi);

      // Optionally, re-highlight the text
      this.rendition.annotations.add("highlight", cfi, {
        fill: "#FFD700",
        "fill-opacity": 0.5,
      });
    },

    // Function to download the EPUB file
    async downloadBookFile(title) {
      try {
        this.errorMessage = ""; 
        this.message = "Fetching EPUB file for download..."; 

        const response = await fetch(
          `${this.$link_backend}/books/file?title=${title}`,
          {
            method: "GET",
            headers: {
              "ngrok-skip-browser-warning": "anyValue",
            },
          }
        );

        if (response.ok) {
          const blob = await response.blob();
          this.bookUrl = URL.createObjectURL(blob); 

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

    async downloadImages() {
  try {
    const response = await fetch(`${this.$link_backend}/books/img?title=${this.book.title}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();  // <-- можно, если это действительно JSON с ошибкой
      throw new Error(errorData.detail || 'Unknown error');
    }

    // <-- ВАЖНО: получаем Blob, а не .json()
    const blob = await response.blob();

    // Создаём url-объект, чтобы показать <img :src="...">
    const urlObject = URL.createObjectURL(blob);
    this.downloadedImageUrls = [urlObject]; // Или как-то сохраняете в массив
    this.displayImages = true;

  } catch (error) {
    console.error("Error downloading images for", this.book.title, error);
    // Выводите сообщение об ошибке
  }
},
async downloadImages() {
  try {
    const response = await fetch(`${this.$link_backend}/books/img?title=${this.book.title}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();  // <-- можно, если это действительно JSON с ошибкой
      throw new Error(errorData.detail || 'Unknown error');
    }

    // <-- ВАЖНО: получаем Blob, а не .json()
    const blob = await response.blob();

    // Создаём url-объект, чтобы показать <img :src="...">
    const urlObject = URL.createObjectURL(blob);
    this.downloadedImageUrls = [urlObject]; // Или как-то сохраняете в массив
    this.displayImages = true;

  } catch (error) {
    console.error("Error downloading images for", this.book.title, error);
    // Выводите сообщение об ошибке
  }
},


    closeModal() {
      // Закрыть модальное окно без сохранения
      this.userDescription = "";
      this.showDescriptionModal = false;
    },
  },

  created() {
    const title = this.$route.params.title;
    if (title) {
      this.getBookInfo(title);
      this.getThemes(title);
    }

    // Retrieve image URL from the query
    const imageUrl = this.$route.query.imageUrl;
    if (imageUrl) {
      this.downloadedImageUrls = [imageUrl];
      this.displayImages = true;
    }
  },
};
</script>

<style>

.book-title1 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px; /* Odstęp między tytułem a sercem */
}

.favorite-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem; /* Rozmiar serca */
  padding: 0;
  margin-left: 10px;
  display: inline-flex;
  align-items: center;
}

.favorite-active {
  color: pink; /* Różowe serce dla ulubionych */
}

.favorite-inactive {
  color: gray; /* Szare serce dla książek niebędących w ulubionych */
}

.favorite-btn:hover span {
  transform: scale(1.2); /* Powiększenie serca po najechaniu */
  transition: transform 0.3s ease, color 0.3s ease;
}



@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');

.library-container {
  position: relative;
  width: 100%; /* Ensure it takes up the full width */
  height: 100%; /* Make the container take the full screen height */
  margin: 0;
  padding: 20px;
  font-family: 'Roboto', Arial, sans-serif;
  color: #333;
  /* Background image with opacity */
  background-image: url('/src/components/pictures/book3.jpeg');
  background-size: cover; /* Ensure the background covers the entire container */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Prevent the image from repeating */
  opacity: 0.85; /* Apply opacity to the background */
}

.book-details-container1 {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  margin: 20px auto;
  max-width: 800px; /* Zmniejszona maksymalna szerokość */
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid #e0e0e0;
}

.book-info1 {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px; /* Jednolity odstęp między sekcjami */
}

.book-title1 {
  font-family: 'Cinzel', serif;
  font-size: 2.2rem;
  font-weight: bold;
  color: #6E4B3A; /* Zmieniony kolor na ciemny brąz */
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 10px;
  border-bottom: 2px solid #6E4B3A; /* Brązowa linia pod tytułem */
  padding-bottom: 5px;
}


.info-item1 {
  display: flex;
  flex-direction: column;
}

/* Brązowa linia tła pod nagłówkami */
.info-title1 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #404040; /* Brązowy kolor tekstu */
  margin-bottom: 8px;
  padding-bottom: 5px; /* Odstęp pod tekstem */
  background-color: #8b67553b; /* Przezroczysty jasny brązowy kolor tła */
  
  display: inline-block; /* Zmienia szerokość elementu na pasującą do tekstu */
}

.info-content1 {
  font-size: 0.95rem; /* Zmniejszony rozmiar treści */
  color: #555555;
  line-height: 1.5;
}

.info-content1 ul li {
  border-left: 3px solid #6E4B3A; /* Brązowa linia w liście */
  padding-left: 10px;
  margin-bottom: 5px;
  color: #6E4B3A; /* Kolor tekstu w liście */
  font-weight: 500;
}

.info-content1 ul li {
  padding: 5px 0;
  border-left: 3px solid #8B4513; /* Zmieniony kolor na brązowy */
  padding-left: 10px;
  margin-bottom: 5px;
  color: #2c3e50;
  font-weight: 500;
}

.image-list1 {
  margin-left: 10px; /* Przesunięcie zdjęcia w lewo */
  margin-top: 150px; /* Przesunięcie zdjęcia w dół */
  max-width: 350px; /* Zwiększona szerokość zdjęcia */
}


.image-item1 {
  width: 100%;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background: #ffffff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.book-cover-image1 {
  width: 100%;
  height: auto; /* Zachowuje proporcje */
  display: block;
}

.image-item1:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .book-details-container1 {
    flex-direction: column; /* Ustawienie elementów w pionie dla małych ekranów */
    align-items: center;
  }

  .image-list1 {
    margin-left: 0;
    margin-top: 20px; /* Odstęp nad obrazem dla małych ekranów */
  }
}


.modal {

  
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
}

button {
  margin-right: 10px;
}
.note-form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.toggle-button {
  padding: 10px;
  font-size: 14px;
  background-color: #072d098f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.toggle-button:hover {
  background-color: #45a049;
}

.note-form {
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  margin-top: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-title {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
}

.input-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  font-size: 12px;
  color: #555;
  margin-bottom: 5px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4caf50;
}

.form-textarea {
  resize: vertical;
  height: 100px;
}

.submit-button {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #45a049;
}
.book-info {
  margin-top: 20px;
  font-family: 'Georgia', serif;
}

.book-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
}

.actions {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  margin-top: 10px;
}

.select-group-container {
  max-width: 150px;
}

.group-select {
  width: 100%;
  padding: 6px;
  font-size: 0.9rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f4f4f4;
  color: #333;
}

.action-button {
  padding: 6px 12px;
  font-size: 0.85rem;
  border-radius: 5px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  transition: all 0.3s ease;
}

.add-to-group-button {
  background-color: #8B4513;
  color: white;
  border: none;
}

.add-to-group-button:hover {
  background-color: #6b3e29;
}

.delete-button {
  background-color: #d9534f;
  color: white;
  border: none;
}

.delete-button:hover {
  background-color: #c0392b;
}

.info-item {
  margin-top: 10px;
}

.info-title {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

.info-content {
  font-size: 0.95rem;
  color: #666;
}

.book-info {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 900px;
  text-align: center;
  margin-left: 20%;
}

.info-item {
  margin-bottom: 20px;
}

.info-title {
  font-weight: bold;
  margin-bottom: 5px;
  margin: 0.5em 0;
  padding: 0.5em;
  background: #f4f4f4;
  border-radius: 4px;
}

.info-content ul {
  margin: 0;
  padding-left: 20px;
}

.info-content p {
  color: #666;
}

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
  margin-left: -20px;
  padding: 0.5em;
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
  background-color: #ffffff;
  color: #5c4033;
}

.header {
  background-color: #5c4033;
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

.main-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
}

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

.bottom-footer {
  text-align: center;
  padding: 10px;
  background-color: #d2b48c;
  color: #fff;
}

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

.page-info {
  font-size: 1.1rem;
  font-weight: 500;
  text-align: center;
  color: #fff;
}

.back-button {
  background-color: #a0522d;
  font-weight: bold;
}

.error-message {
  color: red;
  text-align: center;
  margin: 10px 0;
}

.book-details-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  width: 90%;
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
  box-sizing: border-box;
}

.book-details-container {
  width: 90%;
  max-width: 800px;
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
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  height: 300px;
}

.image-item {
  display: flex;
  justify-content: center;
  align-items: center;
}

.book-cover-image {
  max-width: 300px;
  max-height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: -20px;
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
  background-color: hsla(0, 38%, 60%, 0.418);
  color: white;
  cursor: pointer;
  margin: 5px;
}

.download-button:hover, .nav-button:hover {
  background-color: hsla(0, 30%, 47%, 0.418);
}

.file-input {
  margin: 10px 0;
  width: 100%;
}

.epub-viewer {
  width: 100%;
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

@media (max-width: 768px) {
  .book-title {
    font-size: 2.5em;
  }

  .book-info {
    width: 65%;
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

  .book-cover-image {
    margin-right: -40px;
  }
}

@media (max-width: 480px) {
  .book-title {
    font-size: 1.2em;
  }

  .book-info {
    width: 95%;
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
