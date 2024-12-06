<template>
  <div class="main">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <div class="container">
      <h1>Carregue Seus Certificados Aqui!</h1>

      <!-- Upload Form -->
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

      <!-- Feedback Messages -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="formData">{{ formData }}</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/NavBar.vue";
import { ref } from "vue";
import {
  connectWallet,
  initContract,
  getSigner,
  getContract,
} from "../services/blockchain";
import { contractABI, contractAddress } from "../config";
import { ethers } from "ethers";

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

    const signer = ref(null);
    const contract = ref(null);

    const handleFileChange = (event) => {
      file.value = event.target.files[0];
    };

    const initBlockchainConnection = async () => {
      try {
        await connectWallet();
        signer.value = getSigner();
        await initContract(contractAddress, contractABI);
        contract.value = getContract();
        console.log("Blockchain conectado com sucesso.");
      } catch (error) {
        console.error("Erro ao inicializar blockchain:", error);
        errorMessage.value = "Erro ao conectar à blockchain.";
      }
    };

    // Inicializa a conexão com a blockchain quando o componente é montado
    initBlockchainConnection();

    const submitForm = async () => {
      // Resetar mensagens de feedback
      successMessage.value = "";
      errorMessage.value = "";

      // Validação dos campos do formulário
      if (
        !certificateCode.value ||
        !studentName.value ||
        !issueDate.value ||
        !file.value
      ) {
        errorMessage.value = "Todos os campos são obrigatórios.";
        return;
      }

      // Validar a data de emissão
      const selectedDate = new Date(issueDate.value);
      const currentDate = new Date();
      if (selectedDate > currentDate) {
        errorMessage.value = "Data de emissão não pode estar no futuro.";
        return;
      }

      // Validar o tipo e tamanho do arquivo
      const allowedTypes = ["application/pdf", "image/jpeg", "image/png"];
      if (!allowedTypes.includes(file.value.type)) {
        errorMessage.value = "Tipos de arquivo permitidos: PDF, JPEG, PNG.";
        return;
      }

      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.value.size > maxSize) {
        errorMessage.value = "O tamanho do arquivo excede 5MB.";
        return;
      }

      try {
        loading.value = true;

        if (!signer.value || !contract.value) {
          throw new Error("Erro ao conectar à blockchain.");
        }

        // Converter o código do certificado para bytes32
        const certificateHash = ethers.utils.formatBytes32String(
          certificateCode.value
        );

        // Converter a data de emissão para timestamp UNIX (em segundos)
        const issueTimestamp = Math.floor(selectedDate.getTime() / 1000);

        // Chamar a função registerCertificate do contrato inteligente
        const transaction = await contract.value.registerCertificate(
          certificateHash,
          studentName.value,
          issueTimestamp,
          { gasLimit: 1000000 }
        );

        successMessage.value = "Transação enviada. Aguardando confirmação...";
        console.log("Transação enviada:", transaction.hash);

        // Aguardar a confirmação da transação
        const receipt = await transaction.wait();

        if (receipt.status === 1) {
          successMessage.value =
            "Certificado registrado com sucesso na blockchain!";
          // Limpar os campos do formulário

          const formData = new FormData();
          formData.append("certificate_code", certificateCode.value);
          formData.append("student_name", studentName.value);
          formData.append("issue_date", Math.floor(selectedDate.getTime() / 1000));
          formData.append("file", file.value);
          formData.append("transaction_hash", transaction.hash);
          formData.append("user_address", localStorage.getItem('chave'));

          // Enviar dados para o back-end
          const response = await api.post("/register_certificate", formData);

          certificateCode.value = "";
          studentName.value = "";
          issueDate.value = "";
          file.value = null;

          alert(response);
        } else {
          throw new Error("Transação falhou na blockchain.");
        }
      } catch (error) {
        console.error("Erro ao registrar certificado:", error);
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
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Lucida Sans", sans-serif;
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

/* Form */
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

/* Submit Button */
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

/* Hover Effect */
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

/* Responsiveness */
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