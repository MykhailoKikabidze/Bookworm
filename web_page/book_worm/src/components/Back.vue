<template>
  <div>
    <!-- Input fields to capture username and password from the user -->
    <input v-model="username" placeholder="Enter username" />
    <input v-model="password" type="password" placeholder="Enter password" />

    <!-- Buttons to call fetchData and getToken functions -->
    <button @click="getToken">Fetch Data</button>
    <button @click="deleteAccount">change anem</button>

    <!-- Display token and any response data -->
    <h1>{{ token }}</h1>
    <p>{{ responseData }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: "",
      responseData: "", 
      moder: false,
      username: "", // Add field for username
      password: "", // Add field for password
      link_backend: "https://4ea7-5-173-24-88.ngrok-free.app", // replace with your actual backend URL
    };
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
async deleteAccount() {
  try {
    const response = await fetch(this.link_backend + "/users", {
      method: 'DELETE',
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
      localStorage.removeItem("authToken");
      window.location.reload();
    }
  } catch (error) {
    console.error("Error posting data:", error);
  }
},

    async changePassword() {
      try {
        const params = new URLSearchParams();
params.append("new_password", "newstring");

const url = `${this.link_backend}/users/password?${params.toString()}`;

const response = await fetch(url, {method: 'PUT',
headers: {
'Content-Type': 'application/x-www-form-urlencoded',
"Authorization": "Bearer " + localStorage.getItem('authToken'),
"ngrok-skip-browser-warning": "anyValue"
},
body: params
        });

        if (!response.ok) {
          const data = await response.json();
          this.responseData = data.detail;
        } else {
          const data = await response.json();
          this.responseData = data;
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
