<template>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">

  <div class="book-info">
  <h1 class="book-title">{{ book.title }}</h1>

  

  <div class="info-item">
    <div class="info-title">Description:</div>
    <div class="info-content">{{ book.description || "No description available." }}</div>
  </div>
  
  <div class="info-item">
    <div class="info-title">Year of Publication:</div>
    <div class="info-content">{{ book.year_of_pub || "Unknown" }}</div>
  </div>
  
  <div class="info-item">
    <div class="info-title">Publisher:</div>
    <div class="info-content">{{ book.publisher || "Unknown" }}</div>
  </div>
  
  <div class="info-item">
    <div class="info-title">Authors:</div>
    <div class="info-content">
      <ul v-if="book.authors && book.authors.length">
        <li v-for="(author, index) in book.authors" :key="index">{{ author.name }} {{ author.surname }}</li>
      </ul>
      <p v-else>No authors available.</p>
    </div>
  </div>
  
  <div class="info-item">
    <div class="info-title">Genres:</div>
    <div class="info-content">
      <ul v-if="book.genres && book.genres.length">
        <li v-for="(genre, index) in book.genres" :key="index">{{ genre }}</li>
      </ul>
      <p v-else>No genres available.</p>
    </div>
  </div>

  <div class="info-item">
    <div class="info-title">Themes:</div>
    <div class="info-content">
      <ul v-if="book.themes && book.themes.length">
        <li v-for="(theme, index) in book.themes" :key="index">{{ theme }}</li>
      </ul>
      <p v-else>No themes available.</p>
    </div>
  </div>
</div>



  
  <div class="image-list" v-if="displayImages">
    <div v-for="(imageUrl, index) in downloadedImageUrls" :key="index" class="image-item">
      <img :src="imageUrl" alt="Book Cover" class="book-cover-image" />
    </div>
  </div>

<div v-else>
  <p>Loading book details...</p>
</div>




<header class="header">
<h1>Book Reader</h1>
<div class="actions">
    <!-- Dropdown to Select Group -->
    <div class="select-group-container">
      <select v-model="selectedGroup" class="group-select">
        <option value="is_favourite">Favourite</option>
        <option value="want_to_read">Want to Read</option>
        <option value="now_reading">Now Reading</option>
        <option value="have_read">Have Read</option>
      </select>
    </div>

    <!-- Button to Delete Group -->
    <button @click="deleteGroups(book.title)" class="action-button delete-button">
      Remove from Group
    </button>

    <!-- Button to Add Book to Group -->
    <button @click="postGroups(book.title)" class="action-button add-to-group-button">
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
<span>Page {{ currentPage }} of {{ totalPages }}</span>
<div></div>

<button @click="goNext" :disabled="currentPage >= totalPages">Next</button>
<button @click="handleHighlightAndPost" :disabled="!book">Add Highlight</button>
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
<button @click="getNotes('Coraline')" class="get-notes-button">Show all my Notes</button>
<div v-if="hz.length > 0">
<h3>Notes for {{ this.book.title || 'Unknown Book' }}:</h3>
<ul class="notes-list">
  <li v-for="note in hz" :key="note.id" class="note-item">
    <strong>Page {{ note.page }}:</strong> {{ note.description }} {{ note.character }}
    <button @click="deleteNotes(this.book.title, note.page, note.description)" class="delete-note-button">Delete Note</button>
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
userDescription: "",
showDescriptionModal: false,

};
},
components: {
Toast,

},

mounted() { // If book title is available from the route parameters
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
  toggleForm() {
      this.isFormVisible = !this.isFormVisible;
    },
    submitNote() {
      // Submit logic
      this.postNotes(this.title, this.page, this.description, this.quote, this.character);
    },
  handleImageUpload(event) {
  this.selectedImage = event.target.files[0];
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
  console.error('Error response:', errorData);  // Logowanie odpowiedzi błędu
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
          
          toastRef.message = `Book was deleted`;
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
          this.hz = data;

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

    // Create the JSON object for the request body
    const requestBody = {
      is_favourite: false,
      want_to_read: false,
      now_reading: true,
      have_read: false
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

toastRef.notificationClass = "success-toast";
} else {
const errorData = await response.json();
toastRef.message = `Error fetching genres for "${title}": ${errorData.detail || "Unknown error"}`;
toastRef.notificationClass = "error-toast";
}
} catch (error) {
console.error(`Error fetching genres for "${title}":`, error);
toastRef.message = `Network error. Could not fetch genres for "${title}". ${error.message}`;
toastRef.notificationClass = "error-toast";
}

this.$refs.toastRef.showNotificationMessage();
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

toastRef.notificationClass = "success-toast";
} else {
const errorData = await response.json();
toastRef.message = `Error fetching authors for "${title}": ${errorData.detail || "Unknown error"}`;
toastRef.notificationClass = "error-toast";
}
} catch (error) {
console.error(`Error fetching authors for "${title}":`, error);
toastRef.message = `Network error. Could not fetch authors for "${title}". ${error.message}`;
toastRef.notificationClass = "error-toast";
}

