import { ethers } from 'ethers';

let provider;
let signer;
let contract;

export const connectWallet = async () => {
  if (window.ethereum) {
    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      provider = new ethers.providers.Web3Provider(window.ethereum);
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

export const initContract = async (contractAddress, contractABI) => {
  if (!signer) {
    await connectWallet();
  }
  contract = new ethers.Contract(contractAddress, contractABI, signer);
  console.log('Contrato inicializado:', contract.address);
  return contract;
};

export const getProvider = () => provider;
export const getSigner = () => signer;
export const getContract = () => contract;