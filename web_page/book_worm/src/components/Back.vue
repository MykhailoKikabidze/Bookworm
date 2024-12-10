<template>
  <div>   

    <!-- idk if it will work i just couldn't try it so it can not work properly but you can try... -->
    <button @click="getBookInfo('Garlic & the Vampire')">For get book info for example from Boo</button>
    <div>
      <p>{{ this.book.publisher }}</p>
      <p>{{ this.book.year_of_pub }}</p>
      <p>{{ this.book.title }}</p>
      <p>{{ this.book.description }}</p>

    </div>
    <button @click="getSubstr('me')">get Substr</button>
    <li v-for="(person, index) in authorsForSerching" :key="index">
        Name: {{ person.name }}, Surname: {{ person.surname }}
      </li>

    <p>
      Authors name: {{ this.name }}, Surname {{ this.surname }}
    </p>

    <button @click="getAuthors('Garlic & the Vampire')">get authors</button>
    <li v-for="(person, index) in authors" :key="index">
        Name: {{ person.name }}, Surname: {{ person.surname }}
      </li>
    <!-- Button to download all book images -->
    <button @click="downloadImages">Download All Images</button>



    <button @click="getGenres('Coraline')">get genres</button>
    <ul v-if="genres && genres.length">
  <li v-for="(genre, index) in genres" :key="index">{{ genre }}</li>
</ul>
<p v-else>No genres available.</p>


<button @click="getThemes('Coraline')">get themes</button>
    <ul v-if="themes && themes.length">
  <li v-for="(genre, index) in themes" :key="index">{{ genre }}</li>
</ul>
<p v-else>No themes available.</p>

    <!-- Button to display the downloaded images -->
    <button @click="displayDownloadedImages">Display Images</button>

 
    <!-- it's only for displaying images -->
    <div class="image-list" v-if="displayImages"> 
      <div v-for="(imageUrl, index) in downloadedImageUrls" :key="index" class="image-item">
        <img :src="imageUrl" alt="Book Cover" class="book-cover-image" />
      </div>
    </div>

    <!-- this button for download and displaying images and description itd -->
    <button @click="displayBookMetadata">Display Book Metadata</button>

    <!-- this how it will be displayed images and title and so on but i couldn't test it so i don't if this works fine but i hope so -->
    <div class="book-list" v-if="displayMetadata">
      <div v-for="(book, index) in books" :key="index" class="book-item">
        <h3>{{ book.title }}</h3>
        <p><strong>Description:</strong> {{ book.description }}</p>
        <p><strong>Yera of publication:</strong> {{ book.year_of_pub }}</p>
        <p><strong>Publisher:</strong> {{ book.publisher }}</p>
      </div>
    </div>
    <button @click="getBook()">Download Book File</button>

<!-- Button to display the downloaded book file (PDF) -->
<button @click="displayBookFiles()">Display Book File</button>

<!-- PDF viewer iframe -->
<div class="pdf-viewer" v-if="displayPdf">
  <iframe v-if="bookPdfUrl" :src="bookPdfUrl" width="100%" height="500px" frameborder="0"></iframe>
</div>


    <Toast ref="toastRef" />
  </div>
</template>



<script>
  import Toast from './Toast.vue';

