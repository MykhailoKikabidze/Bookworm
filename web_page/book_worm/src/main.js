
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://c37c-5-173-24-88.ngrok-free.app';

app.use(router).mount('#app')

