<script setup lang="ts">
import Button from '@/components/Button.vue';
</script>

<template>
  <main>
      <div class="text-info">
        <h1>Certifique seus documentos academicos aqui</h1>
        <p>Simplifique a validação de diplomas e históricos escolares com um processo rápido, seguro e 100% online. Garantimos a autenticidade e o reconhecimento de seus documentos, seja para fins acadêmicos ou profissionais.</p>
      </div>

      <img src="../assets/3d cartoon style certificate with gold medal icon.jpg" alt="Certificate">
  </main>
  <div class="Button-comecar">
    <Button></Button>
  </div>
</template>

<style scoped>
  * {
    margin: 0;
    padding: 0;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  }
  main{
    display: flex;
    gap: 200px;
    align-items: center;
    justify-content: center;
  }
  .text-info {
    margin-top: 200px;
    display: flex;
    flex-direction: column;
    width: 300px;
    gap: 50px;
  }
  img {
    margin-top: 200px;
    width: 300px;
    height: 300px;
  }

  .Button-comecar {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 150px;
  }
</style>
