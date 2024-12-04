<template>
  <div class="main">
    <div class="container">
      <h1>Login</h1>
      <input
        id="input-text"
        v-model="address"
        type="text"
        placeholder="Insira o endereço da carteira"
      />
      <button @click="fetchBalance">Acessar sua conta</button>
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

<script lang="ts">
import { defineComponent } from "vue";
import { JsonRpcProvider, isAddress, formatEther } from "ethers";
import router from "@/router";

export default defineComponent({
  name: "WalletBalance",
  data() {
    return {
      address: "", // Armazena o endereço da carteira inserido pelo usuário
      balance: null as string | null, // Armazena o saldo da carteira
      error: null as string | null, // Armazena mensagens de erro
    };
  },
  methods: {
    async fetchBalance() {
      const provider = new JsonRpcProvider("https://mainnet.infura.io/v3/c3c237f677734889a07124571f56d377");

      try {
        // Valida o endereço inserido pelo usuário
        if (!isAddress(this.address)) {
          throw new Error("Endereço inválido.");
        }

        // Obtem o saldo em Wei e converte para Ether
        const balanceWei = await provider.getBalance(this.address);
        this.balance = formatEther(balanceWei);
        this.error = null; // Limpa mensagens de erro

        if (this.balance) {
          router.push("/");
        }
      } catch (err) {
        this.error = (err as Error).message; // Exibe a mensagem de erro
        this.balance = null; // Limpa o saldo
      }
    },
  },
});
</script>
