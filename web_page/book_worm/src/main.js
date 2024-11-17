
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://23d4-5-173-172-31.ngrok-free.app';

app.use(router).mount('#app')

