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
          <label for="certificate_code">Código do Certificado</label>
          <input
            type="text"
            id="certificate_code"
            v-model="certificateCode"
            placeholder="Código do Certificado"
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
import { ref } from "vue";
import { ethers } from "ethers";
import axios from "axios";

export default {
  components: {
    Navbar,
  },
  setup() {
    const certificateCode = ref("");
    const studentName = ref("");
    const issueDate = ref("");
    const file = ref(null);
    const loading = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");

    const handleFileChange = (event) => {
      file.value = event.target.files[0];
    };

    const submitForm = async () => {
      if (!certificateCode.value || !studentName.value || !issueDate.value || !file.value) {
        errorMessage.value = "Todos os campos são obrigatórios.";
        return;
      }

      try {
        loading.value = true;
        successMessage.value = "";
        errorMessage.value = "";

        // Configurar provider e signer para blockchain
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();

        // Assinar o hash do certificado
        const signature = await signer.signMessage(certificateCode.value);

        // Interagir com o contrato inteligente
        const contractAddress = "SEU_ENDEREÇO_DO_CONTRATO";
        const contractABI = []; // Insira a ABI do seu contrato
        const contract = new ethers.Contract(contractAddress, contractABI, signer);

        const transaction = await contract.registerCertificate(
          certificateCode.value,
          studentName.value,
          Math.floor(new Date(issueDate.value).getTime() / 1000),
          await signer.getAddress()
        );

        successMessage.value = "Transação enviada. Aguardando confirmação...";
        await transaction.wait();

        // Preparar os dados para o backend
        const formData = new FormData();
        formData.append("certificate_code", certificateCode.value);
        formData.append("student_name", studentName.value);
        formData.append("issue_date", Math.floor(new Date(issueDate.value).getTime() / 1000));
        formData.append("signature", signature);
        formData.append("user_address", await signer.getAddress());
        formData.append("transaction_hash", transaction.hash);
        formData.append("file", file.value);

        // Enviar para o backend
        const response = await axios.post("http://127.0.0.1:5000/register_certificate", formData);

        if (response.data.status === "success") {
          successMessage.value = "Certificado registrado com sucesso!";
          certificateCode.value = "";
          studentName.value = "";
          issueDate.value = "";
          file.value = null;
        } else {
          throw new Error(response.data.message || "Erro ao registrar certificado.");
        }
      } catch (error) {
        console.error(error);
        errorMessage.value = error.message || "Erro ao enviar certificado.";
      } finally {
        loading.value = false;
      }
    };

    return {
      certificateCode,
      studentName,
      issueDate,
      file,
      loading,
      successMessage,
      errorMessage,
      handleFileChange,
      submitForm,
    };
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
