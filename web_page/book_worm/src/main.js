
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://ccc3-46-112-2-59.ngrok-free.app';

app.use(router).mount('#app')

