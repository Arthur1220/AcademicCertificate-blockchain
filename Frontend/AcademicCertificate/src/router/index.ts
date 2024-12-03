import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue';
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
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('../views/Cadastro.vue'),
    },
    {
      path: '/upload-certificate',  
      name: 'UploadCertificate',  
      component: CertificateUpload,  
    },
  ],
})

export default router
