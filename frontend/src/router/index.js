import { createRouter, createWebHistory } from 'vue-router'
import InventoryView from '../views/InventoryView.vue'
import PoliciesView from '../views/PoliciesView.vue'

const routes = [
  {
    path: '/',
    redirect: '/policies', // Default to policies
  },
  { path: '/inventory', name: 'inventory', component: InventoryView },
  {
    path: '/policies',
    name: 'policies',
    component: PoliciesView,
  },
  {
    path: '/settings',
    name: 'settings',
    // Lazy load example: only loads file when visited
    component: () => import('../views/SettingsView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
