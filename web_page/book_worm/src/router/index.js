import { createRouter, createWebHistory } from 'vue-router';

import FirstPage from '../components/FirstPage.vue'; // Path to FirstPage
import TheWelcome from '../components/TheWelcome.vue'; // Path to TheWelcome
import LibraryPage from '../components/LibraryPage.vue'; // Import your Library page component
import Favorites from '../components/Favorites.vue'; // Import Favorites component
import Reading from '../components/Reading.vue'; // Import Reading component
import WillRead from '../components/WillRead.vue'; // Import Will Read component
import HadRead from '../components/HadRead.vue'; // Import Had Read component
import Topics from '../components/Topics.vue'; // Import Topics component
import Contact from '../components/Contact.vue'; // Import Contact component
import Login from '../components/Login.vue'; // Import Login component
import SignUp from '../components/SignUp.vue'; // Import Sign Up component

const routes = [
 
  { path: '/', name: 'Home', component: FirstPage }, // Route for First Page
  { path: '/another-page', name: 'TheWelcome', component: TheWelcome }, // Route for Welcome Page
  { path: '/library', name: 'Library', component: LibraryPage }, // New route for Library page
  { path: '/favorites', name: 'Favorites', component: Favorites }, // New route for Favorites page
  { path: '/reading', name: 'Reading', component: Reading }, // New route for Reading page
  { path: '/will-read', name: 'WillRead', component: WillRead }, // New route for Will Read page
  { path: '/had-read', name: 'HadRead', component: HadRead }, // New route for Had Read page
  { path: '/topics', name: 'Topics', component: Topics }, // New route for Topics page
  { path: '/contact', name: 'Contact', component: Contact }, // New route for Contact page
  { path: '/sign_up', name: 'SignUP', component: SignUp }, // New route for Sign Up page
  { path: '/login', name: 'Login', component: Login } // New route for Login page
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Correct use of BASE_URL
  routes,
});

export default router;
