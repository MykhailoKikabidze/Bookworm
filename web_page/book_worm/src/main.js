
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App);
app.config.globalProperties.$link_backend = 'https://6ef4e603f8d687c7bbc1cca215251e6d.serveo.net';

app.use(router).mount('#app')

