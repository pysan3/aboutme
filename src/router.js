import { createRouter, createWebHashHistory } from 'vue-router';

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/resume', component: 'Resume' },
  { path: '/researches', component: 'Researches' },
  { path: '/papers', component: 'Papers' },
  { path: '/datasets', component: 'Datasets' },
  { path: '/codes', component: 'Codes' },
  { path: '/event/:id/:anchor?', component: 'Event' },
  { path: '/:pathMatch(.*)*', component: 'NotFound' },
];

const routes = routerOptions.map((route) => ({
  path: route.path,
  name: route.component.toLowerCase(),
  component: () => import(`@/views/${route.component}.vue`),
}));

export default createRouter({
  history: createWebHashHistory(),
  routes,
});
