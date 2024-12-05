<template>
  <div class="certificate-upload">
    <NavBar />
    <main class="main-content">
      <h2 class="title">Consulta de Certificado Acadêmico</h2>
      
      <div class="search-section">
        <input 
          v-model="certificateHash"
          type="text"
          placeholder="Digite o hash do certificado"
          class="hash-input"
        />
        <button @click="fetchCertificate" class="search-button">Buscar Certificado</button>
      </div>

      <div v-if="certificateData" class="certificate-details">
        <h3>Detalhes do Certificado</h3>
        <div class="detail-item">
          <strong>Nome do Aluno:</strong> {{ certificateData.student_name }}
        </div>
        <div class="detail-item">
          <strong>Data de Emissão:</strong> {{ formatDate(certificateData.issue_date) }}
        </div>
        <div class="detail-item">
          <strong>Endereço da Instituição:</strong> {{ certificateData.institution_address }}
        </div>
        <div class="detail-item" v-if="certificateData.file_path">
          <a :href="getFileUrl(certificateData.file_path)" target="_blank" class="view-certificate">
            Visualizar Certificado
          </a>
        </div>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'AlunoCertificado',
  components: {
    NavBar
  },
  data() {
    return {
      certificateHash: '',
      certificateData: null,
      error: null
    }
  },
  methods: {
    async fetchCertificate() {
      try {
        this.error = null
        this.certificateData = null
        
        if (!this.certificateHash) {
          this.error = 'Por favor, insira o hash do certificado'
          return
        }

        const response = await axios.get(`/api/get_certificate/${this.certificateHash}`)
        if (response.data.status === 'success') {
          this.certificateData = response.data.certificate
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Erro ao buscar o certificado'
      }
    },
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleDateString('pt-BR')
    },
    getFileUrl(filePath) {
      return `/api/files/${filePath}`
    }
  }
}
</script>

<style scoped>
.certificate-upload {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.user-info {
  display: flex;
  gap: 1rem;
}

.main-content {
  margin-top: 200px;
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.title {
  margin-top: 200px;
  text-align: center;
  margin-bottom: 3rem;
  font-size: 1.5rem;
  color: #333;
}

.search-section {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
}

.hash-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-button {
  padding: 0.5rem 1rem;
  background-color: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #333;
}

.certificate-details {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-item {
  margin-bottom: 1rem;
}

.view-certificate {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  margin-top: 1rem;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>