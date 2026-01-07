/**
 * Authors of code:
 * - 
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
import UserAccount from '@/views/UserAccount.vue'
import FavoriteSongs from '@/components/FavoriteSongs.vue'
import Admin from '@/views/Admin.vue'
import ModelPerformance from '@/views/ModelPerformance.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
    {
      path: '/model-performance',
      name: 'model-performance',
      component: ModelPerformance,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserAccount,
    },
    {
      path: '/favorite_songs',
      name: 'favoriteSongs',
      component: FavoriteSongs,
    },
    {
      path: '/history',
      name: 'history',
      component: History,
    },
  ],
})

export default router
