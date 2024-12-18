<template>
  <div>   
    <button @click="postcheckpoints('Coraline',5)">postcheckpoints</button>
    <button @click="postNotes('Coraline',5,'description')">postNotes</button>
    <button @click="getCheckpoints('Coraline')">getCheckpoints</button>
    <button @click="deleteNotes('Coraline',5,'description')">deleteNotes</button>
    <button @click="getNotes('Coraline')">getNotes</button>

    <li v-for="(person, index) in hz" :key="index">
        Name: {{ person.page }}, Surname: {{ person.description }}
      </li>
    <Toast ref="toastRef" />
  </div>
</template>



<script>
  import Toast from './Toast.vue';

export default {
  
  data() {
    return {

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
      async deleteNotes(title,page,description) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);
      params.append("page", page);
      params.append("description", description);

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
    async putNotes(title,page,description,new_description) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);
      params.append("page", page);
      params.append("description", description);
      params.append("new_description", new_description);

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
    async postNotes(title,page,description) {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("title", title);
      params.append("page", page);
      params.append("description", description);

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