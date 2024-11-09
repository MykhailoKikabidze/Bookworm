<template>
  <div class="title">
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
    POPULAR CLASSICS
  </div>
  <div class="classical-image-container">
    <div class="classical-image-row">
      <router-link to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicBook1.jpg"
        class="classical-image"/>
      </router-link>
      <router-link to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook2.jpg"
        class="classical-image"/>
      </router-link>
      <router-link to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook3.jpg"
        class="classical-image"/>
      </router-link>
      <router-link to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook4.jpg"
        class="classical-image"/>
      </router-link>
      <router-link to="/another-page" class="classical-image-wrapper">
        <img
        src="./pictures/classicalBook5.jpg"
        class="classical-image"/>
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.classical-image-container {
  padding: 20px;
  text-align: center;
}

.classical-image-row {
  display: flex;
  justify-content: center; /* Center images horizontally */
  gap: 15px;
  flex-wrap: wrap; /* Allow wrapping for smaller screens */
}

.image-container {
  display: flex;
  justify-content: center; /* Center horizontally */
  margin-top: 10px; /* Reduced margin for better layout */
}

.image-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 columns */
  gap: 28px;
  width: 100%;
  justify-items: center; /* Center images within grid cells */
}

.classical-image-wrapper {
  width: 250px;  /* Larger size for classical images */
  height: 350px; /* Larger height for classical images */
  flex: 0 0 auto;
}

.image-wrapper {
  position: relative;
  width: 300px; /* Increased size for images in the Genres section */
  height: 300px; /* Increased height for images in the Genres section */
  overflow: hidden;
  border-radius: 15px; /* Rounded corners */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.title {
  text-align: center;
  font-size: 50px; /* Lekko większa czcionka dla lepszej widoczności */
  font-family: 'Lora', serif; /* Elegancka czcionka szeryfowa */
  font-weight: 700; /* Gruby font dla większej widoczności */
  color: #303031b9; /* Ciepły złoty kolor */
  
  margin-top: 15px; /* Mniejszy margines górny */
  margin-bottom: 15px; /* Mniejszy margines dolny */
  letter-spacing: 3px; /* Szersze odstępy między literami */
  text-transform: uppercase; /* Duże litery dla mocniejszego efektu */
 
}





.classical-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Cover images for the classical section */
  transition: transform 0.3s ease;
}

.image-wrapper {
  position: relative;
  width: 280px; /* Adjusted width for a more balanced layout */
  height: 280px; /* Adjusted height */
  overflow: hidden;
  border-radius: 12px; /* Slightly less rounded corners */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Adjust to fit images properly */
  border-radius: 15px;
  display: block;
  transition: transform 0.3s ease;
}

.image-wrapper:hover .image {
  transform: scale(1.05); /* Slightly scale up the image on hover */
}

.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 97%;
}

.overlay-strip {
  background-color: rgba(255, 255, 255, 0.7); /* Lighter overlay for better contrast */
  height: 45px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
}

.overlay-text {
  color: #333333; /* Darker text for better contrast */
  font-size: 20px; /* Slightly larger text */
  font-weight: 600;
}

.image-wrapper:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.image-wrapper:hover .overlay-strip {
  background-color: rgba(255, 255, 255, 0.9);
  transform: scale(1.05);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

/* Media queries for responsiveness */
@media (max-width: 1200px) {
  .image-row {
    grid-template-columns: repeat(3, 1fr); /* 3 columns on medium screens */
  }
}

@media (max-width: 900px) {
  .image-row {
    grid-template-columns: repeat(2, 1fr); /* 2 columns on small screens */
  }
}

@media (max-width: 600px) {
  .image-row {
    grid-template-columns: 1fr; /* 1 column on extra small screens */
  }
}
</style>
