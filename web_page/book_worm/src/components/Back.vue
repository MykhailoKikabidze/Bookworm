<template>
  <!-- <div>   
    <button @click="postcheckpoints('Coraline',5)">postcheckpoints</button>
    <button @click="postNotes('Coraline',5,'description','want to make it right',122)">postNotes</button>
    <button @click="getCheckpoints('Coraline')">getCheckpoints</button>
    <button @click="deleteNotes('Coraline',5,'description','want to make it right',122)">deleteNotes</button>
    <button @click="getGroups('Coraline')">getGroups</button>
    <button @click="getNotes('test')">get</button>
    <button @click="deleteGroups('test')">deleteGroups</button>
    <button @click="putGroups('Coraline')">putGroups</button>
    <button @click="console.log(getBooksSubstr('a'))">getBooksSubstr</button>
    <button @click="console.log(filterBooks(['Tom Clancy'],[],[]))">filterBooks</button>
    <button @click="console.log(filterBooksByGroup('now_reading'))">filterBooksByGroup</button>

    <div
    v-for="(book, index) in books"
    :key="index"
    class="book-item"
    @click="viewBookDetails(book, downloadedImageUrls[index])"
  >
    <div class="book-info">
      <h3>{{ book.title }}</h3>
      <p><strong>Year of Publication:</strong> {{ book.year_of_pub }}</p>
      <p><strong>Publisher:</strong> {{ book.publisher }}</p>
    </div>
  </div>

    <Toast ref="toastRef" />
  </div> -->
</template>



<script>
  import Toast from './Toast.vue';

export default {
  
  data() {
    return {
      isFavourite: false,
      wantToRead:false,
      nowReading: true,
      haveRead: false,
      themes: ["Mystery"],
      genres: [],
      authors: [],
      books: [],
      hz: [],

    };
  },
  components: {
    Toast,
  },
  methods: {
    handleImageUpload(event) {
  this.selectedImage = event.target.files[0];
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
},




    async postcheckpoints(title,page) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);
      params.append("page", page);

      try {
        const response = await fetch(`${this.$link_backend}/checkpoints?${params.toString()}`, {
          method: "POST",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,

          },
        });

        if (response.ok) {
          const data = await response.json();          

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
          
          toastRef.message = `Successfull ${data}"`;
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
      async deleteNotes(title,page,description,quote,character) {
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
          const data = await response.json();          
          
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
    async putNotes(title,page,description,new_description,quote,character) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);
      params.append("page", page);
      params.append("description", description);
      params.append("new_description", new_description);
      params.append("quote", quote);
      params.append("character", character);
      try {
        const response = await fetch(`${this.$link_backend}/notes?${params.toString()}`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();          
          
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
    async postNotes(title,page,description,quote,character) {
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

    async getBooksSubstr(substr){
      const param = new URLSearchParams();
      param.append("substr", substr);
      try {
        const response = await fetch(`${this.$link_backend}/books/substr?${param.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          const data = await response.json();
          return data; // You can write receive data into your local var
        } else {
          const error = await response.json();
          console.log("Error getting substr from image in response: ", error.detail);
        }

      } catch (error) {
        console.error("Error getting substr from image: ", error);
      }
    },

    async filterBooks(authors, themes, genres){
      //all params is a list of strings. if you dont want to filter by smth just give []
      //example: ["Tom Shelby", "Anna Kawasaki"]
      const requestBody = {
        authors: authors,
        themes: themes,
        genres: genres
      };

      try {
        const response = await fetch(`${this.$link_backend}/filter/books`, {
          method: "POST",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();
          return data; // You can write receive data (big json with books) into your local var
        } else {
          const error = await response.json();
          console.log("Error getting books from filters in response: ", error.detail);
        }

      } catch (error) {
        console.error("Error getting books from filters: ", error);
      }
    },

    async filterBooksByGroup(group){
      //group = "is_favourite", "want_to_read", "now_reading", "have_read"
      const param = new URLSearchParams();
      param.append("group", group);
      try {
        const response = await fetch(`${this.$link_backend}/filter/books/groups?${param.toString()}`, {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "anyValue",
            "Authorization": `Bearer ${localStorage.getItem('authToken')}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          return data; // You can write receive data (big json with books) into your local var
        } else {
          const error = await response.json();
          console.log("Error getting books from filters by group in response: ", error.detail);
        }

      } catch (error) {
        console.error("Error getting books from filters by group: ", error);
      }
    },

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