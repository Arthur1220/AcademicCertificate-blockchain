<script setup lang="ts">
import Button from '@/components/Button.vue';

const redirectToMetaMask = () => {
  window.open('https://metamask.io/', '_blank');
};
</script>

<template>
  <main>
    <!-- Seção do Nome do Projeto e Frase de Efeito -->
    <div class="project-info">
      <h1>Certifica Block</h1>
      <p class="tagline">Onde a confiança encontra a imutabilidade, e cada certificado se torna inquebrável.</p>
    </div>

    <!-- Seção de Conteúdo Principal -->
    <div class="content">
      <div class="text-info">
        <h2>Certifique seus documentos acadêmicos aqui</h2>
        <p>
          Simplifique a validação de diplomas e históricos escolares com um processo rápido, seguro e 100% online.
          Garantimos a autenticidade e o reconhecimento de seus documentos, seja para fins acadêmicos ou profissionais.
        </p>
      </div>
      <img src="../assets/certificate.jpg" alt="Certificate" class="certificate-image">
    </div>

    <!-- Seção de Explicação Detalhada -->
    <div class="detailed-info">
      <h2>Como Funciona o Certifica Block:</h2>
      <p>
        O <strong>Certifica Block</strong> permite que instituições de ensino e professores registrem certificados acadêmicos diretamente na blockchain, garantindo
        a imutabilidade e a segurança dos documentos. Com essa tecnologia, cada certificado recebe um hash único que o torna inquebrável e facilmente verificável.
      </p>
      <p>
        Os alunos podem procurar por seus certificados utilizando o nome ou o hash correspondente, facilitando a validação por potenciais empregadores ou outras instituições
        educacionais. Todo o processo é transparente, eficiente e confiável, eliminando fraudes e simplificando a gestão de documentos acadêmicos.
      </p>
    </div>

    <!-- Botão para Iniciar (Cadastre-se na MetaMask) -->
    <div class="button-comecar">
      <Button @click="redirectToMetaMask">Cadastrar na MetaMask</Button>
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
  min-height: 150vh; /* Centraliza verticalmente o conteúdo */
  padding: 20px;
}

/* Seção do Projeto */
.project-info {
  text-align: center;
  margin-bottom: 30px;
}

.project-info h1 {
  font-size: 2.5rem;
  color: #f6851b; /* Cor característica da MetaMask */
  margin-bottom: 10px;
}

.project-info .tagline {
  font-size: 1.25rem;
  color: #333;
  max-width: 800px;
  margin: 0 auto;
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

.text-info {
  flex: 1; /* Permite que o texto ocupe mais espaço */
}

.text-info h2 {
  text-align: center; /* Centraliza o texto */
  font-size: 1.5rem; /* Tamanho base do título */
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

/* Seção de Explicação Detalhada */
.detailed-info {
  max-width: 800px;
  width: 100%;
  margin-top: 40px;
  text-align: left;
}

.detailed-info h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.detailed-info p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 15px;
}

/* Botão */
.button-comecar {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  width: 100%;
}

/* Responsividade */

/* Tablets e dispositivos com largura máxima de 768px */
@media (max-width: 768px) {
  .project-info h1 {
    font-size: 2rem;
  }

  .project-info .tagline {
    font-size: 1rem;
  }

  .content {
    flex-direction: column; /* Empilha os elementos verticalmente */
    align-items: center; /* Centraliza o conteúdo */
    text-align: center; /* Centraliza o texto */
  }

  .certificate-image {
    width: 250px;
    margin: 20px 0; /* Espaçamento ao redor da imagem */
  }

  .text-info h2 {
    font-size: 1.5rem;
  }

  .text-info p {
    font-size: 1.125rem;
  }

  .detailed-info {
    margin-top: 30px;
  }
}

/* Dispositivos móveis com largura máxima de 480px */
@media (max-width: 480px) {
  .project-info h1 {
    font-size: 1.75rem;
  }

  .project-info .tagline {
    font-size: 0.95rem;
  }

  .content {
    gap: 15px; /* Reduz o espaçamento entre os elementos */
  }

  .certificate-image {
    width: 200px; /* Reduz a largura da imagem */
  }

  .text-info h2 {
    font-size: 1.25rem;
  }

  .text-info p {
    font-size: 1rem;
  }

  .detailed-info h2 {
    font-size: 1.25rem;
  }

  .detailed-info p {
    font-size: 0.95rem;
  }
}
</style>
