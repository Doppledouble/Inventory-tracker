import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [

        // EMPLOYEE ROUTES
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

        // ITEM ROUTES
        {
          path: 'items',
          name: 'items',
          component: () => import('../views/Item/ItemsView.vue')
        },
        {
          path: 'items/material',
          name: 'material',
          component: () => import('../views/Item/ItemsView.vue')
        },
        {
          path: 'items/tool',
          name: 'tool',
          component: () => import('../views/Item/ItemsView.vue')
        },
        {
          path: 'items/create',
          name: 'item-create',
          component: () => import('../views/Item/ItemCreateView.vue')
        },
        {
          path: 'items/:id/edit',
          name: 'item-edit',
          component: () => import('../views/Item/ItemEditView.vue')
        },

        // ASSIGNMENT ROUTES
        {
          path: 'assignments',
          name: 'assignments',
          component: () => import('../views/Assignment/AssignmentsView.vue')
        },
        {
          path: 'assignments/create',
          name: 'assignment-create',
          component: () => import('../views/Assignment/AssignmentCreateView.vue')
        },

        // TRANSACTIONS ROUTES
        {
          path: 'transactions',
          name: 'transactions',
          component: () => import('../views/Transaction/TransactionsView.vue')
        }
      ]
    },
  ]
})

export default router