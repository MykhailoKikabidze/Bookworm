<template>
  <div class="login-container">
    <div class="background-image"></div>
    <div class="overlay"></div>
    <div class="form-container">
      <h1>Sign in</h1>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="username">Email</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <div class="password-container">
            <input 
              :type="passwordVisible ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              required 
            />
            <button type="button" class="toggle-password" @click="togglePasswordVisibility">
              <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>
        <button @click="getToken" type="submit">Sign in</button>
      </form>
      <p class="login-link">
        Don't have an account? <router-link to="/login">Create account</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      password: '',
      passwordVisible: false, // State to toggle visibility of password
      link_backend: "https://459d-94-254-173-8.ngrok-free.app",
      moder: false,
      responseData: "",
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    async authorization() {
      try {
        const response = await fetch(this.link_backend + "/users/me", {
          method: 'GET',
          headers: {
            'Content-type': 'application/json',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          },
        });

        if (!response.ok) {
          const data = await response.json();
          this.responseData = data.detail;
        } else {
          const data = await response.json();
          this.moder = data.is_moder;
          
          // Redirect to main page (e.g., App.vue) upon successful authorization
          this.$router.push('/'); // Adjust "/main" to the actual route of your main page
        }
      } catch (error) {
        console.error("Error during authorization:", error);
      }
    },
    async getToken() {
      const params = new URLSearchParams();
      params.append("username", this.username);
      params.append("password", this.password);

      try {
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
          this.responseData = data.detail;
        } else {
          const data = await response.json();
          localStorage.setItem('authToken', data.access_token);

          // Call authorization after storing token
          await this.authorization();
        }
      } catch (error) {
        console.error("Error fetching token:", error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-image: url('./pictures/book_log_in.jpg'); /* Background image */
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('./pictures/book.jpeg'); /* Background image */
  background-size: cover;
  background-position: center;
  
  z-index: 1; /* Set below other elements */
  overflow: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(250, 250, 250, 0.15); /* Lighter gray */
  z-index: 1;
}

.form-container {
  position: relative;
  z-index: 2; /* Ensure the form is above the background */
  background-color: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 350px;
  text-align: center;
  font-family: 'Georgia', serif;
  color: #002f5b;
}

h1 {
  font-size: 28px;
  color: #002f5b;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  font-size: 17px;
  color: #002f5b;
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  font-family: 'Georgia', serif;
  background-color: #f5f5f5;
  color: #2f2f2f;
}

.password-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.toggle-password {
  position: absolute;
  right: 10px; /* Adjust icon to be at the right edge */
  top: 50%;
  transform: translateY(-50%); /* Vertically center the icon */
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px; /* Size of the eye icon */
  color: #2f2f2f;
  width: 30px; /* Match the size of the icon */
  height: 30px; /* Square background for the icon */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 5px; /* Slight rounded corners for the icon background */
}

.toggle-password:hover {
  color: #004080; /* Color change on hover */
  background-color: rgba(0, 64, 128, 0.1); /* Slight background on hover */
}


button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #002f5b; /* Original button color */
  color: white;
  font-size: 18px;
  font-family: 'Georgia', serif;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #004080; /* Darker navy blue on hover */
}

.login-link {
  margin-top: 15px;
  font-size: 14px;
}

.login-link a {
  color: #002f5b;
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
  color: #004080;
}
</style>
