
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://355b-5-173-157-77.ngrok-free.app';

app.use(router).mount('#app')

