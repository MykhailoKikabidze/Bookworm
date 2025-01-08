<template>
  <div>{{ check() }}</div>
  <div id="app">
    <header class="navbar">
      <router-link to="/" class="logo">BOOK WORM</router-link>
      <nav>
        <router-link to="/library"><i class="fas fa-book"></i> Library</router-link>
        <div class="dropdown">
          <a href="#" class="dropdown-toggle">
            <i class="fas fa-bookmark"></i> My Library
          </a>
          <div class="dropdown-menu">
            <router-link to="/favorites"><i class="fas fa-star"></i> Favorites</router-link>
            <router-link to="/reading"><i class="fas fa-book-reader"></i> Reading</router-link>
            <router-link to="/will-read"><i class="fas fa-plus-square"></i> Will Read</router-link>
            <router-link to="/had-read"><i class="fas fa-check-square"></i> Had Read</router-link>
          </div>
        </div>
        <router-link to="/topics"><i class="fas fa-tag"></i> Topics</router-link>
        <router-link to="/contact"><i class="fas fa-envelope"></i> Contact</router-link>

        <div v-if="isModer" class="add-button-container">
  <!-- Modern Styled Button with Icon -->
  <router-link to="/add" class="add-button"><i class="fas fa-plus"></i> Add</router-link>
</div>

        <!-- Settings dropdown visible only if logged in -->
        <div class="settings-dropdown" v-if="isLoggedIn">
  <router-link to="/settings" class="settings-button">
    <i class="fas fa-user"></i> <span class="username">{{ username }}</span>
  </router-link>
</div>



        <!-- Log In / Log Out Button -->
        <router-link :to="isLoggedIn ? '/' : '/sign_in'" @click="toggleLogin">
          <i class="fas fa-sign-in-alt"></i> {{ isLoggedIn ? 'Log Out' : 'Log In' }}
        </router-link>
      </nav>
    </header>

    <section v-if="$route.name === 'Home'" class="banner">
    <div class="banner-content">
      <h1>{{ displayedText.split(',').join(',\n') }}</h1>
      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="Search for books..." />
        <button @click="performSearch">Search</button>
      </div>
      <!-- Komunikat o błędzie -->
      <div v-if="searchError" class="custom-alert">
        <span>Please enter a search query.</span>
      </div>
    </div>
  </section>
    <Toast ref="toastRef" />
  </div>
</template>

<script>
import validator from 'validator';
import Toast from './Toast.vue';

