<template>
    <div id="app">
      <!-- Always show the header -->
      <header class="navbar">
  <router-link to="/" class="logo">BOOK WORM</router-link>
  <nav>
    <router-link to="/library"><i class="fas fa-book"></i> Library</router-link>
    <div class="dropdown">
      <a href="#" class="dropdown-toggle"><i class="fas fa-user-book"></i> My Library</a>
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
    background-position: center; /* Center the background image */
    width: 100vw; /* Use full width */
    height: 80vh; /* Set the height as desired */
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
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.903); /* Slightly transparent white */
    border-bottom: 2px solid #002f5b; /* Dark blue border */
    z-index: 10;
  }
  
 .navbar .logo {
    font-size: 26px;
    font-weight: bold;
    color: #002f5b; /* Dark blue for contrast */
    text-decoration: none; /* Usuwa podkreślenie */
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
  
  .dropdown-toggle {
    cursor: pointer; /* Change cursor to pointer for better UX */
    padding: 10px 15px; /* Add padding for better clickable area */
    border-radius: 20px; /* Rounded corners for the dropdown toggle */
    line-height: 40px; /* Adjust this value to match the navbar items */
    transition: background-color 0.3s ease, color 0.3s ease; /* Transition for background and text color */
  }
  
  .dropdown:hover .dropdown-menu {
    display: block; /* Show dropdown on hover */
  }
  
  .dropdown-menu {
    display: none; /* Hide the dropdown by default */
    position: absolute;
    top: 100%; /* Position below the toggle */
    left: 0; /* Align to the left edge */
    right: 100px; /* Adjust this as necessary */
    background-color: white; /* White background */
    border: 1px solid #002f5b; /* Border color */
    border-radius: 8px; /* Rounded corners */
    z-index: 10; /* Ensure it appears above other content */
    width: 180px; /* Set width for more space */
  }
  
  .dropdown-menu a {
      display: flex; /* Use flexbox to align icon and text */
      align-items: center; /* Center items vertically */
      justify-content: flex-start; /* Align items to the left */
      padding: 10px 10px; /* Add slight padding, adjust as needed */
      color: #002f5b; /* Text color */
      text-decoration: none; /* Remove text underline */
      transition: background-color 0.3s ease; /* Smooth background color transition */
      text-align: left; /* Left align the text */
      overflow: hidden; /* Hide overflow text */
      white-space: nowrap; /* Prevent text wrapping */
      text-overflow: ellipsis; /* Add ellipsis for overflow text */
  }
  
  .dropdown-menu a i {
      margin-right: 5px; /* Space between icon and text */
      font-size: 18px; /* Icon size */
  }
  
  
  /* Pseudo-element dla animacji migania */
  @keyframes blink {
    0%, 100% {
      background-color: rgba(235, 184, 172, 0.5); /* Przezroczysty różowy */
    }
    50% {
      background-color: rgba(235, 184, 172, 1); /* Pełny różowy */
    }
  }
  
  /* Navbar link styles */
  .navbar nav a:hover {
    color: #ffffff; /* Zmień kolor tekstu na biały na hover */
    animation: blink 0.8s ease-in-out infinite; /* Dodaj animację migania */
  }
  
  /* Pozostałe style nawigacji */
  .navbar nav a {
    position: relative;
    margin-left: 30px;
    text-decoration: none;
    font-size: 18px;
    color: #002f5b;
    padding: 10px 15px;
    border-radius: 20px;
    transition: color 0.3s ease; /* Tylko zmiana koloru tekstu */
  }
  
  
  .dropdown-menu a:hover {
    background-color: rgba(235, 184, 172, 0.5); /* Light color on hover */
  }
  
  /* Pseudo-element for rounded background */
  .navbar nav a::before {
    content: ""; /* Empty content for the pseudo-element */
    position: absolute;
    top: 50%; /* Center vertically */
    left: 50%; /* Center horizontally */
    width: 100%; /* Full width of the link */
    height: 100%; /* Full height of the link */
    background-color: rgba(235, 184, 172, 0.5); /* Background color with opacity */
    border-radius: 20px; /* Rounded corners */
    transform: translate(-50%, -50%) scale(0); /* Center and scale down */
    transition: transform 0.3s ease; /* Smooth transition for scale */
    z-index: -1; /* Send behind the text */
  }
  
  /* Hover styles */
  .navbar nav a:hover {
    color: #ffffff; /* Change text color on hover */
  }
  
  .navbar nav a:hover::before {
    transform: translate(-50%, -50%) scale(1); /* Scale up on hover */
  }
  
  /* Responsive Styling */
  @media (max-width: 768px) {
    .navbar .logo {
      font-size: 22px; /* Adjust logo size for smaller screens */
    }
  
    .navbar nav a {
      font-size: 16px;
      margin-left: 15px; /* Decrease margin for smaller screens */
    }
  }
  
  /* Search Bar Styling */
  .search-bar {
    display: flex;
    justify-content: center;
    margin-top: 30px; /* Add more margin above the search bar */
  }
  
  .search-bar input {
    padding: 15px 20px; /* Increased padding for a larger input */
    font-size: 18px; /* Larger font size for better readability */
    border: 2px hsla(55, 63%, 68%, 0.418);; /* Dark blue with some opacity */
    border-radius: 30px 0 0 30px; /* More pronounced rounded corners */
    outline: none; /* Remove outline */
    width: 350px; /* Increased width for the input */
    transition: border-color 0.3s ease, background-color 0.3s ease; /* Transition for border and background color */
    background-color: rgba(255, 255, 255, 0.8); /* Light background with opacity */
  }
  
  .search-bar input:focus {
    border-color: #ebb8ac; /* Change border color on focus */
    background-color: rgba(255, 255, 255, 1); /* Solid white background on focus */
  }
  
  .search-bar button {
    padding: 15px 30px; /* Increased padding for a larger button */
    background-color: hsla(55, 63%, 68%, 0.418); /* Fully opaque color */
    color: #ffffff; /* White text */
    border: none;
    border-radius: 0 30px 30px 0; /* More pronounced rounded corners */
    cursor: pointer;
    transition: background-color 0.3s ease; /* Transition for background color */
    font-size: 18px; /* Match font size with the input */
  }
  
  .search-bar button:hover {
    background-color: rgba(235, 184, 172, 0.8); /* Light color on hover with opacity */
  }
  </style>
  