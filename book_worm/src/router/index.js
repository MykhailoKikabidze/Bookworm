import { createRouter, createWebHistory } from 'vue-router';
import FirstPage from '../components/FirstPage.vue'; // Path to FirstPage
import TheWelcome from '../components/TheWelcome.vue'; // Path to TheWelcome

const routes = [
  { path: '/', name: 'Home', component: FirstPage }, // Route for First Page
  { path: '/another-page', name: 'TheWelcome', component: TheWelcome } // Route for Welcome Page
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Correct use of BASE_URL
  routes,
});

export default router;