export default {
  name: 'App',
  data() {
    return {
      fullText: 'A SOFA, A GOOD BOOK, AND YOU.',
      displayedText: '',
      typingIndex: 0,
      typingSpeed: 100,
      searchQuery: '',
      isModer: false,
      isLoggedIn: false,
      username: localStorage.getItem('username') || 'Guest', // Initial value from localStorage
      password: '',
      confirmPassword: '',
      passwordVisible: false,
      newUsername: '',
      searchQuery: '',
      searchError: false, // Flaga do pokazania komunikatu błędu
    };
  },
  created() {
    window.addEventListener('storage', this.syncUsernameFromLocalStorage); // Sync when localStorage is updated
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.syncUsernameFromLocalStorage); // Clean up listener
  },
  components: {
    Toast,
  },
  computed: {
    isPasswordValid() {
      return validator.isLength(this.password, { min: 8 });
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('username');  // Remove username from localStorage
      this.username = '';  // Reset username in component state
    },

    updateUsername(newUsername) {
      this.username = newUsername;  // Update username in component state
      localStorage.setItem('username', newUsername);  // Save username to localStorage
    },

    login() {
      const newUsername = 'NowaPoczta@przyklad.com';  // New username example
      this.updateUsername(newUsername);  // Update username in component and localStorage
    },

    showCustomError() {
      const toastRef = this.$refs.toastRef;
      toastRef.message = 'Custom error message from parent!';
      toastRef.notificationClass = 'error-toast';
      toastRef.showNotificationMessage();
    },

    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },

    async changeName() {
      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("new_username", this.newUsername);
      const url = `${this.$link_backend}/users/name?${params.toString()}`;

      try {
        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          toastRef.message = 'Username successfully changed!';
          toastRef.notificationClass = 'success-toast';
        } else {
          const data = await response.json();
          toastRef.message = data.detail || 'Error changing username.';
          toastRef.notificationClass = 'error-toast';
        }
      } catch (error) {
        toastRef.message = 'Error changing username.';
        toastRef.notificationClass = 'error-toast';
      }
      this.username = ''; // Clear the input
      this.$refs.toastRef.showNotificationMessage();
    },

    async changePassword() {
      if (!this.isPasswordValid || this.confirmPassword !== this.password) {
        this.showCustomError();
        return;
      }

      const toastRef = this.$refs.toastRef;
      const params = new URLSearchParams();
      params.append("new_password", this.password);

      try {
        const url = `${this.$link_backend}/users/password?${params.toString()}`;

        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          toastRef.message = 'Password successfully changed!';
          toastRef.notificationClass = 'success-toast';
        } else {
          const data = await response.json();
          toastRef.message = data.detail || 'Error changing password.';
          toastRef.notificationClass = 'error-toast';
        }
      } catch (error) {
        toastRef.message = 'Error changing password.';
        toastRef.notificationClass = 'error-toast';
      }
      this.password = '';
      this.confirmPassword = '';
      this.$refs.toastRef.showNotificationMessage();
    },

    async deleteAccount() {
      const confirmation = confirm("Are you sure you want to delete your account? This action is irreversible.");
      if (!confirmation) return;

      const toastRef = this.$refs.toastRef;
      try {
        const response = await fetch(this.$link_backend + "/users", {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          localStorage.removeItem("authToken");
          localStorage.removeItem('username');
          window.location.reload();
          toastRef.message = 'Account deleted successfully.';
          toastRef.notificationClass = 'success-toast';
        } else {
          const data = await response.json();
          toastRef.message = data.detail || 'Error deleting account.';
          toastRef.notificationClass = 'error-toast';
        }
      } catch (error) {
        toastRef.message = 'Error deleting account.';
        toastRef.notificationClass = 'error-toast';
      }
      this.$refs.toastRef.showNotificationMessage();
    },

    printText() {
      console.log(this.fullText);
    },

    typeText() {
      if (this.typingIndex < this.fullText.length) {
        this.displayedText += this.fullText.charAt(this.typingIndex);
        this.typingIndex++;
        setTimeout(this.typeText, this.typingSpeed);
      }
    },
  

    performSearch() {
      if (this.searchQuery.trim() === '') {
        this.searchError = true;
        // Po 3 sekundach ukrywamy komunikat
        setTimeout(() => {
          this.searchError = false;
        }, 3000);
      } else {
        this.$router.push({ name: 'Search', query: { query: this.searchQuery } });
        this.searchError = false; // Ukryj komunikat po prawidłowym wyszukaniu
      }
    },

    toggleLogin() {
      if (this.isLoggedIn) {
        const confirmation = confirm("Are you sure you want to log out?");
        if (confirmation) {
          localStorage.removeItem("authToken");
          this.isLoggedIn = false;
          localStorage.removeItem("username");  // Remove username from localStorage
          localStorage.removeItem("moder"); 
          this.isModer=false;
        }
      } else {
        this.isLoggedIn = true;
        this.isModer=true;
      }
    },

    check() {
      const token = localStorage.getItem("authToken");
      if (token) {
        this.isLoggedIn = true;
      } else {
        this.isLoggedIn = false;
      }
    
      if(localStorage.getItem("moder")=="true"){
        this.isModer=true;
      }
      else this.isModer=false;
      this.syncUsernameFromLocalStorage();

    },

    // Sync username whenever localStorage is updated
    syncUsernameFromLocalStorage() {
      const storedUsername = localStorage.getItem('username');
      if (storedUsername && storedUsername !== this.username) {
        this.username = storedUsername;
      }
    },
  },
  mounted() {
  this.printText();
  this.typeText(); // Ensure the username is correct when mounted
},

  watch: {
    // // Watch username changes and update localStorage
    // username(newValue) {
    //   localStorage.setItem('username', newValue);
    // }
  }
};
</script>



<style>
.custom-alert {
  background-color: #d7d7d7af;
  color: #393939;
  padding: 15px;
  margin-top: 20px;
  border: 1px solid #ffffff;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
}

.custom-alert span {
  margin-right: 10px;
}

/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
  position: absolute;
  left: 0;
  top: 100%;
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

html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

/* Fullscreen banner styling */
section.banner {
  background-image: url('/src/components/icons/book-sofa.jpg');
  background-size: cover;
  background-position: center center;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  z-index: 1;
}

.banner-content {
  text-align: center;
  color: #002f5b;
}

/* Font Import */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

