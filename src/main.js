import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';
import mixin from '@/mixin';
import axios from '@/axios';
import i18n from '@/i18n';

const app = createApp(App)
  .use(router)
  .use(store)
  .use(i18n)
  .mixin(mixin);

app.config.globalProperties.$axios = axios;

app.mount('#app');
