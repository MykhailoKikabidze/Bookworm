
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://1593-46-113-8-57.ngrok-free.app';

app.use(router).mount('#app')

