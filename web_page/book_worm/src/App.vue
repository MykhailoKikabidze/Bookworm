<!-- App.vue -->
<template>
  <div id="app">
    <!-- Your Navbar or Menu component -->
    <Menu />
    
    <!-- The <router-view> will render the component for the current route -->
    <router-view></router-view>
  </div>
</template>

<script>
import Menu from './components/Menu.vue'; // Import your navbar or menu component

export default {
  components: {
    Menu, // Register the Menu component
  },
};
</script>

<style>

</style>