export default {
  
  data() {
    return {
      authors: [],
      genres: [],
      authorsForSerching: [],
      themes: [],

    downloadedImageUrls: [],  // Stores the URLs of downloaded images
    displayImages: false, 
    imageSrc: null, // To hold the image URL or blob
    books: [], // Store the fetched books here
    book: [],
    imageUrl: null, // Holds the downloaded image URL
    responseData: "", 
    name: "s",
    data: "",
    surname: "s",
    displayMetadata: false, // Flag to toggle metadata display
    selectedImage: null, // To store the chosen image file
    selectedFile: null,  // To store the chosen EPUB file
    bookPdfUrl: null, // Holds the PDF URL to be displayed
    displayPdf: false, // Add field for password
    };
  },
  components: {
    Toast,
  },
  methods: {
    handleImageUpload(event) {
  this.selectedImage = event.target.files[0];
},

async downloadBookFiles(){
  if (this.books.length === 0) { // Assuming books stores the fetched books
    console.log("No books available.");
    return;
  }

  for (const book of this.books) {
    try {
      await this.downloadBookFile(book.title);
    } catch (error) {
      console.error("Error processing book title ${book.title}", error);
    }
  }
},

// handleFileUpload(event) {
//   this.selectedFile = event.target.files[0];
// },
// async getFile() {
//   if (this.books.length === 0) { // Assuming `books` stores the fetched books
//     console.log("No books available.");
//     return;
//   }

//   for (const book of this.books) {
//     try {
//       await this.displayImage(book.title);
//     } catch (error) {
//       console.error(`Error processing book title "${book.title}":`, error);
//     }
//   }
// },

// // Function to display the downloaded book file (PDF) in the window
// async displayBookFile(title) {
//   const toastRef = this.$refs.toastRef;
//   const params = new URLSearchParams();
//   params.append("title", title);

//   try {
//     const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
//       method: "GET",
//       headers: {
//         "ngrok-skip-browser-warning": "anyValue",
//         "Authorization": "Bearer " + localStorage.getItem("authToken"),
//       },
//     });

//     if (response.ok) {
//       const blob = await response.blob(); // Parse the response as a Blob
//       const url = URL.createObjectURL(blob); // Create an object URL for the file

//       // Set the PDF URL for display in iframe
//       this.bookPdfUrl = url;
//       this.displayPdf = true; // Show the iframe to display the PDF

//       // Show success notification
//       toastRef.message = `Successfully fetched and displaying book file for "${title}"`;
//       toastRef.notificationClass = "success-toast";
//     } else {
//       const errorData = await response.json();
//       toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
//       toastRef.notificationClass = "error-toast";
//     }
//   } catch (error) {
//     console.error(`Error fetching and displaying book file for "${title}":`, error);
//     toastRef.message = `Network error. Could not fetch and display book file for "${title}". ${error.message}`;
//     toastRef.notificationClass = "error-toast";
//   }

//   this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
// }
// ,

// async getBook() {
//   const toastRef = this.$refs.toastRef;
//   const params = new URLSearchParams();
//   params.append("page", 1);
//   params.append("page_size", 10);

//   try {
//     const response = await fetch(`${this.$link_backend}/books/all?${params.toString()}`, {
//       method: "GET",
//       headers: {
//         "Content-type": "application/json",
//         "ngrok-skip-browser-warning": "anyValue",
//       },
//     });

//     if (response.ok) {
//       const data = await response.json();
//       this.books = data.map(book => ({
//             title: book.title,
//             description: book.description || "No description available.",
//             genres: book.genres || [],
//             author: book.author || "Unknown Author",
//             published_date: book.published_date || "Unknown Date",
//           }));      console.log(data); // Log the fetched data to check

//       // Assuming the response contains an array of books
//       if (Array.isArray(data)) {
//         const titles = data.map(book => book.title).join(", "); // Concatenate all book titles
//         toastRef.message = `Books fetched successfully! Titles: ${titles}`;
//         toastRef.notificationClass = "success-toast";
//       } else {
//         toastRef.message = "Unexpected data format received.";
//         toastRef.notificationClass = "error-toast";
//       }
//       await this.downloadBookFile();
//     } else {
//       const errorData = await response.json();
//       toastRef.message = "Error fetching books: " + (errorData.detail || "Unknown error");
//       toastRef.notificationClass = "error-toast";
//     }
//   } catch (error) {
//     console.error("Error fetching book data:", error);
//     toastRef.message = "Network error. Please try again. " + error.message;
//     toastRef.notificationClass = "error-toast";
//   }

//   this.$refs.toastRef.showNotificationMessage();
// },
// Function to download book file
// async downloadBookFile(title) {
//   const toastRef = this.$refs.toastRef;
//   const params = new URLSearchParams();
//   params.append("title", title); // Using title to request the book file

//   try {
//     const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
//       method: "GET",
//       headers: {
//         "ngrok-skip-browser-warning": "anyValue",
//         "Authorization": "Bearer " + localStorage.getItem("authToken"),
//       },
//     });

//     if (response.ok) {
//       const blob = await response.blob(); // Parse the response as a Blob
//       const url = URL.createObjectURL(blob); // Create an object URL for the file

//       // Trigger the download
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = `${title}.pdf`; // Assuming it's a PDF file (adjust the extension if needed)
//       a.click();

//       // Revoke the URL after use to release memory
//       URL.revokeObjectURL(url);

//       // Show success notification
//       toastRef.message = `Successfully downloaded the book file for "${title}"`;
//       toastRef.notificationClass = "success-toast";
//     } else {
//       const errorData = await response.json();
//       toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
//       toastRef.notificationClass = "error-toast";
//     }
//   } catch (error) {
//     console.error(`Error downloading book file for "${title}":`, error);
//     toastRef.message = `Network error. Could not download book file for "${title}". ${error.message}`;
//     toastRef.notificationClass = "error-toast";
//   }

//   this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
// }
// ,

displayBookMetadata() {
      if (this.books.length === 0) {
        this.downloadImages(); // Fetch books if not already fetched
      }
      this.displayMetadata = !this.displayMetadata; // Toggle display
    },
    // Function to download images
    async downloadImages() {
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
          
          this.books = data.map(book => ({
            title: book.title,
            description: book.description || "No description available.",
            genres: book.genres || [],
            author: book.author || "Unknown Author",
            published_date: book.published_date || "Unknown Date",
          }));
          // Loop through the fetched books and download their images
          for (const book of data) {
            await this.downloadImage(book.title);
          }

          toastRef.message = `Images downloaded successfully!`;
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

           this.book = data;
          // and to get book title or description and so on you can just write this.book.title and so on
          

          toastRef.message = `Successfully downloaded image for "${title}"`;
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

    // Function to download an individual image and store its URL
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
          const url = URL.createObjectURL(blob); // Create an object URL for the image

          // Add the image URL to the list
          this.downloadedImageUrls.push(url);

          toastRef.message = `Successfully downloaded image for "${title}"`;
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
   
    async getAuthors(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);

      try {
        const response = await fetch(`${this.$link_backend}/books/authors?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();

          this.authors = data;

          toastRef.message = `Successful#"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching: ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error :`, error);
        toastRef.message = `Network error. Could not fetch. ${error.message}`;
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

          toastRef.message = `Successful#"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching: ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error :`, error);
        toastRef.message = `Network error. Could not fetch. ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },
    async getGenres(title) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", 'Book test');

      try {
        const response = await fetch(`${this.$link_backend}/books/genres?${params.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.genres = Array.isArray(data) ? data : [];

          console.log("Genres received:", data); // Debugging line
          toastRef.message = `Successful#"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching: ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error :`, error);
        toastRef.message = `Network error. Could not fetch. ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },

    // Function to toggle the visibility of downloaded images
    displayDownloadedImages() {
      this.displayImages = !this.displayImages; // Toggle the flag
    },

    
    async getSubstr(substr) {
      const toastRef = this.$refs.toastRef;
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

          this.authorsForSerching = data;

          this.name = data.name;
          this.surname = data.surname;

          toastRef.message = `Successful#"`;
          toastRef.notificationClass = "success-toast";
        } else {
          const errorData = await response.json();
          toastRef.message = `Error fetching :" ${errorData.detail || "Unknown error"}`;
          toastRef.notificationClass = "error-toast";
        }
      } catch (error) {
        console.error(`Error :`, error);
        toastRef.message = `Network error. Could not fetch". ${error.message}`;
        toastRef.notificationClass = "error-toast";
      }

      this.$refs.toastRef.showNotificationMessage();
    },

    // // Function to toggle the visibility of downloaded images
    // displayDownloadedImages() {
    //   this.displayImages = !this.displayImages; // Toggle the flag
    // },


// async getBooksFile(title) {
//   const toastRef = this.$refs.toastRef; // Reference to the Toast component
//   const params = new URLSearchParams();
//   params.append("title", title);

//   try {
//     const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
//       method: "GET",
//       headers: {
//         "ngrok-skip-browser-warning": "anyValue", // Custom header if required
//         "Authorization": "Bearer " + localStorage.getItem("authToken"),
//       },
//     });

//     if (response.ok) {
//       const blob = await response.blob(); // Parse the response as a Blob
//       const url = URL.createObjectURL(blob); // Create an object URL for the file

//       // Trigger the download
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = title; // Use the book title as the file name
//       a.click();

//       // Revoke the URL after use to release memory
//       URL.revokeObjectURL(url);

//       // Show success notification
//       toastRef.message = `Successfully downloaded file for "${title}"`;
//       toastRef.notificationClass = "success-toast";
//     } else {
//       const errorData = await response.json();
//       toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
//       toastRef.notificationClass = "error-toast";
//     }
//   } catch (error) {
//     console.error(`Error downloading file for "${title}":`, error);
//     toastRef.message = `Network error. Could not download file for "${title}". ${error.message}`;
//     toastRef.notificationClass = "error-toast";
//   }

//   this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
// }
// ,

// async displayImage(title) {
//   const toastRef = this.$refs.toastRef; // Reference to the Toast component
//   const params = new URLSearchParams();
//   params.append("title", title);

//   try {
//     // Fetch the image file from the backend
//     const response = await fetch(`${this.$link_backend}/books/img?${params.toString()}`, {
//       method: "GET",
//       headers: {
//         "ngrok-skip-browser-warning": "anyValue", // Custom header if required
//         "Authorization": "Bearer " + localStorage.getItem("authToken"),
//       },
//     });

//     if (response.ok) {
//       const blob = await response.blob(); // Parse the response as a Blob
//       const url = URL.createObjectURL(blob); // Create an object URL for the image

//       // Trigger the image download (like getBooksFile)
//       const a = document.createElement("a");
//       a.href = url;
//       a.download = `${title}.png`; // Use a default extension if backend doesn't provide it
//       a.click();

//       // Display the image in the same window
//       this.imageUrl = url;

//       // Show success notification
//       toastRef.message = `Successfully downloaded and displayed image for "${title}"`;
//       toastRef.notificationClass = "success-toast";
//     } else {
//       const errorData = await response.json();
//       toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
//       toastRef.notificationClass = "error-toast";
//     }
//   } catch (error) {
//     console.error(`Error downloading and displaying image for "${title}":`, error);
//     toastRef.message = `Network error. Could not download image for "${title}". ${error.message}`;
//     toastRef.notificationClass = "error-toast";
//   }

//   this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
// }

},

};
</script>


<style scoped>
.book-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 20px 0;
  padding: 10px;
  width: 100%;
}

.book-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.book-item h3 {
  margin: 0;
  font-size: 1.5em;
}

.book-item p {
  margin: 5px 0;
  color: #555;
}

/* Container for the images stacked vertically */
.image-list {
  display: block;
  padding: 10px;
  margin: 20px 0;
  width: 100%;
}

/* Style for each image item */
.image-item {
  margin-bottom: 40px;  /* Add space between images */
  display: block;
  text-align: left;  /* Align images to the left */
}

/* Style for the book cover image */
.book-cover-image {
  max-width: 100%;  /* Make the image responsive */
  height: auto; /* Maintain the aspect ratio */
  max-height: 250px; /* Limit the height of images */
  object-fit: cover;  /* Crop the image to maintain aspect ratio */
  border-radius: 5px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.book-cover-image:hover {
  transform: scale(1.05);  /* Slight zoom effect on hover */
}
</style>