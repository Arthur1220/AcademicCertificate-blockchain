<template>
  <div class="main">
    <!-- Navbar -->
    <Navbar />

    <!-- Conteúdo Principal -->
    <div class="container">
      <h1>Carregue Seus Certificados Aqui!</h1>

      <!-- Formulário de Upload -->
      <form @submit.prevent="submitForm" class="upload-form">
        <div class="form-group">
          <label for="certificate_hash">Hash do Certificado</label>
          <input
            type="text"
            id="certificate_hash"
            v-model="certificateHash"
            placeholder="Hash do certificado"
            required
          />
        </div>

        <div class="form-group">
          <label for="student_name">Nome do Estudante</label>
          <input
            type="text"
            id="student_name"
            v-model="studentName"
            placeholder="Nome do estudante"
            required
          />
        </div>

        <div class="form-group">
          <label for="issue_date">Data de Emissão</label>
          <input
            type="date"
            id="issue_date"
            v-model="issueDate"
            required
          />
        </div>

        <div class="form-group">
          <label for="file">Arquivo do Certificado</label>
          <input
            type="file"
            id="file"
            @change="handleFileChange"
            accept=".pdf, .jpg, .jpeg, .png"
            required
          />
        </div>

        <div class="form-group">
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? 'Enviando...' : 'Enviar Certificado' }}
          </button>
        </div>
      </form>

      <!-- Mensagens de Feedback -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/NavBar.vue";
import { mapActions, mapGetters } from 'vuex';

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      certificateHash: "",
      studentName: "",
      issueDate: "",
      file: null,
    };
  },
  computed: {
    ...mapGetters(['isLoading', 'getSuccessMessage', 'getErrorMessage']),
    loading() {
      return this.isLoading;
    },
    successMessage() {
      return this.getSuccessMessage;
    },
    errorMessage() {
      return this.getErrorMessage;
    },
  },
  methods: {
    ...mapActions(['registerCertificate']),
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    async submitForm() {
      // Validações no Frontend
      if (!this.certificateHash || !this.studentName || !this.issueDate || !this.file) {
        this.$store.commit('setErrorMessage', 'Todos os campos são obrigatórios.');
        return;
      }

      // Verificar se o hash está no formato correto (ajuste conforme necessário)
      const hashPattern = /^[0-9a-fA-F]{64}$/;
      if (!hashPattern.test(this.certificateHash)) {
        this.$store.commit('setErrorMessage', 'Hash do certificado inválido.');
        return;
      }

      // Verificar se a data de emissão não está no futuro
      const selectedDate = new Date(this.issueDate);
      const currentDate = new Date();
      if (selectedDate > currentDate) {
        this.$store.commit('setErrorMessage', 'Data de emissão não pode estar no futuro.');
        return;
      }

      // Verificar o tipo e tamanho do arquivo (por exemplo, máximo de 5MB)
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
      if (!allowedTypes.includes(this.file.type)) {
        this.$store.commit('setErrorMessage', 'Tipos de arquivo permitidos: PDF, JPEG, PNG.');
        return;
      }

      const maxSize = 5 * 1024 * 1024; // 5MB
      if (this.file.size > maxSize) {
        this.$store.commit('setErrorMessage', 'O tamanho do arquivo excede 5MB.');
        return;
      }

      try {
        // Iniciar o processo de envio
        this.$store.commit('setLoading', true);
        this.$store.commit('clearMessages');

        const signer = this.$store.getters.getSigner;
        const contract = this.$store.getters.getContract;

        if (!signer || !contract) {
          this.$store.commit('setErrorMessage', 'Carteira não conectada ou contrato não inicializado.');
          this.$store.commit('setLoading', false);
          return;
        }

        // Assinar o hash do certificado
        const signature = await signer.signMessage(this.certificateHash);

        // Interagir com o smart contract para registrar o certificado na blockchain
        const transaction = await contract.registerCertificate(
          this.certificateHash,
          this.studentName,
          Math.floor(new Date(this.issueDate).getTime() / 1000),
          await signer.getAddress()
        );

        // Informar ao usuário que a transação está sendo confirmada
        this.$store.commit('setSuccessMessage', 'Transação enviada. Aguardando confirmação...');

        // Aguardar a confirmação da transação
        const receipt = await transaction.wait();

        if (receipt.status === 1) {
          // Transação bem-sucedida
          this.$store.commit('setSuccessMessage', 'Certificado registrado na blockchain com sucesso!');

          // Preparar os dados para enviar ao backend
          const formData = new FormData();
          formData.append("certificate_hash", this.certificateHash);
          formData.append("student_name", this.studentName);
          formData.append("issue_date", Math.floor(new Date(this.issueDate).getTime() / 1000));
          formData.append("signature", signature);
          formData.append("user_address", await signer.getAddress());
          formData.append("transaction_hash", transaction.hash);
          formData.append("file", this.file);

          // Enviar os dados para o backend
          const response = await this.registerCertificate(formData);

          if (response.status === 'success') {
            this.$store.commit('setSuccessMessage', 'Certificado registrado com sucesso na blockchain e no banco de dados!');
            // Resetar o formulário
            this.certificateHash = '';
            this.studentName = '';
            this.issueDate = '';
            this.file = null;
          } else {
            this.$store.commit('setErrorMessage', response.message || 'Erro ao registrar certificado no backend.');
          }
        } else {
          // Transação falhou
          this.$store.commit('setErrorMessage', 'Transação falhou na blockchain.');
        }
      } catch (error) {
        console.error("Erro ao enviar certificado", error);
        this.$store.commit('setErrorMessage', 'Ocorreu um erro ao enviar o certificado.');
      } finally {
        this.$store.commit('setLoading', false);
      }
    },
  },
};
</script>

<style scoped>
/* Estilos Globais */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lucida Sans', sans-serif;
}

/* Main */
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

/* Container */
.container {
  max-width: 600px;
  width: 100%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-top: 20px;
  text-align: center;
}

.container h1 {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
}

/* Formulário */
.upload-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-form .form-group {
  text-align: left;
}

.upload-form .form-group label {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
  color: #333;
}

.upload-form .form-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

/* Botão de Enviar */
.upload-form .submit-btn {
  background-color: #4d6ff9;
  color: #fff;
  border: none;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  height: 50px;
  width: 200px; 
  margin: 0 auto;
  display: block;
}

/* Efeito Hover */
.upload-form .submit-btn:hover:not(:disabled) {
  background-color: #1abc9c;
  transform: scale(1.05);
}

.upload-form .submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-size: 0.9rem;
}

.success-message {
  color: green;
  margin-top: 10px;
  font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  .container h1 {
    font-size: 1.5rem;
  }

  .upload-form .form-group input {
    font-size: 0.9rem;
    padding: 8px;
  }

  .upload-form .submit-btn {
    padding: 10px;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .container h1 {
    font-size: 1.3rem;
  }

  .upload-form .form-group input {
    font-size: 0.8rem;
    padding: 6px;
  }

  .upload-form .submit-btn {
    padding: 8px;
    font-size: 0.9rem;
  }
}
</style>
