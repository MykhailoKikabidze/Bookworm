<template>
  <div class="title">
    <br><br>
    Genres
  </div>
  <div class="image-container">
    <div class="image-row">
      <router-link to="/another-page" class="image-wrapper">
        <img 
          src="./pictures/adventureBook.jpg" 
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Adventure</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/romanticBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Romantic</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/childBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Child</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/historicalBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">History</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/detectiveBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Detective</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/poetryBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Poetry</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/fantasyBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Fantasy</div>
          </div>
        </div>
      </router-link>

      <router-link to="/another-page" class="image-wrapper">
        <img
          src="./pictures/mysteryBook.jpg"
          class="image"
        />
        <div class="overlay">
          <div class="overlay-strip">
            <div class="overlay-text">Mystery</div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
  <div class="title">
    <br>
    POPULAR CLASSICS
  </div>
  <div class="classical-image-container">
    <div class="classical-image-row">
      <router-lint to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicBook1.jpg"
        class="classical-image"/>
      </router-lint>
      <router-lint to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook2.jpg"
        class="classical-image"/>
      </router-lint>
      <router-lint to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook3.jpg"
        class="classical-image"/>
      </router-lint>
      <router-lint to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook4.jpg"
        class="classical-image"/>
      </router-lint>
      <router-lint to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook5.jpg"
        class="classical-image"/>
      </router-lint>
    </div>
  </div>
</template>



  
  <script setup>
  </script>
  
  <style scoped>
  .classical-image-container{
    padding: 20px;
    text-align: center;
  }
  .classical-image-row{
    display:flex;
    overflow-x:auto;
    scroll-snap-type: x mandatory;
    gap: 15px;
  }
  .image-container {
    display: flex;         
    justify-content: center; 
    margin-top: 20px;       
  }
  
  .image-row {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 28px;
  }
  .classical-image-row::-webkit-scrollbar {
  display: none; /* Hide scrollbar */
}
  .classical-image:hover {
  transform: scale(1.05); /* Slightly scale up the image on hover */
}
  .classical-image-wrapper {
    flex: 0 0 auto;
    scroll-snap-align: start;
    scroll-behavior:smooth;
    }
  
  .title {
  text-align: center; /* Center the title */
  font-size: 36px; /* Increase font size */
  font-family: Garamond, serif;
  font-weight: 700; /* Use bold weight */
  color: #4A90E2; /* Change color to a shade you like */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Add text shadow */
  margin-bottom: 5px; /* Space below the title */
  letter-spacing: 2px; /* Increase spacing between letters */
  text-transform: uppercase; /* Make text uppercase for a modern look */
}
  .image-wrapper {
    position: relative; /* Set relative positioning on the image container */
    width: 250px; 
    height: 250px;
    overflow: hidden; /* Ensures the image doesn't overflow the container */
    border-radius: 29px; /* Apply border radius here to maintain shape on hover */
    transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition for transform and shadow */
  }
  
  .classical-image {
    width: 200px; 
    height: 290px;
    object-fit: cover;
    transition: transform 0.3s ease; /* Smooth transition for image scaling */
  }
  .image {
    width: 100%; 
    height: 100%;
    object-fit: cover; 
    border-radius: 29px; 
    display: block; 
    transition: transform 0.3s ease; /* Smooth transition for image scaling */
  }
  
  .image-wrapper:hover .image {
    transform: scale(1.05); /* Slightly scale up the image on hover */
  }
  
  .overlay {
    position: absolute; 
    top: 50%; /* Center the overlay vertically */
    left: 50%; /* Center the overlay horizontally */
    transform: translate(-50%, -50%); /* Center the overlay */
    width: 97%; /* Allow width to adjust based on content */
  }
  
  .overlay-strip {
    background-color: rgba(195, 157, 157, 0.707); /* Light grey color for the strip */
    height: 40px; /* Height of the strip */
    width: 100%;
    display: flex; /* Use flexbox for centering text */
    align-items: center; /* Center text vertically within the strip */
    justify-content: center; /* Center text horizontally within the strip */
    border-radius: 5px; /* Optional: round the corners of the strip */
    transition: background-color 0.3s ease, transform 0.3s ease; /* Smooth transition for strip background color and scaling */
  }
  
  .overlay-text {
    color: black; /* Change text color to contrast with the strip */
    font-size: 18px; /* Adjust as needed */
    font-weight: bold; /* Make the text bold */
  }
  
  /* Hover Effects */
 
  .image-wrapper:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); /* Add shadow effect on hover */
  }
  
  .image-wrapper:hover .overlay-strip {
    background-color: rgba(255, 255, 255, 0.9); /* Change overlay background color on hover */
    transform: scale(1.05); /* Scale up the strip slightly */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* Add shadow to the strip */
    border-radius: 5px; /* Keep corners rounded */
  }
  </style>
  