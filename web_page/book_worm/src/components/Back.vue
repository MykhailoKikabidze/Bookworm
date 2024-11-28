<template>
  <div>
    <!-- Input fields for username and password -->
    <input v-model="username" placeholder="Enter username" />
    <input v-model="password" type="password" placeholder="Enter password" />

    <!-- Buttons to fetch data and get token -->
    <button @click="getToken">Fetch Data</button>
    <button @click="changeName">Change Name</button>

    <!-- Button to download all book images -->
    <button @click="downloadImages">Download All Images</button>

    <!-- Button to display the downloaded images -->
    <button @click="displayDownloadedImages">Display Images</button>

    <!-- Image grid container -->
    <div class="image-list" v-if="displayImages">
      <div v-for="(imageUrl, index) in downloadedImageUrls" :key="index" class="image-item">
        <img :src="imageUrl" alt="Book Cover" class="book-cover-image" />
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
      token: "",
    downloadedImageUrls: [],  // Stores the URLs of downloaded images
    displayImages: false, 
    imageSrc: null, // To hold the image URL or blob
    bookTitle: [], // Store the fetched books here
    hz: "",
    imageUrl: null, // Holds the downloaded image URL
    joj: "s",
    responseData: "", 
    moder: false,
    selectedImage: null, // To store the chosen image file
    selectedFile: null,  // To store the chosen EPUB file
    username: "", // Add field for username
    password: "", // Add field for password
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
  if (this.bookTitle.length === 0) { // Assuming books stores the fetched books
    console.log("No books available.");
    return;
  }

  for (const book of this.bookTitle) {
    try {
      await this.downloadBookFile(book.title);
    } catch (error) {
      console.error("Error processing book title ${book.title}", error);
    }
  }
},

handleFileUpload(event) {
  this.selectedFile = event.target.files[0];
},
async getFile() {
  if (this.bookTitle.length === 0) { // Assuming `books` stores the fetched books
    console.log("No books available.");
    return;
  }

  for (const book of this.bookTitle) {
    try {
      await this.displayImage(book.title);
    } catch (error) {
      console.error(`Error processing book title "${book.title}":`, error);
    }
  }
},

// Function to display the downloaded book file (PDF) in the window
async displayBookFile(title) {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("title", title);

  try {
    const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue",
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
      },
    });

    if (response.ok) {
      const blob = await response.blob(); // Parse the response as a Blob
      const url = URL.createObjectURL(blob); // Create an object URL for the file

      // Set the PDF URL for display in iframe
      this.bookPdfUrl = url;
      this.displayPdf = true; // Show the iframe to display the PDF

      // Show success notification
      toastRef.message = `Successfully fetched and displaying book file for "${title}"`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error fetching and displaying book file for "${title}":`, error);
    toastRef.message = `Network error. Could not fetch and display book file for "${title}". ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
}
,

async getBook() {
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
      this.bookTitle=data;
      console.log(data); // Log the fetched data to check

      // Assuming the response contains an array of books
      if (Array.isArray(data)) {
        const titles = data.map(book => book.title).join(", "); // Concatenate all book titles
        toastRef.message = `Books fetched successfully! Titles: ${titles}`;
        toastRef.notificationClass = "success-toast";
      } else {
        toastRef.message = "Unexpected data format received.";
        toastRef.notificationClass = "error-toast";
      }
      await this.downloadBookFile();
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
// Function to download book file
async downloadBookFile(title) {
  const toastRef = this.$refs.toastRef;
  const params = new URLSearchParams();
  params.append("title", title); // Using title to request the book file

  try {
    const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue",
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
      },
    });

    if (response.ok) {
      const blob = await response.blob(); // Parse the response as a Blob
      const url = URL.createObjectURL(blob); // Create an object URL for the file

      // Trigger the download
      const a = document.createElement("a");
      a.href = url;
      a.download = `${title}.pdf`; // Assuming it's a PDF file (adjust the extension if needed)
      a.click();

      // Revoke the URL after use to release memory
      URL.revokeObjectURL(url);

      // Show success notification
      toastRef.message = `Successfully downloaded the book file for "${title}"`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error downloading book file for "${title}":`, error);
    toastRef.message = `Network error. Could not download book file for "${title}". ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
}
,

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

    // Function to toggle the visibility of downloaded images
    displayDownloadedImages() {
      this.displayImages = !this.displayImages; // Toggle the flag
    },

    // Fetch token
    async getToken() {
      const params = new URLSearchParams();
      params.append("username", "carrot@gmail.com");
      params.append("password", "userpass");

      const response = await fetch(this.link_backend + "/token", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          "ngrok-skip-browser-warning": "anyValue"
        },
        body: params
      });

      if (!response.ok) {
        const data = await response.json();
        this.token = data.detail;
      } else {
        const data = await response.json();
        this.token = data.access_token;
        localStorage.setItem('authToken', this.token);
      }
    },

    // Change username
    async changeName() {
      try {
        const params = new URLSearchParams();
        params.append("new_username", "newstring@gmail.com");

        const response = await fetch(`${this.link_backend}/users/name?${params.toString()}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          }
        });

        const data = await response.json();
        this.responseData = data;
      } catch (error) {
        console.error("Error posting data:", error);
      }
    },

    
async getBooksFile(title) {
  const toastRef = this.$refs.toastRef; // Reference to the Toast component
  const params = new URLSearchParams();
  params.append("title", title);

  try {
    const response = await fetch(`${this.$link_backend}/books/file?${params.toString()}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue", // Custom header if required
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
      },
    });

    if (response.ok) {
      const blob = await response.blob(); // Parse the response as a Blob
      const url = URL.createObjectURL(blob); // Create an object URL for the file

      // Trigger the download
      const a = document.createElement("a");
      a.href = url;
      a.download = title; // Use the book title as the file name
      a.click();

      // Revoke the URL after use to release memory
      URL.revokeObjectURL(url);

      // Show success notification
      toastRef.message = `Successfully downloaded file for "${title}"`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error fetching file for "${title}": ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error downloading file for "${title}":`, error);
    toastRef.message = `Network error. Could not download file for "${title}". ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
}
,

