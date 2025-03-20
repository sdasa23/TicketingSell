// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import homePage from '@/components/homePage.vue';
import connectMateMask from '../components/connectMateMask.vue';
import firstMarket from '../components/firstMarket.vue';
import secondMarket from '../components/secondMarket.vue';
import newUser from '../components/newUser.vue';

const routes = [
  {
    path: '/', 
    name: 'connectMateMask',  
    component: connectMateMask, 
  },
  {
    path: '/homePage', 
    name: 'homePage',  
    component: homePage, 
  },
  {
    path: '/firstMarket', 
    name: 'firstMarket',  
    component: firstMarket, 
  },
  {
    path: '/secondMarket', 
    name: 'secondMarket',  
    component: secondMarket, 
  },
  {
    path: '/newUser', 
    name: 'newUser',  
    component: newUser, 
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;