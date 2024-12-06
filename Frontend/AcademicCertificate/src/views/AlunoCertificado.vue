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
      <div v-if="certificateData.length > 0" class="certificate-table">
        <h3>Detalhes do Certificado</h3>
        <table>
          <thead>
            <tr>
              <th>Nome do Aluno</th>
              <th>Data de Emissão</th>
              <th>Endereço da Transação</th>
              <th>Obter Link</th> <!-- Somente a coluna de "Me Dê o Link" -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(certificate, index) in certificateData" :key="index">
              <td>{{ certificate.student_name }}</td>
              <td>{{ formatDate(certificate.issue_date) }}</td>
              <td>{{ certificate.transaction_hash }}</td>
              <td>
                <button 
                  @click="copyLink(certificate.file_path)"
                  class="view-certificate">
                  Me Dê o Link
                </button>
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

axios.defaults.baseURL = 'http://localhost:5000'

export default {
  name: 'AlunoCertificado',
  components: {
    NavBar
  },
  data() {
    return {
      searchQuery: '',
      certificateData: [],  // Inicialize como um array vazio
      error: null
    }
  },
  methods: {
    async fetchCertificate() {
      try {
        this.error = null
        this.certificateData = [] // Limpa os dados antes de uma nova requisição

        if (!this.searchQuery) {
          this.error = 'Por favor, insira o nome ou ID do certificado'
          return
        }

        // Requisição ao backend para buscar o certificado
        const response = await axios.get(`http://localhost:5000/get_certificate?student_name=${this.searchQuery}`)
        
        if (response.data.status === 'success') {
          // Verifica se é um único certificado e transforma em array
          this.certificateData = Array.isArray(response.data.certificates)
            ? response.data.certificates
            : [response.data.certificates] // Garante que seja sempre um array
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Erro ao buscar o certificado'
      }
    },
    formatDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleDateString('pt-BR')
    },
    copyLink(filePath) {
      const fileUrl = 'file:///' + filePath; // O link completo para o arquivo
      // Cria um elemento de input temporário
      const tempInput = document.createElement('input');
      tempInput.value = fileUrl;
      document.body.appendChild(tempInput);
      tempInput.select();
      document.execCommand('copy');
      document.body.removeChild(tempInput);

      // Alerta ou feedback visual para o usuário
      alert(`Link copiado para a área de transferência: ${fileUrl}`);
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
  table-layout: fixed; /* Coloca a tabela em layout fixo para controlar melhor as larguras */
}

th, td {
  padding: 0.8rem;
  border: 1px solid #ddd;
  word-wrap: break-word; /* Garante que o texto não ultrapasse a célula */
  overflow: hidden; /* Esconde o texto que ultrapassa o limite da célula */
  text-overflow: ellipsis; /* Exibe "..." quando o texto é grande demais */
}

th {
  background-color: #333;
  color: white;
}

td {
  max-width: 200px; /* Limita a largura das células para evitar que ultrapassem */
  white-space: nowrap; /* Impede que o texto quebre para outra linha */
}

.view-certificate {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap; /* Impede o botão de quebrar a linha */
  min-width: 120px; /* Tamanho mínimo para o botão */
  text-align: center;
}

.view-certificate:hover {
  background-color: #45a049;
}

.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
}
</style>
