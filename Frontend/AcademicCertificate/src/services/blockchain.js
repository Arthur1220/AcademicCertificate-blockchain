// src/services/blockchain.js
import { ethers } from 'ethers';

let provider;
let signer;
let contract;

// Função para conectar a carteira
export const connectWallet = async () => {
  if (window.ethereum) {
    try {
      // Solicita a conexão com a carteira
      await window.ethereum.request({ method: 'eth_requestAccounts' });

      // Inicializa o provider usando ethers.js v5
      provider = new ethers.providers.Web3Provider(window.ethereum);

      // Obtém o signer
      signer = provider.getSigner();

      console.log('Carteira conectada:', await signer.getAddress());
      return signer;
    } catch (error) {
      console.error('Erro ao conectar a carteira:', error);
      throw error;
    }
  } else {
    alert('Por favor, instale o MetaMask!');
    throw new Error('MetaMask não encontrado');
  }
};

// Função para inicializar o contrato
export const initContract = async (contractAddress, contractABI) => {
  if (!signer) {
    await connectWallet();
  }
  contract = new ethers.Contract(contractAddress, contractABI, signer);
  console.log('Contrato inicializado:', contract.address);
  return contract;
};

// Getters
export const getProvider = () => provider;
export const getSigner = () => signer;
export const getContract = () => contract;