this.$refs.toastRef.showNotificationMessage();
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

        this.currentDescription = selectedText;

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

        this.showDescriptionModal = true; // Open the modal to write a description
      } else {
        alert("Please select text to highlight.");
      }
    },

    handleHighlightAndPost() {
      this.highlightSelection();
    },
    saveHighlightAndDescription() {
  const bookTitle = this.book?.title || this.$route.params.title;
  if (this.currentDescription && bookTitle) {
    const iframe = this.$refs.viewer.querySelector("iframe");
    const iframeWindow = iframe.contentWindow;
    const selection = iframeWindow.getSelection();

    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const startContainer = range.startContainer;
      const pageText = iframeWindow.document.body.textContent;

      // Calculate the character offset of the selected text within the page's content
      const selectedText = range.toString();
      const startOffsetInPage = pageText.indexOf(selectedText);

      if (startOffsetInPage !== -1) {
        const cfi = this.rendition.currentLocation().start.cfi;
        const quote = this.currentDescription;
        const characterOffset = startOffsetInPage; // This is the precise offset

        // Post the highlight with accurate characterOffset
        this.postNotes(bookTitle, this.currentPage, this.userDescription, quote, characterOffset);

        // Clear and close the modal
        this.userDescription = "";
        this.showDescriptionModal = false;
        alert(`Saved highlight with description: "${this.userDescription}"`);
      } else {
        alert("Failed to locate the selected text on the page.");
      }
    } else {
      alert("No text selected.");
    }
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

          toastRef.message = `Successfull"`;
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

    // Display the correct page in the eBook
    this.rendition.display(page).then(() => {
      const iframeDoc = iframeWindow.document;
      const pageText = iframeDoc.body.textContent;

      // Locate the starting position of the quote using the character offset
      const startOffsetInPage = parseInt(character, 10); // Convert character to integer

      if (isNaN(startOffsetInPage)) {
        console.error(`Invalid character offset: ${character}`);
        return;
      }

      // Find the quote in the page text
      const endOffsetInPage = startOffsetInPage + quote.length;
      const range = iframeWindow.document.createRange();
      const selection = iframeWindow.getSelection();

      let currentNode = iframeDoc.body.firstChild;
      let offset = 0;

      // Traverse the document's text nodes until we find the start and end of the quote
      while (currentNode && offset < startOffsetInPage) {
        offset += currentNode.textContent.length;
        currentNode = currentNode.nextSibling;
      }

      if (currentNode) {
        const startOffset = startOffsetInPage - offset;
        const endOffset = startOffset + quote.length;

        // Set the range to highlight the quote
        range.setStart(currentNode, startOffset);
        range.setEnd(currentNode, endOffset);

        // Create a span to wrap the quote with a highlight
        const span = iframeWindow.document.createElement("span");
        span.style.backgroundColor = "#FFD700"; // Default yellow color
        span.style.padding = "0 2px";
        span.className = "custom-highlight";
        span.textContent = quote;

        // Insert the span in place of the quoted text
        range.deleteContents();
        range.insertNode(span);

        // Clear the selection after applying the highlight
        selection.removeAllRanges();
      } else {
        console.warn(`Quote not found on page ${page}: "${quote}"`);
      }
    });
  });
}
,
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
  font-size: 0.9rem; /* Mniejsze rozmiary czcionki */
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
  background-color: #8B4513; /* Ciepły brąz */
  color: white;
  border: none;
}

.add-to-group-button:hover {
  background-color: #6b3e29;
}

.delete-button {
  background-color: #d9534f; /* Subtelna czerwień */
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
  margin-left: 20%; /* Przesuwa kontener w prawo */
  
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
  margin-left: -20px; /* Przesuwa obrazek w lewo */
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
  max-width: 300px; /* Ensure the image scales proportionally */
  max-height: 300px; /* Prevent overflow beyond the container */
  border: 1px solid #ddd; /* Optional: Add a border around the image */
  border-radius: 4px; /* Optional: Slightly rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Add a shadow for styling */
  margin-top: -20px; /* Podnosi obrazek w górę */
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

  .book-info {
    width: 65%; /* Zmniejsza szerokość kontenera na mniejszych ekranach */
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
    margin-right: -40px; /* Przesuwa obrazek w lewo */
}

}

@media (max-width: 480px) {
  .book-title {
    font-size: 1.2em;
  }

  .book-info {
    width: 95%; /* Zmniejsza szerokość kontenera jeszcze bardziej */
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