.banner-content h1 {
  font-family: 'Playfair Display', serif;
  font-size: 77px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  margin-bottom: 0;
  text-transform: uppercase;
  letter-spacing: 2px;
  white-space: pre-wrap;
}

/* Navbar Styling */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap; /* Ensure navbar items do not wrap */
  padding: 15px 40px;
}

.navbar .logo {
  font-size: 26px;
  font-weight: bold;
  color: #002f5b;
  text-decoration: none;
}

.navbar nav {
  display: flex;
  gap: 15px; /* Space between navbar items */
}

.navbar nav a {
  position: relative;
  text-decoration: none;
  font-size: 18px;
  color: #002f5b;
  padding: 10px 15px;
  border-radius: 20px;
  transition: color 0.3s ease;
}

.navbar nav a i {
  margin-right: 8px;
  font-size: 18px;
  vertical-align: middle;
}

.dropdown {
  position: relative;
}

.dropdown-toggle {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.dropdown-toggle i {
  margin-right: 8px;
  font-size: 20px;
}

.settings-dropdown {
  margin-top: 10px; /* Adds space above the button */
}

.dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #002f5b;
  border-radius: 8px;
  z-index: 10;
  width: 180px;
  max-height: 300px;
  overflow-y: auto;
}

.dropdown-menu a {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 10px 10px;
  color: #002f5b;
  text-decoration: none;
  transition: background-color 0.3s ease;
  text-align: left;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.dropdown-menu a i {
  margin-right: 5px;
  font-size: 18px;
}

.navbar nav a:hover {
  color: #ffffff;
}

.dropdown-menu a:hover {
  background-color: rgba(235, 184, 172, 0.5);
}

.navbar nav a::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background-color: rgba(235, 184, 172, 0.5);
  border-radius: 20px;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.3s ease;
  z-index: -1;
}

.navbar nav a:hover::before {
  transform: translate(-50%, -50%) scale(1);
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.search-bar input {
  width: 300px;
  height: 40px;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 20px;
  margin-right: 10px;
}

.search-bar button {
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background-color: #002f5b;
  color: white;
  cursor: pointer;
}

.search-bar button:hover {
  background-color: #335f8d;
}

/* Font size scaling for the entire page */
html {
  font-size: 100%;
}

@media (max-width: 1200px) {
  html {
    font-size: 90%;
  }
}

@media (max-width: 992px) {
  html {
    font-size: 80%;
  }
}

@media (max-width: 768px) {
  html {
    font-size: 70%;
  }
}

@media (max-width: 576px) {
  html {
    font-size: 60%;
  }
}

/* Navbar Styling */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px; /* Reduce padding for smaller screens */
}

.navbar nav {
  display: flex;
  gap: 10px; /* Slightly reduce spacing between items */
  justify-content: center; /* Center navbar items */
}

.navbar nav a,
.navbar .settings-button {
  transition: font-size 0.3s ease, border-radius 0.3s ease; /* Add transition for border-radius */
}

/* Hover effect on navbar items */
.navbar nav a:hover,
.navbar .settings-button:hover {
  border-radius: 15px; /* Increased border-radius for a more rounded effect */
}

@media (max-width: 992px) {
  .navbar nav a:hover,
  .navbar .settings-button:hover {
    border-radius: 13px; /* Slightly smaller radius on medium screens */
  }
}

@media (max-width: 768px) {
  .navbar nav a,
  .navbar .settings-button {
    font-size: 1.2em; /* Further reduce font size on smaller screens */
    padding: 7px 3px;
    border-radius: 5px; /* Add border-radius to create rounded corners */
  }
}

@media (max-width: 576px) {
  .navbar nav a,
  .navbar .settings-button {
    font-size: 1.2em; /* Minimize font size for very small screens */
    padding: 7px 2px; /* Adjust padding for small screens */
    border-radius: 10px; /* Ensure border-radius is consistent */
    outline: none; /* Remove focus outline */
    border: none; /* Remove border if any */
  }

  
}

.fas.fa-cogs {
  font-weight: bold;  /* Ustawienie grubości dla ikony */
}

.username {
  font-weight: bold;  /* Ustawienie grubości dla tekstu użytkownika */
}


.add-button-container {
  display: flex; /* Aby zapewnić kontrolowanie położenia elementów wewnętrznych */
  justify-content: center; /* Centrujemy przycisk w poziomie */
  margin-top: 1px; /* Zwiększamy odległość od góry, dostosuj w zależności od potrzeb */
}




</style>
