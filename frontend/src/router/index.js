import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: 'employees',
          name: 'employees',
          component: () => import('../views/Employee/EmployeesView.vue')
        },
        {
          path: 'employees/create',
          name: 'employee-create',
          component: () => import('../views/Employee/EmployeeCreateView.vue')
        },
        {
          path: 'employees/:id/edit',
          name: 'employee-edit',
          component: () => import('../views/Employee/EmployeeEditView.vue')
        },
        {
          path: 'locations',
          name: 'locations',
          component: () => import('../views/Location/LocationsView.vue')
        },
        {
          path: 'locations/create',
          name: 'location-create',
          component: () => import('../views/Location/LocationCreateView.vue')
        },
        {
          path: 'locations/:id/edit',
          name: 'location-edit',
          component: () => import('../views/Location/LocationEditView.vue')
        },
        {
          path: 'items',
          name: 'items',
          component: () => import('../views/Item/ItemsView.vue')
        },
        {
          path: 'items/create',
          name: 'item-create',
          component: () => import('../views/Item/ItemCreateView.vue')
        },
      ]
    },
  ]
})

export default router