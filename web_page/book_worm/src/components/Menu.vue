<template>
  <div >{{ check() }}</div>
  <div id="app">
    <div class="toast" :class="['toast', notificationClass, { show: showNotification }]">
    {{ message }}
  </div>    <header class="navbar">
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

        <!-- Settings dropdown visible only if logged in -->
        <div class="settings-dropdown" v-if="isLoggedIn">
      <a href="#" class="settings-button">
        <i class="fas fa-cogs"></i> Settings
      </a>
      <div class="settings-menu">
        <form @submit.prevent="updateSettings">
          <div class="form-group">
            <label for="username">New Username</label>
            <input type="text" id="username" v-model="newUsername" required />
            <button type="button" @click="changeName()">Save Username</button>
          </div>
          <div class="form-group">
  <label for="password">New Password</label>
  <div class="password-wrapper">
    <input
      :type="passwordVisible ? 'text' : 'password'"
      id="password"
      v-model="newPassword"
      required
    />
    <span class="eye-icon" @click="togglePasswordVisibility">
      <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
    </span>
  </div>
  <button type="button" @click="changePassword()">Save Password</button>
</div>
          <button type="button" class="delete-account-button" @click="deleteAccount()">Delete Account</button>
        </form>
          </div>
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
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      fullText: 'A SOFA, A GOOD BOOK, AND YOU.',
      displayedText: '',
      typingIndex: 0,
      typingSpeed: 100,
      link_backend: "https://abe4-188-146-152-16.ngrok-free.app",
      searchQuery: '',
      isLoggedIn: false, // User login status
      username: '',
      message: '',
      showNotification: false,  // New property to show/hide notification
      notificationClass: '',  
      password: '',
      passwordVisible: false 
    };
  },
  computed: {
    messageClass() {
      return this.message.includes('successfully') ? 'success-message' : 'error-message';
    },
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    async changeName() {
      try {
        const params = new URLSearchParams();
        params.append("new_username", this.newUsername);

        const url = `${this.link_backend}/users/name?${params.toString()}`;

        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          }
        });

        if (response.ok) {
          this.message = 'Username successfully changed!';
          this.notificationClass = 'success-toast';  // Class for success
        } else {
          const data = await response.json();
          this.message = data.detail || 'Error changing username.';
          this.notificationClass = 'error-toast';  // Class for error
        }
      } catch (error) {
        this.message = 'Error changing username.';
        this.notificationClass = 'error-toast';  // Class for error
      }
      this.showNotificationMessage();
    },
    async changePassword() {
      try {
        const params = new URLSearchParams();
        params.append("new_password", this.newPassword);

        const url = `${this.link_backend}/users/password?${params.toString()}`;

        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          },
        });

      if (response.ok) {
          this.message = 'Password successfully changed!';
          this.notificationClass = 'success-toast';  // Class for success
          this.newPassword = '';  
        } else {
          const data = await response.json();
          this.message = data.detail || 'Error changing password.';
          this.notificationClass = 'error-toast';  // Class for error
        }
      } catch (error) {
        this.message = 'Error changing password.';
        this.notificationClass = 'error-toast';  // Class for error
      }
      this.showNotificationMessage();
    },

    async deleteAccount() {
      const confirmation = confirm("Are you sure you want to delete your account? This action is irreversible.");
      if (!confirmation) return;
      try {
        const response = await fetch(this.link_backend + "/users", {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": "Bearer " + localStorage.getItem('authToken'),
            "ngrok-skip-browser-warning": "anyValue"
          }
        });

        if (response.ok) {
          localStorage.removeItem("authToken");
          window.location.reload();
          this.message = 'Account deleted successfully.';
          this.notificationClass = 'success-toast';  // Class for success
        } else {
          const data = await response.json();
          this.message = data.detail || 'Error deleting account.';
          this.notificationClass = 'error-toast';  // Class for error
        }
      } catch (error) {
        console.error("Error posting data:", error);
        this.message = 'Error deleting account.';
        this.notificationClass = 'error-toast';  // Class for error

      }
      this.showNotificationMessage();
    },
    typeText() {
      if (this.typingIndex < this.fullText.length) {
        this.displayedText += this.fullText.charAt(this.typingIndex);
        this.typingIndex++;
        setTimeout(this.typeText, this.typingSpeed);
      }
    },
    performSearch() {
      console.log(`Searching for: ${this.searchQuery}`);
      // Implement your actual search functionality here (e.g., API call)
    },
    toggleLogin() {
      if (this.isLoggedIn) {
        const confirmation = confirm("Are you sure you want to log out?");
        if (confirmation) {
          // Clear the token from localStorage
          localStorage.removeItem("authToken");
          this.isLoggedIn = false;
        }
      } else {
        // Navigate to the login page if not logged in
        this.$router.push('/sign_in');
      }
    },
    updateSettings() {
      alert(`Changes saved!\nUsername: ${this.username}\nPassword: ${this.password}`);
      // Add logic to save settings (e.g., update user profile)
    }
    ,check()
    {
      const token = localStorage.getItem("authToken");
    if (token) {
      this.isLoggedIn = true; // Set the user as logged in if a token is present
    } else {
      this.isLoggedIn = false; // Ensure logged-out state if no token
    }
    this.typeText();
    },

    showNotificationMessage() {
    this.showNotification = true; // Show the toast
    setTimeout(() => {
      this.showNotification = false; // Hide the toast after 3 seconds
      this.message = ''; // Clear the message
    }, 3000); // Adjust the duration (in milliseconds) as desired
  },
},
  mounted() {
  }
};
</script>


<style>
/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
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


.toast {
  position: fixed;
  bottom: 20px; /* distance from the bottom of the viewport */
  left: 50%; /* centers the toast horizontally */
  transform: translateX(-50%); /* adjust it so that it's centered */
  background-color: #333; /* dark background */
  color: white;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  opacity: 0; /* Initially invisible */
  visibility: hidden; /* Hidden by default */
  transition: opacity 0.5s ease, visibility 0s 0.5s; /* Smooth fade-out */
  z-index: 9999; /* Make sure the toast is on top */
}

.toast.show {
  opacity: 1; /* Make the toast visible */
  visibility: visible; /* Ensure it's visible */
  transition: opacity 0.5s ease, visibility 0s 0s; /* Smooth fade-in */
}

.success-toast {
  background-color: #4caf50; /* Green for success */
}

.error-toast {
  background-color: #f44336; /* Red for errors */
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
  flex-wrap: wrap;
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
  position: relative;
  /* flex-direction: column; */
}

.navbar nav a {
  position: relative;
  margin-left: 30px;
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

/* Settings Dropdown Styles */
.settings-dropdown {
  position: relative;
}

.settings-button {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 20px;
}

.settings-button i {
  margin-right: 8px;
}

.settings-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #002f5b;
  border-radius: 8px;
  z-index: 10;
  width: 250px;
  padding: 8px 12px; /* Reduced padding */
  font-family: 'Playfair Display', serif; /* Matching font with your site */
  font-size: 16px; /* Adjust the font size to match your site */
}

.settings-dropdown:hover .settings-menu {
  display: block;
}

.settings-menu .form-group {
  margin-bottom: 10px;
}



.settings-menu input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.settings-menu button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  background-color: #002f5b;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.settings-menu button:hover {
  background-color: #335f8d;
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
  gap: 0px; /* Reduce spacing between items */
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
    font-size: 1.1em; /* Minimize font size for very small screens */
    padding: 6px 6px;
    border-radius: 2px;
  }
}

</style>
