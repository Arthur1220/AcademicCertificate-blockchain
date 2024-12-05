import { createStore } from 'vuex';
import { connectWallet, initContract, getContract } from '@/services/blockchain';
import api from '@/services/api';
import contractABI from '@/abis/AcademicCertificate.json';

export default createStore({
  state: {
    signer: null,
    contract: null,
    certificates: []
  },
  mutations: {
    setSigner(state, signer) {
      state.signer = signer;
    },
    setContract(state, contract) {
      state.contract = contract;
    },
    setCertificates(state, certificates) {
      state.certificates = certificates;
    }
  },
  actions: {
    async connect({ commit }) {
      try {
        const signer = await connectWallet();
        commit('setSigner', signer);

        const contractAddress = '0x5FbDB2315678afecb367f032d93F642f64180aa3'; // Substitua pelo endereço real
        const contract = await initContract(contractAddress, contractABI.abi);
        commit('setContract', contract);
      } catch (error) {
        console.error(error);
      }
    },
    async registerCertificate({ state }, certificateData) {
      try {
        if (!state.contract) {
          throw new Error('Contrato não inicializado');
        }

        const transaction = await state.contract.emitCertificate(
          certificateData.certificate_code,
          certificateData.student_name,
          certificateData.issue_date,
          certificateData.user_address
        );

        await transaction.wait();

        const response = await api.post('/register_certificate', certificateData);

        return response.data;
      } catch (error) {
        console.error('Erro ao registrar certificado:', error);
        throw error;
      }
    },
    async fetchCertificateByCode({ commit }, certificateCode) {
      try {
        const response = await api.get(`/get_certificate?certificate_code=${certificateCode}`);

        if (response.data.status === 'success') {
          commit('setCertificates', [response.data.certificate]);
        } else {
          console.error('Erro:', response.data.message);
        }
      } catch (error) {
        console.error('Erro ao buscar certificado:', error);
      }
    },
    async fetchCertificatesByStudentName({ commit }, studentName) {
      try {
        const response = await api.get(`/get_certificate?student_name=${encodeURIComponent(studentName)}`);

        if (response.data.status === 'success') {
          commit('setCertificates', response.data.certificates);
        } else {
          console.error('Erro:', response.data.message);
        }
      } catch (error) {
        console.error('Erro ao buscar certificados:', error);
      }
    }
  },
  getters: {
    getCertificates(state) {
      return state.certificates;
    }
  },
  modules: {}
});