import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      redirect: '/employees'
    },

    {
      path: '/employees',
      name: 'employees',
      component: () => import('../views/EmployeesView.vue')
    },

    {
      path: '/employees/create',
      name: 'employee-create',
      component: () => import('../views/EmployeeCreateView.vue')
    },

    {
      path: '/employees/:id/edit',
      name: 'employee-edit',
      component: () => import('../views/EmployeeEditView.vue')
    }
  ]
})

export default router