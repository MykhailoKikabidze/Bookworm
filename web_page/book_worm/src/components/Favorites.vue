<template>
  <div>
    <h1>Favourites</h1>
    <ul>
      <li v-for="book in books" :key="book.id">
        {{ book.title }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: [], // Lista książek
    };
  },
  methods: {
    async fetchBooksByGroup(group) {
      try {
        const response = await fetch(`${this.$link_backend}/books?group=${group}`, {
          method: "GET",
          headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "ngrok-skip-browser-warning": "anyValue",
          },
        });

        if (response.ok) {
          this.books = await response.json();
        } else {
          const error = await response.json();
          console.error("Error fetching books:", error);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },
  created() {
    this.fetchBooksByGroup("is_favourite"); // Pobierz tylko książki z ulubionych
  },
};
</script>
