<template>
  <div class="certificate-upload">
    <NavBar />
    <main class="main-content">
      <div class="container">
        <h1 class="title">Consulta de Certificado Acadêmico</h1>

        <!-- Campo de busca único, centralizado -->
        <div class="search-section">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Digite o nome ou ID do certificado"
            class="search-input"
          />
          <button @click="fetchCertificate" class="search-button" :disabled="loading">
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>

        <!-- Exibição dos resultados em tabela -->
        <div v-if="certificateData.length > 0" class="certificate-table">
          <h2>Detalhes do Certificado</h2>
          <table>
            <thead>
              <tr>
                <th>Nome do Aluno</th>
                <th>Data de Emissão</th>
                <th>Endereço da Transação</th>
                <th>Obter Link</th>
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
                    class="view-certificate"
                  >
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
      error: null,
      loading: false
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

        this.loading = true

        // Requisição ao backend para buscar o certificado
        const response = await axios.get(`/get_certificate`, {
          params: {
            student_name: this.searchQuery
          }
        })
        
        if (response.data.status === 'success') {
          // Verifica se é um único certificado e transforma em array
          this.certificateData = Array.isArray(response.data.certificates)
            ? response.data.certificates
            : [response.data.certificates] // Garante que seja sempre um array
        } else {
          this.error = response.data.message || 'Nenhum certificado encontrado.'
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Erro ao buscar o certificado'
      } finally {
        this.loading = false
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
/* Reset Global */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lucida Sans', sans-serif;
}

/* Estilo Principal */
.certificate-upload {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centraliza verticalmente */
  align-items: center;     /* Centraliza horizontalmente */
  min-height: 100vh;
  background-color: #ffffff;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* Container */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  width: 100%;
  max-width: 800px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Título */
.title {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

/* Campo de Busca */
.search-section {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 20px;
}

.search-input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 1rem;
  flex: 1;
  max-width: 500px;
}

.search-button {
  padding: 0.8rem 1.5rem;
  background-color: #96FF7C;
  border: none;
  border-radius: 0 4px 4px 0;
  color: black;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.search-button:hover:not(:disabled) {
  background-color: #1abc9c;
}

.search-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Tabela de Certificados */
.certificate-table {
  width: 100%;
  margin-top: 20px;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.certificate-table h2 {
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th, td {
  padding: 0.8rem;
  border: 1px solid #ddd;
  word-wrap: break-word;
}

th {
  background-color: #333;
  color: white;
}

td {
  background-color: #fff;
}

/* Botão "Me Dê o Link" */
.view-certificate {
  padding: 0.5rem 1rem;
  background-color: #96FF7C;
  border: none;
  border-radius: 4px;
  color: black;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.view-certificate:hover {
  background-color: #1abc9c;
}

/* Mensagem de Erro */
.error-message {
  color: #dc3545;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .container {
    padding: 20px;
    width: 95%;
  }

  .title {
    font-size: 1.75rem;
  }

  .search-input {
    font-size: 0.95rem;
  }

  .search-button {
    font-size: 0.95rem;
    padding: 0.7rem 1.2rem;
  }

  .certificate-table h2 {
    font-size: 1.25rem;
  }

  th, td {
    padding: 0.6rem;
    font-size: 0.9rem;
  }

  .view-certificate {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }

  .search-input {
    font-size: 0.85rem;
  }

  .search-button {
    font-size: 0.85rem;
    padding: 0.6rem 1rem;
  }

  .certificate-table h2 {
    font-size: 1.1rem;
  }

  th, td {
    padding: 0.5rem;
    font-size: 0.85rem;
  }

  .view-certificate {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }
}
</style>
