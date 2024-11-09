<template>
  <div id="app">
    <!-- Always show the header -->
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
        <router-link to="/sign_in"><i class="fas fa-sign-in-alt"></i> Log In</router-link>
      </nav>
    </header>

    <!-- Conditionally render the banner only on 'Home' route -->
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
      fullText: 'A SOFA, A GOOD BOOK, AND YOU.', // Full text for typing effect
      displayedText: '', // Text to be displayed
      typingIndex: 0, // Index to track typing
      typingSpeed: 100, // Speed of typing effect
      searchQuery: '' // Search query
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

/* Ensure the body and html are full width */
html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden; /* Prevent horizontal scrolling */
}

/* Fullscreen banner styling */
section.banner {
  background-image: url('/src/components/icons/book-sofa.jpg');
  background-size: cover; /* Ensure the background image covers the whole section */
  background-position: center center; /* Center the background image */
  width: 100vw; /* Use full width */
  height: 100vh; /* Ensure it takes full screen height */
  display: flex; /* Use flexbox */
  justify-content: center; /* Center contents horizontally */
  align-items: center; /* Center contents vertically */
  margin: 0; /* Remove margins */
  z-index: 1;
}

.banner-content {
  text-align: center;
  color: #002f5b; /* Dark blue color */
}

/* Font Import */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

.banner-content h1 {
  font-family: 'Playfair Display', serif; /* Updated font */
  font-size: 77px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  margin-bottom: 0;
  text-transform: uppercase;
  letter-spacing: 2px;
  white-space: pre-wrap; /* Allows for line breaks in the text */
}

/* Navbar Styling */
.navbar {
  display: flex;
  justify-content: space-between; /* Adjust for even spacing */
  align-items: center;
  flex-wrap: wrap; /* Allow navbar items to wrap */
  padding: 15px 40px;
}

.navbar .logo {
  font-size: 26px;
  font-weight: bold;
  color: #002f5b; /* Dark blue for contrast */
  text-decoration: none; /* Remove underline */
}

.navbar nav {
  display: flex; /* Use flexbox for nav items */
  position: relative; /* Ensure relative positioning for dropdown */
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
  margin-right: 8px; /* Space between icon and text */
  font-size: 18px; /* Adjust icon size */
  vertical-align: middle; /* Align icon with text */
}

/* Dropdown styles */
.dropdown {
  position: relative; /* Relative positioning for the dropdown */
}

/* Dropdown toggle - icon and text alignment */
.dropdown-toggle {
  display: flex;
  align-items: center; /* Align icon and text vertically */
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Icon styling */
.dropdown-toggle i {
  margin-right: 8px; /* Space between icon and text */
  font-size: 20px; /* Icon size */
}

/* Adjust the size of the text if needed */
.dropdown-toggle {
  font-size: 18px;
}

.dropdown:hover .dropdown-menu {
  display: block; /* Show dropdown on hover */
}

.dropdown-menu {
  display: none; /* Hide the dropdown by default */
  position: absolute;
  top: 100%; /* Position below the toggle */
  left: 0; /* Align to the left edge */
  right: 0; /* Ensure it doesn’t overflow */
  background-color: white; /* White background */
  border: 1px solid #002f5b; /* Border color */
  border-radius: 8px; /* Rounded corners */
  z-index: 10; /* Ensure it appears above other content */
  width: 180px; /* Set width for more space */
  max-height: 300px; /* Limit max height */
  overflow-y: auto; /* Add scroll if the menu is too long */
}

.dropdown-menu a {
  display: flex; /* Use flexbox to align icon and text */
  align-items: center; /* Center items vertically */
  justify-content: flex-start; /* Align items to the left */
  padding: 10px 10px; /* Add slight padding */
  color: #002f5b; /* Text color */
  text-decoration: none; /* Remove text underline */
  transition: background-color 0.3s ease;
  text-align: left;
  overflow: hidden;
  white-space: nowrap; /* Prevent text wrapping */
  text-overflow: ellipsis; /* Add ellipsis for overflow text */
}

.dropdown-menu a i {
  margin-right: 5px; /* Space between icon and text */
  font-size: 18px; /* Icon size */
}

/* Navbar link hover effect */
.navbar nav a:hover {
  color: #ffffff;
  animation: blink 0.8s ease-in-out infinite; /* Add blinking animation */
}

.dropdown-menu a:hover {
  background-color: rgba(235, 184, 172, 0.5); /* Light color on hover */
}

/* Pseudo-element for rounded background */
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

/* Search Bar Styling */
.search-bar {
  display: flex;
  justify-content: center;
  margin-top: 5vh;
}

.search-bar input {
  padding: 15px 20px;
  font-size: 1.2rem;
  border: 2px hsla(55, 63%, 68%, 0.418);
  border-radius: 30px 0 0 30px;
  outline: none;
  width: 40vw;
  transition: border-color 0.3s ease, background-color 0.3s ease;
  background-color: rgba(255, 255, 255, 0.8);
}

.search-bar input:focus {
  border-color: #ebb8ac;
  background-color: rgba(255, 255, 255, 1);
}

.search-bar button {
  padding: 15px 30px;
  background-color: hsla(55, 63%, 68%, 0.418);
  color: #ffffff;
  border: none;
  border-radius: 0 30px 30px 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 1.2rem;
}

.search-bar button:hover {
  background-color: rgba(235, 184, 172, 0.8);
}

@media (max-width: 768px) {
  .search-bar input {
    width: 70vw;
  }

  .search-bar button {
    font-size: 1rem;
  }

  .navbar nav a {
    font-size: 16px;
    margin-left: 20px;
  }

  .dropdown-menu {
    width: 100%; /* Ensure dropdown is full width on small screens */
  }
}

</style>
