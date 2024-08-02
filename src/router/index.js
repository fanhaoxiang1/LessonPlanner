import { createRouter, createWebHistory } from 'vue-router';
import LessonEdit from '@/views/LessonEdit.vue';
import LessonCreate from '@/views/LessonCreate.vue';
import LessonMain from '@/views/LessonMain.vue';

const routes = [
  {
    path: '/lesson-edit',
    name: 'LessonEdit',
    component: LessonEdit
  },
  {
    path: '/lesson-create',
    name: 'LessonCreate',
    component: LessonCreate
  },
  {
    path: '/lesson-main',
    name: 'LessonMain',
    component: LessonMain
  },
  // 其他路由...
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;