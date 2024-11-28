
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://e1be-94-254-162-24.ngrok-free.app';

app.use(router).mount('#app')

