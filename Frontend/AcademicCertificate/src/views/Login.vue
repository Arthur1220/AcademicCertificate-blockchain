<template>
  <div class="main">
    <div class="container">
      <h1>Login</h1>
      <p class="description">
        Clique no botão abaixo para conectar sua carteira MetaMask. Uma extensão será aberta para autorizar e realizar o login.
      </p>
      
      <!-- Informações Adicionais sobre MetaMask -->
      <div class="additional-info">
        <h2>Por que usar a MetaMask?</h2>
        <ul>
          <li>
            <span class="icon" aria-hidden="true">🔒</span>
            <div>
              <strong>Segurança:</strong> Suas chaves privadas são armazenadas localmente, garantindo que você tenha controle total sobre seus ativos.
            </div>
          </li>
          <li>
            <span class="icon" aria-hidden="true">🔗</span>
            <div>
              <strong>Integração com Blockchain:</strong> Permite interações diretas com a blockchain, essencial para registrar e verificar certificados.
            </div>
          </li>
          <li>
            <span class="icon" aria-hidden="true">⚡</span>
            <div>
              <strong>Facilidade de Uso:</strong> Interface amigável para gerenciar suas transações e interações de forma simples e eficiente.
            </div>
          </li>
        </ul>
      </div>

      <!-- Botão de Conexão -->
      <button @click="connectWallet" :disabled="loading">
        {{ loading ? 'Conectando...' : 'Conectar MetaMask' }}
      </button>
      
      <!-- Mensagens de Sucesso e Erro -->
      <p v-if="shortAddress" class="success-message">Conectado: {{ shortAddress }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      
      <!-- Link para Instalar MetaMask -->
      <p class="install-link" v-if="!isMetaMaskInstalled">
        Não tem o MetaMask? 
        <a href="https://metamask.io/download/" target="_blank" rel="noopener">Instale aqui</a>.
      </p>
    </div>
  </div>
</template>

<script>
import { ref, onUnmounted } from 'vue';
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
    const loading = ref(false);
    const isMetaMaskInstalled = ref(false);
    let accountsChangedHandler = null;

    const connectWallet = async () => {
      if (window.ethereum) {
        isMetaMaskInstalled.value = true;
        try {
          loading.value = true;
          const provider = new ethers.providers.Web3Provider(window.ethereum);
          const accounts = await provider.send('eth_requestAccounts', []);
          account.value = accounts[0];
          shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`;
          isConnected.value = true;
          localStorage.setItem('address', account.value); // Armazena o endereço completo

          setTimeout(() => {
            router.push({ name: 'UploadCertificate' });
          }, 1500);

          // Ouvir mudanças na conta
          accountsChangedHandler = (accounts) => {
            if (accounts.length > 0) {
              account.value = accounts[0];
              shortAddress.value = `${account.value.slice(0, 6)}...${account.value.slice(-4)}`;
            } else {
              isConnected.value = false;
              account.value = '';
              shortAddress.value = '';
              localStorage.removeItem('address');
              router.push({ name: 'Login' }); // Redirecionar para login
            }
          };

          window.ethereum.on('accountsChanged', accountsChangedHandler);
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
        } finally {
          loading.value = false;
        }
      } else {
        isMetaMaskInstalled.value = false;
      }
    };

    // Verificar se MetaMask está instalado ao montar o componente
    isMetaMaskInstalled.value = typeof window.ethereum !== 'undefined' && window.ethereum.isMetaMask;

    // Remover o listener quando o componente for desmontado
    onUnmounted(() => {
      if (accountsChangedHandler) {
        window.ethereum.removeListener('accountsChanged', accountsChangedHandler);
      }
    });

    return {
      isConnected,
      connectWallet,
      shortAddress,
      errorMessage,
      loading,
      isMetaMaskInstalled,
    };
  },
};
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
.main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background-color: #fff; /* Correção da cor de fundo */
}

/* Container */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  width: 100%;
  max-width: 600px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Título */
.container h1 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

/* Descrição */
.description {
  color: #666;
  font-size: 1rem;
  margin-bottom: 20px;
}

/* Informações Adicionais */
.additional-info {
  width: 100%;
  text-align: left;
  margin-bottom: 20px;
}

.additional-info h2 {
  text-align: center;
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.additional-info ul {
  list-style: none;
  padding-left: 0;
}

.additional-info li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  color: #555;
}

.additional-info .icon {
  margin-right: 10px;
  font-size: 1.5rem;
  flex-shrink: 0;
  line-height: 1;
}

.additional-info li div {
  flex: 1;
}

.additional-info li strong {
  margin-right: 5px;
}

/* Botão */
.container button {
  height: 50px;
  width: 100%;
  max-width: 250px;
  background-color: #96FF7C;
  border: none;
  border-radius: 30px;
  color: black;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.container button:hover:not(:disabled) {
  background-color: #1abc9c;
}

.container button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Mensagens */
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

/* Link para Instalar MetaMask */
.install-link {
  margin-top: 15px;
  font-size: 0.9rem;
  color: #666;
}

.install-link a {
  color: #1abc9c;
  text-decoration: none;
}

.install-link a:hover {
  text-decoration: underline;
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

  .additional-info h2 {
    font-size: 1.1rem;
  }

  .additional-info li {
    font-size: 0.95rem;
  }

  .container button {
    height: 45px;
    font-size: 0.95rem;
    width: 180px;
  }
}

@media (max-width: 480px) {
  .container h1 {
    font-size: 1.5rem;
  }

  .description {
    font-size: 0.9rem;
  }

  .additional-info h2 {
    font-size: 1rem;
  }

  .additional-info li {
    font-size: 0.85rem;
  }

  .container button {
    height: 40px;
    font-size: 0.9rem;
    width: 160px;
  }

  .install-link {
    font-size: 0.8rem;
  }
}
</style>
