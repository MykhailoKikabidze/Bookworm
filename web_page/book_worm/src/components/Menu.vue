<template>
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

        <!-- Settings dropdown visible only if logged in -->
        <div class="settings-dropdown" v-if="isLoggedIn">
          <a href="#" class="settings-button">
            <i class="fas fa-cogs"></i> Settings
          </a>
          <div class="settings-menu">
            <form @submit.prevent="updateSettings">
              <div class="form-group">
                <label for="username">New Username</label>
                <input type="text" id="username" v-model="username" required />
              </div>
              <div class="form-group">
                <label for="email">New Email</label>
                <input type="email" id="email" v-model="email" required />
              </div>
              <button type="submit">Save Changes</button>
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
      searchQuery: '',
      isLoggedIn: false, // User login status
      username: '',
      email: ''
    };
  },
  methods: {
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
          this.isLoggedIn = false;
          // Add logout logic if necessary
        }
      } else {
        this.isLoggedIn = true;
        // Add login logic if necessary
      }
    },
    updateSettings() {
      alert(`Changes saved!\nUsername: ${this.username}\nEmail: ${this.email}`);
      // Add logic to save settings (e.g., update user profile)
    }
  },
  mounted() {
    this.typeText();
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
  flex-direction: column;
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


</style>
