<template>
  <div class="login-container">
    <div class="background-image"></div>
    <div class="overlay"></div>
    <div class="form-container">
      <h1>Sign in</h1>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="email">Email</label>
          <div class="password-wrapper">
          <input type="text" id="email" v-model="email" 
          :class="{ 'input-error': !isEmailValid && email.length > 0 }"
          required />
          <span v-if="!isEmailValid && email.length > 0" class="error-message">Please enter a valid email.</span>
        </div>
      </div>
        <div class="input-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input
              :type="passwordVisible ? 'text' : 'password'"
              id="password"
              v-model="password"
              :class="{ 'input-error': !isPasswordValid && password.length > 0 }"
              required
            />
            <span v-if="!isPasswordValid && password.length > 0" class="error-message">Password must be at least 8 characters.</span>
            <span class="eye-icon" @click="togglePasswordVisibility">
              <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>
        <button type="submit" :disabled="!isEmailValid || !isPasswordValid">Sign in</button>
      </form>
      <p class="login-link">
        Don't have an account? <router-link to="/login">Create account</router-link>
      </p>
    </div>
    <div v-if="showToast" :class="['toast', toastType]">
      {{ toastMessage }}
    </div>

    <Toast ref="toastRef" />

  </div>
</template>

<script>
import validator from 'validator';
import Toast from './Toast.vue';

export default {
  name: 'SignIp',
  data() {
    return {
      email: '',
      password: '',
      passwordVisible: false, // Add password visibility toggle state
      moder: false,
      responseData: "",
    };
  },
  components: {
    Toast, 
  },
  computed:{
    isEmailValid() {
      return validator.isEmail(this.email);
    },
    isPasswordValid() {
      return validator.isLength(this.password, { min: 8 });
    }
  },
  methods: {

    showCustomError() {
      const toastRef = this.$refs.toastRef;
      toastRef.message = 'Custom error message from parent!';
      toastRef.notificationClass = 'error-toast'; // Set as error
      toastRef.showNotificationMessage(); // Trigger toast
    },
    async handleSubmit() {
      await this.getToken();
    },
    async getToken() {
      const toastRef = this.$refs.toastRef; // Reference the toast

      if (!this.isEmailValid || !this.isPasswordValid ) {
        this.errorMessage = "Please correct your email or password.";
        this.showToast = true;
        setTimeout(() => { this.showToast = false; }, 3000);
        return;
      }

      const params = new URLSearchParams();
      params.append("username", this.email);
      params.append("password", this.password);

      try {
        const response = await fetch(this.$link_backend + "/token", {
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
          toastRef.message = 'Error logging in: ' + this.responseData;
          toastRef.notificationClass = 'error-toast';  // Class for error

        } else {
          const data = await response.json();
          localStorage.setItem('authToken', data.access_token);
          toastRef.message ='Successfully';
          toastRef.notificationClass = 'success-toast';  // Class for success
          await this.authorization();
        }
      } catch (error) {
        console.error("Error fetching token:", error);
        toastRef.message = 'Network error. Please try again.'+error;
        toastRef.notificationClass = 'error-toast';  // Class for error
      }
      this.$refs.toastRef.showNotificationMessage();  
    },
    async authorization() {
      const toastRef = this.$refs.toastRef; // Reference the toast
      try {
        const response = await fetch(this.$link_backend + "/users/me", {
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
          toastRef.message ='Error authorizing user: ' + this.responseData;
          toastRef.notificationClass = 'error-toast';  // Class for error

        } else {
          const data = await response.json();
          this.moder = data.is_moder;
          toastRef.message ='Successfully logged in!';
          toastRef.notificationClass = 'success-toast';  // Class for success
          localStorage.setItem('username', data.name);
          localStorage.setItem('moder', data.is_moder);
          this.$router.push('/'); 
        }
      } catch (error) {
        console.error("Error during authorization:", error);
        toastRef.message ='Network error. Please try again.'+error;
        toastRef.notificationClass = 'error-toast';  // Class for error

      }
      this.$refs.toastRef.showNotificationMessage();  

    },
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible; 
    },
  }
};
</script>

<style scoped>
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
