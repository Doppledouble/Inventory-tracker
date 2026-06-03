import { createRouter, createWebHistory } from 'vue-router'
import EmployeesView from '../views/EmployeesView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/employees',
      component: EmployeesView
    }
  ]
})

export default router