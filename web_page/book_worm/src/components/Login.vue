
<template>
  <div class="login-container">
    
    <div v-if="showToast" class="toast"> <!--if there be wrong email or password it will show message about it-->
      {{ errorMessage }}
    </div>

    <div class="overlay"></div> <!-- Warstwa półprzezroczysta nad obrazem tła -->
    <div :class="['form-container', { 'login-failed': loginFailed }]">
      <h1>Create account</h1>
      <form @submit.prevent="postData">
        <div class="input-group">
          <label for="email">Email</label>
          <input
            type="text"
            id="email"
            v-model="email"
            :class="{ 'input-error': !isEmailValid && email.length > 0 }"
            required
          />
          <span v-if="!isEmailValid && email.length > 0" class="error-message">Please enter a valid email.</span>
        </div>
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            :class="{ 'input-error': !isPasswordValid && password.length > 0 }"
            required
          />
          <span v-if="!isPasswordValid && password.length > 0" class="error-message">Password must be at least 8 characters.</span>
        </div>
        <button @click="postData" type="submit" :disabled="!isEmailValid || !isPasswordValid">Create</button>
      </form>
      <p class="signin-link">
        Already have an account? <router-link to="/sign_in">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
// Import validator.js
import validator from 'validator';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      responseData: null,
      link_backend: "https://4fd3-94-254-173-8.ngrok-free.app",
      loginFailed: false, 
      errorMessage: "", 
      token: "",
      sps: "",
      showToast: false 
    };
  },
  computed: {
    // Validate email using validator.js
    isEmailValid() {
      return validator.isEmail(this.email);
    },
    // Validate password with minimum length of 8
    isPasswordValid() {
      return validator.isLength(this.password, { min: 8 });
    }
  },
  methods: {
    async getToken() {
  const params = new URLSearchParams();
  params.append("username", this.email);
  params.append("password", this.password);

  const response = await fetch(this.link_backend + "/token", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      "ngrok-skip-browser-warning": "anyValue"
    },
    body: params
  });

  if (response.ok) {
    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('authToken', this.token);  // Store token in localStorage

    // Redirect to home page on successful login
    this.$router.push('/');  // or any other route you prefer after login
  } else {
    const data = await response.json();
    this.token = data.detail;
    this.errorMessage = "Failed to retrieve token. Please try again.";
    this.showToast = true;
    setTimeout(() => { this.showToast = false; }, 3000);
  }
},
    async postData() {
      // Prevent sending if fields are invalid (shouldn't happen due to button disable)
      if (!this.isEmailValid || !this.isPasswordValid) {
        this.errorMessage = "Please correct your email or password.";
        this.showToast = true;
        setTimeout(() => { this.showToast = false; }, 3000);
        return;
      }

      try {
        const jsonData = JSON.stringify({
          name: this.username,
          password: this.password,
          login: this.email,
          is_moder: true
        });

        const response = await fetch(this.link_backend + "/users", {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            "ngrok-skip-browser-warning": "anyValue"
          },
          body: jsonData
        });

        if (response.ok) {
          // If account creation succeeds, call getToken to retrieve the token
          await this.getToken();
        } else {
          const data = await response.json();
          this.responseData = data.detail;
          this.loginFailed = true;
          this.errorMessage = "Invalid email or password. Please try again."; 
          this.showToast = true;
          setTimeout(() => { this.showToast = false; }, 3000); 
        }

      } catch (error) {
        console.error("Error posting data:", error);
        this.loginFailed = true;
        this.errorMessage = "Error connecting to server. Please try again later.";
        this.showToast = true;
        setTimeout(() => { this.showToast = false; }, 3000);
      }
    }
  }
};
</script>

<style scoped>

.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(255, 0, 0, 0.9);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 20;
  font-weight: bold;
}

/* Red border for invalid inputs */
.input-error {
  border: 2px solid red;
}

/* Error message styling */
.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
  position: absolute;
  left: 0;
  top: 100%;
}

.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-image: url('./pictures/book.jpeg'); /* Obraz tła */
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(250, 250, 250, 0.15); /* Jaśniejszy kolor szary */
  z-index: 1;
}

/* Stylizacja formularza logowania */
.form-container {
  position: relative;
  z-index: 2; /* Ustawienie formularza nad tłem */
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
  position: relative;
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

.signin-link {
  margin-top: 15px;
  font-size: 14px;
}

.signin-link a {
  color: #002f5b;
  text-decoration: none;
  font-weight: bold;
}

.signin-link a:hover {
  color:#004080;
}
</style>
