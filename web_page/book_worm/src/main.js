
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://7ab3-212-191-80-214.ngrok-free.app';

app.use(router).mount('#app')

