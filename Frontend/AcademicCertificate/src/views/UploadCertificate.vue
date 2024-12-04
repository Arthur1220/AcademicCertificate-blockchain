<template>
    <div>
      <!-- Importando e utilizando a Navbar -->
      <Navbar />
  
      <!-- Título -->
      <div class="container">
        <h1>Carregue Seus Certificados Aqui!</h1>
  
        <!-- Formulário de Upload -->
        <form @submit.prevent="submitForm" class="upload-form">
          <div class="form-group">
            <label for="certificate_hash">Hash do Certificado</label>
            <input type="text" id="certificate_hash" v-model="certificateHash" placeholder="Hash do certificado" required />
          </div>
  
          <div class="form-group">
            <label for="student_name">Nome do Estudante</label>
            <input type="text" id="student_name" v-model="studentName" placeholder="Nome do estudante" required />
          </div>
  
          <div class="form-group">
            <label for="issue_date">Data de Emissão</label>
            <input type="date" id="issue_date" v-model="issueDate" required />
          </div>
  
          <div class="form-group">
            <label for="file">Arquivo do Certificado</label>
            <input type="file" id="file" @change="handleFileChange" accept=".pdf, .jpg, .jpeg, .png" required />
          </div>
  
          <div class="form-group">
            <button type="submit" class="submit-btn">Enviar</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
import Navbar from '../components/NavBar.vue';
import axios from 'axios';
import { ethers } from 'ethers';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      certificateHash: '',
      studentName: '',
      issueDate: '',
      file: null,
    };
  },
  methods: {
    async signMessage(message) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const signature = await signer.signMessage(message);
        return signature;
      } catch (error) {
        console.error('Erro ao assinar a mensagem:', error);
        throw error;
      }
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    async submitForm() {
      try {
        const signature = await this.signMessage(this.certificateHash);

        const formData = new FormData();
        formData.append('certificate_hash', this.certificateHash);
        formData.append('student_name', this.studentName);
        formData.append('issue_date', Math.floor(new Date(this.issueDate).getTime() / 1000));
        formData.append('signature', signature);
        formData.append('file', this.file);

        const response = await axios.post('http://127.0.0.1:5000/register_certificate', formData);
        console.log('Certificado enviado com sucesso', response.data);
      } catch (error) {
        console.error('Erro ao enviar certificado', error);
      }
    }
  }
};
</script>
  
  <style scoped>
  /* Estilos para o layout e formulário */
  .container {
    max-width: 600px;
    margin: 80px auto; /* Adicionando margem superior para distanciar da navbar */
    padding: 30px; /* Aumentando o padding para distanciar os campos da borda */
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border: 2px solid #aaa; /* Borda com cor cinza clara */
  }
  
  .container h1 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .upload-form {
    display: flex;
    flex-direction: column;
  }
  
  .upload-form .form-group {
    margin-bottom: 20px;
  }
  
  .upload-form .form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .upload-form .form-group input {
    width: 95%;
    padding: 12px; /* Aumentando o padding para criar espaçamento interno */
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 5px; /* Adicionando espaçamento entre o label e o input */
  }
  
  .upload-form .submit-btn {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 15px;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .upload-form .submit-btn:hover {
    background-color: #218838;
  }
  </style>