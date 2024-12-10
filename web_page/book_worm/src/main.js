
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://fdaa-5-173-196-178.ngrok-free.app';

app.use(router).mount('#app')

