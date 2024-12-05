<template>
    <div class="certificate-upload">
      
  
      <main class="main-content">
        <h2 class="title">Certifique seus documentos academicos aqui</h2>
        
        <div class="certificates-list">
          <div class="certificate-item" @click="handleCertificateClick('certificado')">
            <span class="certificate-name">Certificado.pdf</span>
            <span class="status-icon" :class="{ 'uploaded': certificateStatus.certificado }">✓</span>
          </div>
        </div>
  
        <input 
          type="file" 
          ref="certificadoInput"
          @change="handleFileUpload('certificado', $event)"
          accept=".pdf"
          style="display: none"
        >
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CertificateUpload',
    data() {
      return {
        certificateStatus: {
          certificado: false
        }
      }
    },
    handleFileUpload(type, event) {
      const file = event.target.files[0]
      if (file) {
        this.certificateStatus[type] = true
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
  
  .certificates-list {
    background-color: #1a1a1a;
    border-radius: 8px;
    padding: 2rem;
  }
  
  .certificate-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s;
    border-radius: 4px;
  }
  
  .certificate-item:hover {
    background-color: #333;
  }
  
  .certificate-name {
    font-size: 1rem;
  }
  
  .status-icon {
    width: 20px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: #333;
    color: transparent;
    font-size: 0.8rem;
  }
  
  .status-icon.uploaded {
    background-color: #4CAF50;
    color: white;
  }
  </style>
