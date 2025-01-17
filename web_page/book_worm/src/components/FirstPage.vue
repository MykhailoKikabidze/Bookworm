<template>
  
</template>

<script setup>
</script>

<style scoped>
.classical-image-container {
  padding: 20px;
  text-align: center;
  overflow-x: auto; /* Włącz przewijanie w poziomie */
  white-space: nowrap; /* Zapobiega łamaniu linii w poziomie */
}

.classical-image-row {
  display: inline-flex; /* Zamiast flex, używamy inline-flex, by umożliwić przewijanie poziome */
  justify-content: flex-start; /* Wyrównanie obrazków po lewej stronie */
  gap: 15px;
}

.classical-image-wrapper {
  position: relative;
  width: 250px;  /* Można dostosować szerokość obrazków */
  height: 350px; /* Można dostosować wysokość obrazków */
  overflow: hidden;
  border-radius: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  flex-shrink: 0; /* Zapobiega skurczeniu się obrazków */
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



.classical-image-wrapper:hover {
  transform: scale(1.1); /* Slightly enlarge the image */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
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
  font-size: 50px; /* Font size for better visibility */
  font-family: 'Lora', serif; /* Elegant serif font */
  font-weight: 700; /* Bold font for stronger visibility */
  color: #fff; /* White text color */
  
  margin-top: 30px; /* Increased top margin for better spacing */
  margin-bottom: 30px; /* Increased bottom margin for better spacing */
  letter-spacing: 4px; /* Slightly wider letter spacing for elegance */
  text-transform: uppercase; /* Uppercase letters for stronger effect */
  
  position: relative;
  width: 100%; /* Full width of the screen */
  height: 50px; /* Height of the line */
  padding: 0; /* Remove additional padding */
  background-color: #8d6e631c; /* Set opacity to 0.5 */
  color: #8d6e63; /* White text color */
  border-radius: 0; /* No border radius for a straighter appearance */
  margin: 0 auto; /* Center the element horizontally */
  box-shadow: none; /* No shadow for a cleaner line */
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
