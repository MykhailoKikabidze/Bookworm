<template>
  <div>
    <!-- Check if we're on the main page before displaying buttons and response -->
    <div v-if="isMainPage">
      <button @click="fetchData">Fetch Data</button>
      <button @click="postData">Post Data</button>

      <div v-if="responseData">
        <pre>{{ responseData }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      responseData: null, // to store the backend response
      link_backend: "https://b07d-212-191-80-214.ngrok-free.app", // backend URL
    };
  },
  computed: {
    isMainPage() {
      // You can check for the route path that represents your main page
      return this.$route.path === '/'; // or '/home', depending on your route
    }
  },
  methods: {
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
        this.responseData = data; // store the response in `responseData`
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    async postData() {
      try {
        const jsonData = JSON.stringify({
          name: "test1",
          password: "test1",
          login: "test1",
          is_moder: true,
        });

        const response = await fetch(this.link_backend + "/users", {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            "ngrok-skip-browser-warning": "anyValue"
          },
          body: jsonData,
        });

        if (!response.ok) {
          const data = await response.json();
          this.responseData = data.detail;
        } else {
          const data = await response.json();
          this.responseData = data.status;
        }
      } catch (error) {
        console.error("Error posting data:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Your styles here */
</style>
