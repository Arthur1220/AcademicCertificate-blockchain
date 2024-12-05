<template>
  <div class="main">
    <div class="container">
      <h1>Login</h1>
      <p class="description">
        Clique no botão abaixo para conectar sua carteira MetaMask. Uma extensão será aberta para autorizar e realizar o login.
      </p>
      <button @click="connectWallet">
        {{ isConnected ? `Conectando...` : 'Conectar MetaMask' }}
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
/* Reset Global */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lucida Sans', sans-serif;
}

/* Estilo Principal */
.main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
}

/* Container */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.container h1 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

.description {
  color: #666;
  font-size: 1rem;
  margin-bottom: 20px;
}

.container button {
  height: 50px;
  width: 100%;
  max-width: 250px;
  background-color: #4D6FF9;
  border: none;
  border-radius: 30px;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  height: 50px;
  width: 200px;
}

.container button:hover {
  background-color: #1abc9c;
}

.error-message {
  color: red;
  margin-top: 10px;
  font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .container {
    padding: 20px;
    width: 95%;
  }

  .container h1 {
    font-size: 1.8rem;
  }

  .description {
    font-size: 0.95rem;
  }

  .container button {
    height: 45px;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .container h1 {
    font-size: 1.5rem;
  }

  .description {
    font-size: 0.9rem;
  }

  .container button {
    height: 40px;
    font-size: 0.9rem;
  }
}
</style>

<script>
import { ref } from 'vue';
import { ethers } from 'ethers';
import { useRouter } from 'vue-router';

export default {
  name: 'ConnectWallet',
  setup() {
    const isConnected = ref(false);
    const account = ref('');
    const shortAddress = ref('');
    const router = useRouter();
    const errorMessage = ref('');

    const connectWallet = async () => {
      if (window.ethereum) {
        try {
          const provider = new ethers.BrowserProvider(window.ethereum);
          const accounts = await provider.send('eth_requestAccounts', []);
          account.value = accounts[0];
          shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`;
          isConnected.value = true;
          localStorage.setItem('chave', shortAddress.value);
          setTimeout(() => {
            router.push({ name: 'UploadCertificate' });
          }, 2000);

          // Ouvir mudanças na conta
          window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length > 0) {
              account.value = accounts[0];
              shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`;
            } else {
              isConnected.value = false;
              account.value = '';
              shortAddress.value = '';
            }
          });
        } catch (error) {
          // Tratamento de erros
          if (error.code === 4001) {
            console.error('Conexão rejeitada pelo usuário.');
            errorMessage.value = 'Você rejeitou a conexão. Por favor, tente novamente.';
          } else if (error.code === -32002) {
            console.error('Solicitação de conexão já pendente.');
            errorMessage.value = 'Já existe uma solicitação de conexão pendente. Verifique sua extensão MetaMask.';
          } else if (error.code === -32603) {
            console.error('Erro interno no MetaMask.');
            errorMessage.value = 'Erro interno no MetaMask. Por favor, reinicie sua carteira e tente novamente.';
          } else {
            console.error('Erro desconhecido:', error);
            errorMessage.value = 'Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.';
          }
        }
      } else {
        alert('Por favor, instale o MetaMask!');
      }
    };

    return {
      isConnected,
      connectWallet,
      shortAddress,
      errorMessage,
    };
  },
};
</script>
