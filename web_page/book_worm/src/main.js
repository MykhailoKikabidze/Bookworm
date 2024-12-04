
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://a416-5-173-200-19.ngrok-free.app';

app.use(router).mount('#app')

