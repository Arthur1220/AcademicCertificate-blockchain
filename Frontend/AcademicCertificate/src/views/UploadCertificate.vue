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
            placeholder="Código do Certificado (0x...)"
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
import { ref, onMounted } from "vue";
import { connectWallet, initContract, getSigner, getContract } from "../services/blockchain";
import api from "../services/api";
import { utils } from 'ethers';

export default {
  components: {
    Navbar,
  },
  setup() {
    // Estados reativos para o formulário e mensagens de feedback
    const certificateCode = ref("");
    const studentName = ref("");
    const issueDate = ref("");
    const file = ref(null);
    const loading = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");

    // Variáveis para armazenar objetos do ethers.js
    const signer = ref(null);
    const contract = ref(null);

    // Função para lidar com a mudança de arquivo
    const handleFileChange = (event) => {
      file.value = event.target.files[0];
    };

    // Função para inicializar a conexão com a blockchain
    const initBlockchainConnection = async () => {
      try {
        await connectWallet();
        signer.value = getSigner();
        await initContract();
        contract.value = getContract();
      } catch (error) {
        console.error("Erro ao inicializar blockchain:", error);
        errorMessage.value = "Erro ao conectar à blockchain.";
      }
    };

    // Inicializar a conexão quando o componente for montado
    onMounted(() => {
      initBlockchainConnection();
    });

    // Função para enviar o formulário
    const submitForm = async () => {
      // Resetar mensagens de feedback
      successMessage.value = "";
      errorMessage.value = "";

      // Validações no Frontend
      if (!certificateCode.value || !studentName.value || !issueDate.value || !file.value) {
        errorMessage.value = "Todos os campos são obrigatórios.";
        return;
      }

      // Verificar se o código do certificado está no formato correto (bytes32)
      // Deve começar com '0x' seguido de 64 caracteres hexadecimais
      const certificateCodePattern = /^0x[a-fA-F0-9]{64}$/;
      if (!certificateCodePattern.test(certificateCode.value)) {
        errorMessage.value = "Código do certificado inválido. Deve ser um hash hexadecimal de 32 bytes.";
        return;
      }

      // Verificar se a data de emissão não está no futuro
      const selectedDate = new Date(issueDate.value);
      const currentDate = new Date();
      if (selectedDate > currentDate) {
        errorMessage.value = "Data de emissão não pode estar no futuro.";
        return;
      }

      // Verificar o tipo e tamanho do arquivo (por exemplo, máximo de 5MB)
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
        successMessage.value = "";
        errorMessage.value = "";

        if (!signer.value || !contract.value) {
          throw new Error("Erro ao conectar à blockchain.");
        }

        // Assinar o código do certificado
        const signature = await signer.value.signMessage(certificateCode.value);

        // Interagir com o smart contract para registrar o certificado na blockchain
        const transaction = await contract.value.registerCertificate(
          certificateCode.value,
          studentName.value,
          Math.floor(selectedDate.getTime() / 1000)
        );

        successMessage.value = "Transação enviada. Aguardando confirmação...";
        console.log("Transação enviada:", transaction.hash);

        // Aguardar a confirmação da transação
        const receipt = await transaction.wait();

        if (receipt.status === 1) {
          // Preparar os dados para enviar ao backend
          const formData = new FormData();
          formData.append("certificate_code", certificateCode.value);
          formData.append("student_name", studentName.value);
          formData.append("issue_date", Math.floor(selectedDate.getTime() / 1000));
          formData.append("signature", signature);
          formData.append("user_address", await signer.value.getAddress());
          formData.append("transaction_hash", transaction.hash);
          formData.append("file", file.value);

          // Enviar os dados para o backend
          const response = await api.post("/register_certificate", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });

          if (response.data.status === "success") {
            successMessage.value = "Certificado registrado com sucesso na blockchain e no banco de dados!";
            // Resetar o formulário
            certificateCode.value = "";
            studentName.value = "";
            issueDate.value = "";
            file.value = null;
          } else {
            throw new Error(response.data.message || "Erro ao registrar certificado no backend.");
          }
        } else {
          throw new Error("Transação falhou na blockchain.");
        }
      } catch (error) {
        console.error("Erro ao enviar certificado:", error);
        if (error.code === "UNPREDICTABLE_GAS_LIMIT") {
          errorMessage.value = "Limite de gas imprevisível. Tente novamente.";
        } else if (error.code === 4001) { // Erro de rejeição pelo usuário
          errorMessage.value = "Transação rejeitada pelo usuário.";
        } else {
          errorMessage.value = error.message || "Erro ao enviar certificado.";
        }
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
/* Estilos similares ao login */
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