async displayImage(title) {
  const toastRef = this.$refs.toastRef; // Reference to the Toast component
  const params = new URLSearchParams();
  params.append("title", title);

  try {
    // Fetch the image file from the backend
    const response = await fetch(`${this.$link_backend}/books/img?${params.toString()}`, {
      method: "GET",
      headers: {
        "ngrok-skip-browser-warning": "anyValue", // Custom header if required
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
      },
    });

    if (response.ok) {
      const blob = await response.blob(); // Parse the response as a Blob
      const url = URL.createObjectURL(blob); // Create an object URL for the image

      // Trigger the image download (like getBooksFile)
      const a = document.createElement("a");
      a.href = url;
      a.download = `${title}.png`; // Use a default extension if backend doesn't provide it
      a.click();

      // Display the image in the same window
      this.imageUrl = url;

      // Show success notification
      toastRef.message = `Successfully downloaded and displayed image for "${title}"`;
      toastRef.notificationClass = "success-toast";
    } else {
      const errorData = await response.json();
      toastRef.message = `Error fetching image for "${title}": ${errorData.detail || "Unknown error"}`;
      toastRef.notificationClass = "error-toast";
    }
  } catch (error) {
    console.error(`Error downloading and displaying image for "${title}":`, error);
    toastRef.message = `Network error. Could not download image for "${title}". ${error.message}`;
    toastRef.notificationClass = "error-toast";
  }

  this.$refs.toastRef.showNotificationMessage(); // Display the toast notification
}

,
    async addBooks() {

  const toastRef = this.$refs.toastRef; // Reference for notifications

  // Check if files are selected
  if (!this.selectedImage || !this.selectedFile) {
    toastRef.message = "File(s) are missing.";
    toastRef.notificationClass = "error-toast";
    this.$refs.toastRef.showNotificationMessage();
    return;
  }

  try {
    // Define query parameters
    const params = {
      title: "joj",
      year_of_pub: 2004,
      num_of_pages: 23,
      description: "joj",
      publisher: "Joj Joj",
    };

    // Construct the query string
    const queryPar = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      queryPar.append(key, String(value)); // Convert all values to strings
    }

    // Create FormData object for files and additional JSON body data
    const formData = new FormData();
    formData.append("authors", "sup");
    formData.append("themes", "Classic");
    formData.append("genres", "Classic");
    formData.append("file_img_book", this.selectedImage); // Add image file
    formData.append("file_book", this.selectedFile); // Add EPUB file

    // Execute the POST request
    const response = await fetch(`${this.$link_backend}/books/?${queryPar.toString()}`, {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("authToken"),
        "ngrok-skip-browser-warning": "anyValue",
      },
      body: formData, // Use FormData as the request body
    });

    // Handle response
    if (!response.ok) {
      const errorData = await response.json();
      toastRef.message = errorData.detail || "Error adding the book.";
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
    async fetchData() {
      
      try {
        const response = await fetch(this.link_backend + "/", {
          method: 'GET',
          headers: {
            'Content-type': 'application/json',
            "ngrok-skip-browser-warning": "anyValue"
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        this.responseData = data; 
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async getToken() {

const params = new URLSearchParams();
params.append("username", "carrot@gmail.com");
params.append("password", "userpass");

const response = await fetch(this.link_backend + "/token", {
method: 'POST',
headers: {
'Content-Type': 'application/x-www-form-urlencoded',
"ngrok-skip-browser-warning": "anyValue"
},
body: params
});

  if (!response.ok) {
    const data = await response.json();
    this.token = data.detail;
  } else {
    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('authToken',this.token);
  }
},
async changeName() {
  try {
    // Initialize URLSearchParams to add the query parameter
    const params = new URLSearchParams();
    params.append("new_username", "newstring@gmail.com");

    // Append the query parameters to the URL
    const url = `${this.link_backend}/users/name?${params.toString()}`;

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": "Bearer " + localStorage.getItem('authToken'),
        "ngrok-skip-browser-warning": "anyValue"
      }
    });

    if (!response.ok) {
      const data = await response.json();
      this.responseData = data;
    } else {
      const data = await response.json();
      this.responseData = data;
    }
  } catch (error) {
    console.error("Error posting data:", error);
  }
}
, 
},

};
</script>



<style scoped>
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