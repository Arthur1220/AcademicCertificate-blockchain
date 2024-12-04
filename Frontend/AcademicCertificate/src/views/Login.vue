<template>
  <div class="main">
    <div class="container">
      <h1>Login</h1>
      <button @click="connectWallet">{{ isConnected ? `Conectado: ${shortAddress}` : 'Conectar MetaMask' }}</button>
      <p v-if="error" style="color: red;">Erro: {{ error }}</p>
    </div>
  </div>
  
</template>

<style scoped>
  * {
    margin: 0;
    padding: 0;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    font-size: 1rem;
  }
  .main {
    display: flex;
    justify-content: center;
    height: 100%;
    width: 100%;
  }
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 500px;
    width: 500px;
    background-color: #333;
    margin-top: 200px;
    border-radius: 10px;
  }

  .container h1 {
    display: flex;
    justify-content: center;
    margin-top: 50px;
    color: white;
    font-size: 3rem;
    margin-bottom: 100px;
  }

  .container input {
    display: flex;
    margin-top: 80px;
    margin-bottom: 100px;
    width: 300px;
    height: 50px;
    background-color: #acacac;
    border: none;
    border-radius: 10px;
    color: #000;
  }

  #input-text::placeholder {
    color: #000;
    font-size: 1rem;
  }

  .container button {
    height: 50px;
    width: 200px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    background-color: #4D6FF9;
    transition: background-color 0.3s ease;
    color: white;
  }

  .container p {
    margin-top: 20px;
  }

  .container button:hover {
    background-color: #1abc9c;
  }


</style>

<script>
  import { ref } from 'vue'
  import { ethers } from 'ethers'
  
  export default {
    name: 'ConnectWallet',
    setup() {
      const isConnected = ref(false)
      const account = ref('')
      const shortAddress = ref('')
  
      const connectWallet = async () => {
        if (window.ethereum) {
          try {
            const provider = new ethers.BrowserProvider(window.ethereum)
            const accounts = await provider.send('eth_requestAccounts', [])
            account.value = accounts[0]
            shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`
            isConnected.value = true
            localStorage.setItem('chave', account.value);
            router.push({name: "UploadCertificate"});
  
            // Ouvir mudanças na conta
            window.ethereum.on('accountsChanged', (accounts) => {
              if (accounts.length > 0) {
                account.value = accounts[0]
                shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`
              } else {
                isConnected.value = false
                account.value = ''
                shortAddress.value = ''
              }
            })
          } catch (error) {
            console.error('Erro ao conectar MetaMask:', error)
          }
        } else {
          alert('Por favor, instale o MetaMask!')
        }
      }
  
      return {
        isConnected,
        connectWallet,
        shortAddress
      }
    }
  }
  </script>
