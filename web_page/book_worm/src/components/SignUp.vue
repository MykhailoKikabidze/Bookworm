<template>
    <div class="login-container">
      <div>
        <img src="./pictures/books.jpg" class="image-log" />
      </div>
      <div class="form-container">
        <h1>Login</h1>
        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
  
      <p class="login-link">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
  
      <!-- <div class="image-container">
        <div class="light-overlay"></div>
        <img src="./pictures/books_log_in.jpg" class="image" alt="Login Background" />
      </div> -->
    </div>
  </template>
  
  <script>
  export default {
    name: 'SignUp',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      handleSubmit() {
        console.log('Logging in with', this.username, this.password);
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    opacity: 06;
    position: relative;
    color: white;
  }
  
  .form-container {
    position: relative;
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    width: 50vmax;
    height: 62vh;
  }
  
  h1 {
    margin-bottom: 8%;
  }
  
  .input-group {
    margin-bottom: 4vh;
  }
  
  label {
    display: block;
    margin-bottom: 3px;
  }
  
  input {
    width: 45%;
    padding: 15px;
    border: none;
    border-radius: 5px;
    background-color: rgba(255, 255, 255, 0.8);
  }
  
  button {
    width: 45%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #1ea490;
    color: white;
    font-size: 25px;
    margin-top: 5%;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .login-link {
    position: relative;
    z-index: 15;
    top: -7vh;
    text-align: center;
    font-size: 15px;
    color: rgba(255, 255, 255, 1); /* Lighter shade of white */
    background-color: rgba(0, 0, 0, 0.6);
    padding: 5px 10px;
    border-radius: 4px;
    font-weight: 300;
    opacity: 1;
  }
  
  .login-link a {
    color: #1ea490; /* Change this to your desired color */
    text-decoration: none; /* Removes the default underline */
  }
  
  .signup-link a:hover {
    color: #17a085; /* Optional: Hover effect with another shade */
  }
  
  
  .image-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 30%;
    overflow: hidden;
  }
  
  .image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .light-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    pointer-events: none;
  }
  
  .image-log {
    position: absolute;
    z-index: 11;
    width: 25vmax;
    border-radius: 8px;
    height: 62vh;
    overflow: hidden;
    object-fit: cover;
  }
  </style>
  