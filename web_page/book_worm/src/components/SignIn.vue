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
          <div class="password-wrapper">
            <input
              :type="passwordVisible ? 'text' : 'password'"
              id="password"
              v-model="password"
              required
            />
            <span class="eye-icon" @click="togglePasswordVisibility">
              <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>
        <button type="submit">Sign in</button>
      </form>
      <p class="login-link">
        Don't have an account? <router-link to="/login">Create account</router-link>
      </p>
    </div>
    <div v-if="showToast" :class="['toast', toastType]">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignIp',
  data() {
    return {
      username: '',
      password: '',
      passwordVisible: false, // Add password visibility toggle state
      link_backend: "https://abe4-188-146-152-16.ngrok-free.app",
      moder: false,
      responseData: "",
      showToast: false,  
      toastMessage: '', 
      toastType: 'success' 
    };
  },
  methods: {
    async handleSubmit() {
      await this.getToken();
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
          this.showToastMessage('Error logging in: ' + this.responseData, 'error');

        } else {
          const data = await response.json();
          localStorage.setItem('authToken', data.access_token);

          await this.authorization();
        }
      } catch (error) {
        console.error("Error fetching token:", error);
        this.showToastMessage('Network error. Please try again.', 'error');

      }
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
          this.showToastMessage('Error authorizing user: ' + this.responseData, 'error');

        } else {
          const data = await response.json();
          this.moder = data.is_moder;
          this.showToastMessage('Successfully logged in!', 'success');

          this.$router.push('/'); 
        }
      } catch (error) {
        console.error("Error during authorization:", error);
        this.showToastMessage('Network error. Please try again.', 'error');

      }
    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible; 
    },
    showToastMessage(message, type) {
    this.toastMessage = message;
    this.toastType = type;
    this.showToast = true;

    setTimeout(() => {
      this.showToast = false;
    }, 3000);
  }
  }
};
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease, visibility 0s 0.5s;
  z-index: 9999;
}

.toast.show {
  opacity: 1;
  visibility: visible;
  transition: opacity 0.5s ease, visibility 0s 0s;
}

.toast.success {
  background-color: #4caf50; /* Green for success */
}

.toast.error {
  background-color: #f44336; /* Red for error */
}
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
  background-color: rgba(250, 250, 250, 0.15); /* Lighter gray color */
  z-index: 1;
}

.form-container {
  position: relative;
  z-index: 2; /* Set form above background */
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

.password-wrapper {
  position: relative;
}

.eye-icon {
  position: absolute;
  right: 14px;
  top: 7px;
  cursor: pointer;
  font-size: 20px;
  color: #002f5b;
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
  color:#004080;
}
</style>
