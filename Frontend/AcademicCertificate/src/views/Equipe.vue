<script setup lang="ts">
// Importa o componente Button se necessário no futuro
// import Button from '@/components/Button.vue';

// Informações estáticas dos membros da equipe
const teamMembers = [
  {
    name: 'Arthur Azevedo',
    photo: 'https://avatars.githubusercontent.com/u/68549693?v=4',
  },
  {
    name: 'Diego Farias',
    photo: 'https://avatars.githubusercontent.com/u/103037462?v=4',
  },
  {
    name: 'Lavinia Fahning',
    photo: 'https://media.licdn.com/dms/image/v2/D4D03AQGQi1kCRv9Eww/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1712517373178?e=1738800000&v=beta&t=FJxtNhqGPL1PV_8v2E14ZxaYW3Zu5pSzyVtoO1d1J1I',
  },
  {
    name: 'Pedro Henrick',
    photo: 'https://avatars.githubusercontent.com/u/152924711?v=4',
  },
  {
    name: 'Mateus Lisboa',
    photo: 'https://media.licdn.com/dms/image/v2/C4D03AQEi5kUi4gaVLA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1653457385659?e=1738800000&v=beta&t=jbPh_GAWz7632iQ_fijrCC-qeyEb92oH5qdMW-wcCWo',
  },
];
</script>

<template>
  <main>
    <div class="content">
      <div class="text-info">
        <h1>Nossa Equipe</h1>
        <p>
          Conheça os membros dedicados da nossa equipe que trabalham arduamente para garantir a autenticidade e a segurança dos seus documentos acadêmicos na blockchain.
        </p>
      </div>
    </div>

    <div class="team-section">
      <div class="team-members">
        <div v-for="(member, index) in teamMembers" :key="index" class="team-member">
          <img :src="member.photo" :alt="member.name" class="member-photo">
          <p class="member-name">{{ member.name }}</p>
        </div>
      </div>
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
  flex-direction: column; /* Texto empilhado */
  align-items: center; /* Centraliza verticalmente os itens */
  gap: 20px; /* Espaçamento entre os elementos */
  max-width: 800px; /* Limita a largura */
  width: 100%; /* Garante responsividade */
  text-align: center; /* Centraliza o texto */
}

/* Texto Informativo */
.text-info h1 {
  font-size: 2rem; /* Tamanho base do título */
  margin-bottom: 10px;
}

.text-info p {
  font-size: 1rem; /* Tamanho base do parágrafo */
  line-height: 1.6; /* Melhora a legibilidade */
  margin-bottom: 20px;
}

/* Seção da Equipe */
.team-section {
  width: 100%;
  max-width: 1000px;
  margin-top: 40px;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.team-member {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 150px;
}

.member-photo {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%; /* Torna a imagem redonda */
  border: 2px solid #96FF7C; /* Opcional: adiciona uma borda */
}

.member-name {
  margin-top: 10px;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
}

/* Responsividade */

/* Tablets e dispositivos com largura máxima de 768px */
@media (max-width: 768px) {
  .team-members {
    gap: 15px;
  }

  .team-member {
    width: 120px;
  }

  .member-photo {
    width: 120px;
    height: 120px;
  }

  .member-name {
    font-size: 0.9rem;
  }
}

/* Dispositivos móveis com largura máxima de 480px */
@media (max-width: 480px) {
  .team-members {
    flex-direction: column;
    align-items: center;
  }

  .team-member {
    width: 100px;
  }

  .member-photo {
    width: 100px;
    height: 100px;
  }

  .member-name {
    font-size: 0.8rem;
  }
}
</style>
