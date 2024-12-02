
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://7067-94-254-233-7.ngrok-free.app';

app.use(router).mount('#app')

