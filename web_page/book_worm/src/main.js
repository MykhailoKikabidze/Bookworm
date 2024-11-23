
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://5fac-5-173-192-15.ngrok-free.app';

app.use(router).mount('#app')

