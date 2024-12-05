<template>
  <div class="certificate-upload">
    <NavBar />
    <main class="main-content">
      <h2 class="title">Consulta de Certificado Acadêmico</h2>
      
      <!-- Campo de busca único, centralizado -->
      <div class="search-section">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Digite o nome ou ID do certificado"
          class="search-input"
        />
        <button @click="fetchCertificate" class="search-button">Buscar</button>
      </div>

      <!-- Exibição dos resultados em tabela -->
      <div v-if="certificateData" class="certificate-table">
        <h3>Detalhes do Certificado</h3>
        <table>
          <thead>
            <tr>
              <th>Nome do Aluno</th>
              <th>Data de Emissão</th>
              <th>Endereço da Instituição</th>
              <th>Visualizar Certificado</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ certificateData.student_name }}</td>
              <td>{{ formatDate(certificateData.issue_date) }}</td>
              <td>{{ certificateData.institution_address }}</td>
              <td v-if="certificateData.file_path">
                <a :href="getFileUrl(certificateData.file_path)" target="_blank" class="view-certificate">
                  Visualizar
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mensagem de erro -->
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
      searchQuery: '',
      certificateData: null,
      error: null
    }
  },
  methods: {
    async fetchCertificate() {
      try {
        this.error = null
        this.certificateData = null

        if (!this.searchQuery) {
          this.error = 'Por favor, insira o nome ou ID do certificado'
          return
        }

        const response = await axios.get(`/api/get_certificate_by_name_or_id/${this.searchQuery}`)
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
  background-color: #ffffff;
}

.main-content {
  margin-top: 100px;
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.title {
  margin-top: 110px;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  color: #333;
}

.search-section {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.search-input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1.2rem;
  width: 70%;
  max-width: 500px;
}

.search-button {
  padding: 0.8rem 1.5rem;
  background-color: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #333;
}

.certificate-table {
  margin-top: 2rem;
  background-color: #f2f2f2;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background-color: #fff;
  margin: 0 auto;
}

th, td {
  padding: 0.8rem;
  border: 1px solid #ddd;
}

th {
  background-color: #333;
  color: white;
}

.view-certificate {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>
