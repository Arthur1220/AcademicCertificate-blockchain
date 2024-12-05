<script setup lang="ts">
import Button from '@/components/Button.vue';
</script>

<template>
  <main>
    <div class="content">
      <div class="text-info">
        <h1>Certifique seus documentos acadêmicos aqui</h1>
        <p>Simplifique a validação de diplomas e históricos escolares com um processo rápido, seguro e 100% online. Garantimos a autenticidade e o reconhecimento de seus documentos, seja para fins acadêmicos ou profissionais.</p>
      </div>
      <img src="../assets/certificate.jpg" alt="Certificate" class="certificate-image">
    </div>

    <div class="button-comecar">
      <Button></Button>
    </div>
  </main>
</template>

<style scoped>
/* Estilos Globais */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}

/* Estilo do Main */
main {
  display: flex;
  flex-direction: column; /* Elementos empilhados */
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* Centraliza verticalmente o conteúdo */
  padding: 20px;
}

/* Conteúdo Centralizado */
.content {
  display: flex;
  flex-direction: row; /* Texto e imagem lado a lado */
  align-items: center; /* Alinha verticalmente os itens */
  gap: 20px; /* Espaçamento entre os elementos */
  max-width: 800px; /* Limita a largura */
  width: 100%; /* Garante responsividade */
}

/* Texto Informativo */
.text-info {
  flex: 1; /* Permite que o texto ocupe mais espaço */
}

.text-info h1 {
  text-align: center; /* Centraliza o texto */
  font-size: 1.75rem; /* Tamanho base do título */
  margin-bottom: 10px;
}

.text-info p {
  text-align: left; /* Alinha o texto à esquerda */
  font-size: 1rem; /* Tamanho base do parágrafo */
  line-height: 1.6; /* Melhora a legibilidade */
  margin-bottom: 20px;
}

/* Imagem */
.certificate-image {
  width: 300px;
  height: auto; /* Mantém a proporção */
  flex-shrink: 0; /* Impede que a imagem encolha */
}

/* Botão */
.button-comecar {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

/* Responsividade */

/* Tablets e dispositivos com largura máxima de 768px */
@media (max-width: 768px) {
  .content {
    flex-direction: column; /* Empilha os elementos verticalmente */
    align-items: center; /* Centraliza o conteúdo */
    text-align: center; /* Centraliza o texto */
  }

  .certificate-image {
    width: 250px;
    margin: 20px 0; /* Espaçamento ao redor da imagem */
  }

  .text-info h1 {
    font-size: 1.75rem; /* Ajusta o título para telas menores */
  }

  .text-info p {
    font-size: 1.125rem; /* Ajusta o parágrafo para telas menores */
  }
}

/* Dispositivos móveis com largura máxima de 480px */
@media (max-width: 480px) {
  .content {
    gap: 15px; /* Reduz o espaçamento entre os elementos */
  }

  .certificate-image {
    width: 200px; /* Reduz a largura da imagem */
  }

  .text-info h1 {
    font-size: 1.5rem; /* Ajusta o tamanho do título */
  }

  .text-info p {
    font-size: 1rem; /* Ajusta o tamanho do parágrafo */
  }
}
</style>
