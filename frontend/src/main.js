import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/newstyle.css'
import "@tabler/icons-webfont/dist/tabler-icons.min.css";

createApp(App)
  .use(router)
  .mount('#app')