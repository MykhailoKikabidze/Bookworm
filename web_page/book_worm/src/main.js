
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://7ba3-188-146-152-208.ngrok-free.app';

app.use(router).mount('#app')

