import { createRouter, createWebHistory } from 'vue-router';

import FirstPage from '../components/FirstPage.vue'; // Path to FirstPage
import TheWelcome from '../components/TheWelcome.vue'; // Path to TheWelcome
import LibraryPage from '../components/LibraryPage.vue'; // Import Library page
import Favorites from '../components/Favorites.vue'; // Import Favorites component
import Reading from '../components/Reading.vue'; // Import Reading component
import WillRead from '../components/WillRead.vue'; // Import Will Read component
import HadRead from '../components/HadRead.vue'; // Import Had Read component
import Topics from '../components/Topics.vue'; // Import Topics component
import Contact from '../components/Contact.vue'; // Import Contact component
import Login from '../components/Login.vue'; // Import Login component
import SignIn from '../components/SignIn.vue'; // Import SignIn component
import SettingsPage from '../components/SettingsPage.vue'; // Import SettingsPage component
import AddBooks from '../components/Add.vue'; // Import AddBooks component
import AddAuthor from '../components/AddAuthor.vue'; // Import AddAuthor component
import Add from '../components/Add.vue'; // Importuj komponent Add.vue

const routes = [
  { path: '/', name: 'Home', component: FirstPage },
  { path: '/another-page', name: 'TheWelcome', component: TheWelcome }, // Route for Welcome Page
  { path: '/library', name: 'Library', component: LibraryPage },
  { path: '/favorites', name: 'Favorites', component: Favorites },
  { path: '/reading', name: 'Reading', component: Reading },
  { path: '/will-read', name: 'WillRead', component: WillRead },
  { path: '/had-read', name: 'HadRead', component: HadRead },
  { path: '/topics', name: 'Topics', component: Topics },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/sign_in', name: 'SignIN', component: SignIn },
  { path: '/login', name: 'Login', component: Login },
  { path: '/settings', name: 'Settings', component: SettingsPage },
  { path: '/add-author', name: 'AddAuthor', component: AddAuthor },
  { path: '/add', name: 'Add', component: AddBooks }, // Route for AddBooks page
  { path: '/add', name: 'Add', component: Add }, // Definicja trasy dla Add.vue
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
