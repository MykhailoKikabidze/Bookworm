<template>
  <div class="login-container">
    
    <div v-if="showToast" class="toast">
      {{ errorMessage }}
    </div>

    <div class="overlay"></div>
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
          <div class="password-container">
            <input
              :type="passwordVisible ? 'text' : 'password'"
              id="password"
              v-model="password"
              :class="{ 'input-error': !isPasswordValid && password.length > 0 }"
              required
            />
            <button type="button" class="toggle-password" @click="togglePasswordVisibility">
              <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span v-if="!isPasswordValid && password.length > 0" class="error-message">Password must be at least 8 characters.</span>
        </div>

        <div class="input-group">
          <label for="confirmPassword">Confirm Password</label>
          <div class="password-container">
            <input
              :type="confirmPasswordVisible ? 'text' : 'password'"
              id="confirmPassword"
              v-model="confirmPassword"
              :class="{ 'input-error': confirmPassword !== password && confirmPassword.length > 0 }"
              required
            />
            <button type="button" class="toggle-password" @click="toggleConfirmPasswordVisibility">
              <i :class="confirmPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span v-if="confirmPassword !== password && confirmPassword.length > 0" class="error-message">Passwords do not match.</span>
        </div>

        <button type="submit" :disabled="!isEmailValid || !isPasswordValid || password !== confirmPassword">Create</button>
      </form>

      <p class="signin-link">
        Already have an account? <router-link to="/sign_in">Sign in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import validator from 'validator';

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      email: '',
      loginFailed: false,
      errorMessage: "",
      passwordVisible: false, // To toggle password visibility
      confirmPasswordVisible: false, // To toggle confirm password visibility
      showToast: false,
    };
  },
  computed: {
    isEmailValid() {
      return validator.isEmail(this.email);
    },
    isPasswordValid() {
      return validator.isLength(this.password, { min: 8 });
    }
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    toggleConfirmPasswordVisibility() {
      this.confirmPasswordVisible = !this.confirmPasswordVisible;
    },
    async postData() {
      if (!this.isEmailValid || !this.isPasswordValid || this.password !== this.confirmPassword) {
        this.errorMessage = "Please correct your email or password, or ensure both passwords match.";
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

        const response = await fetch("https://8958-94-254-173-8.ngrok-free.app/users", {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
            "ngrok-skip-browser-warning": "anyValue"
          },
          body: jsonData
        });

        if (!response.ok) {
          const data = await response.json();
          this.errorMessage = "Error occurred while creating your account.";
          this.showToast = true;
          setTimeout(() => { this.showToast = false; }, 3000);
        } else {
          this.errorMessage = "Account created successfully!";
          this.showToast = true;
          setTimeout(() => { this.showToast = false; }, 3000);
        }

      } catch (error) {
        console.error("Error posting data:", error);
        this.errorMessage = "Error connecting to server. Please try again later.";
        this.showToast = true;
        setTimeout(() => { this.showToast = false; }, 3000);
      }
    }
  }
};
</script>

<style scoped>
.password-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

input {
  width: 100%;
  padding: 10px;
  padding-right: 35px; /* Adjusted space for the icon */
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  font-family: 'Georgia', serif;
  background-color: #f5f5f5;
  color: #2f2f2f;
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
  background-image: url('./pictures/book.jpeg'); /* Background image */
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
  background-color: rgba(250, 250, 250, 0.15); /* Lighter gray background */
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
  position: relative;
}

label {
  font-size: 17px;
  color: #002f5b;
  margin-bottom: 5px;
  display: block;
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
  color: #004080;
}
</style>
