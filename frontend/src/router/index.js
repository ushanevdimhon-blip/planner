import { createRouter, createWebHistory } from 'vue-router'
import authRoutes from '@/modules/auth/routes'
import invitationsRoutes from '@/modules/invitations/routes'

// Каждый модуль отдаёт свой массив маршрутов, здесь они только собираются.
const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...authRoutes,
    ...invitationsRoutes,
    { path: '/:pathMatch(.*)*', redirect: '/login' },
  ],
})

// TODO: guard — неавторизованных отправлять на /login (маршруты с meta.public пропускать)

export default router
