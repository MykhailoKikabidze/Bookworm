<template>
  <div class="login-container">
    <div class="overlay"></div> <!-- Warstwa półprzezroczysta nad obrazem tła -->
    <div class="form-container">
      <h1>Login</h1>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="email">Email</label>
          <input type="text" id="email" v-model="email" required />
        </div>
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
      <p class="signup-link">
        Don't have an account? <router-link to="/sign_up">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
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
/* Ustawienie pełnoekranowego obrazu tła */
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

.signup-link {
  margin-top: 15px;
  font-size: 14px;
}

.signup-link a {
  color: #002f5b;
  text-decoration: none;
  font-weight: bold;
}

.signup-link a:hover {
  color:#004080;
}
</style>
