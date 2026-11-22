export default [
  {
    path: '/invite/:token/register',
    name: 'invite-register',
    component: () => import('./views/RegisterView.vue'),
    meta: { public: true },
  },
]
