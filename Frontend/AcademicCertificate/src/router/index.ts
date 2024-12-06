import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CertificateUpload from '../views/UploadCertificate.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/upload-certificate',
      name: 'UploadCertificate',
      component: () => import('../views/UploadCertificate.vue'),
    },
    {
      path: '/aluno',
      name: 'aluno',
      component: () => import('../views/AlunoCertificado.vue'),
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('../views/Cadastro.vue'),
    },
    {
      path: '/equipe' 
      ,name: 'equipe'
      ,component: () => import('../views/Equipe.vue')
    }
  ],
})

export default router
