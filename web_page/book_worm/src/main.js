
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://6ecd-213-241-49-110.ngrok-free.app';

app.use(router).mount('#app')

