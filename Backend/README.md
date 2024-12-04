# Academic Certificate Backend

## Visão Geral

Este repositório contém o **componente backend** do projeto Blockchain de Certificados. O backend é construído usando **Flask** e integra-se com uma **rede blockchain Ethereum** para registrar e verificar certificados acadêmicos. O objetivo principal é fornecer uma maneira segura e imutável de armazenar e verificar credenciais acadêmicas usando tecnologia blockchain.

## Funcionalidades

- **Registro de Certificados**: **Qualquer pessoa** pode registrar novos certificados na blockchain.
- **Verificação de Certificados**: Usuários podem verificar a autenticidade de um certificado.
- **Busca de Certificados**: É possível buscar certificados pelo hash específico ou pelo nome do estudante, retornando todos os certificados registrados com aquele nome.
- **Gerenciamento de Administradores**: O administrador pode transferir privilégios de administração para outro endereço.

## Arquitetura

O backend serve como intermediário entre a aplicação frontend e a blockchain. Ele expõe endpoints de API RESTful que o frontend pode consumir para realizar ações como registrar certificados e buscar detalhes de certificados.

O backend se comunica com a blockchain Ethereum usando o **Web3.py**. Funções de contratos inteligentes são chamadas para interagir com a blockchain, garantindo que todos os dados de certificados sejam armazenados com segurança e de forma imutável.

## Configuração e Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Virtualenv
- Node.js e npm (para o frontend)
- Um nó Ethereum ou provedor (por exemplo, Ganache, Hardhat, Infura)
- Compilador Solidity (se precisar compilar contratos inteligentes)

### Clonar o Repositório

```bash
git clone https://github.com/Arthur1220/AcademicCertificate-blockchain
cd CertificateBlockchain/Backend
```

### Criar um Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows use 'venv\Scripts\activate'
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Configuração

Crie um arquivo `.env` no diretório `Backend` com o seguinte conteúdo:

```ini
# Configuração da Rede Ethereum
CONTRACT_ADDRESS=0xSeuEnderecoDoContrato
ADMIN_ADDRESS=0xSeuEnderecoAdmin
ADMIN_PRIVATE_KEY=SuaChavePrivadaAdmin
BLOCKCHAIN_URL=http://127.0.0.1:8545  # ou o URL do seu provedor
CONTRACT_ABI_PATH=./app/abis/AcademicCertificate.json

# Configuração do Banco de Dados
DATABASE_URI=sqlite:///certificates.db

# Caminho de Armazenamento
STORAGE_PATH=./storage
```

**Importante:** Nunca faça commit das suas chaves privadas ou informações sensíveis no controle de versão.

### Inicializar o Banco de Dados

```bash
flask db upgrade
```

### Executar a Aplicação

```bash
python run.py
```

A aplicação será iniciada em `http://localhost:5000`.

## Endpoints da API

### 1. Registrar Certificado

- **Endpoint:** `/register_certificate`
- **Método:** `POST`
- **Descrição:** Registra um novo certificado na blockchain.
- **Corpo da Requisição (Form Data):**

  - `certificate_hash`: O hash do certificado.
  - `student_name`: Nome do estudante.
  - `issue_date`: Data de emissão em formato timestamp.
  - `issuer_private_key`: Chave privada do emissor (necessária para assinar a transação).
  - `file`: O arquivo do certificado (PDF ou imagem).

- **Exemplo de Requisição:**

  O arquivo e os dados devem ser enviados como `multipart/form-data`.

- **Resposta:**

  ```json
  {
    "status": "success",
    "transaction_hash": "0xTransactionHash",
    "file_path": "/caminho/para/arquivo/armazenado"
  }
  ```

### 2. Obter Certificado

- **Endpoint:** `/get_certificate`
- **Método:** `GET`
- **Descrição:** Recupera os detalhes de um certificado. Pode buscar por `certificate_hash` ou `student_name` como parâmetros de consulta.
- **Parâmetros de Consulta:**

  - `certificate_hash` (opcional): O hash do certificado.
  - `student_name` (opcional): Nome do estudante.

  **Nota:** É necessário fornecer pelo menos um dos parâmetros.

- **Exemplo de Requisição:**

  - Por `certificate_hash`:

    ```
    GET /get_certificate?certificate_hash=0xSeuCertificateHash
    ```

  - Por `student_name`:

    ```
    GET /get_certificate?student_name=Nome%20do%20Estudante
    ```

- **Resposta ao Buscar por `certificate_hash`:**

  ```json
  {
    "status": "success",
    "certificate": {
      "student_name": "Nome do Estudante",
      "issue_date": 1700000000,
      "issuer_address": "0xEnderecoDoEmissor",
      "file_path": "/caminho/para/arquivo/armazenado"
    }
  }
  ```

- **Resposta ao Buscar por `student_name`:**

  ```json
  {
    "status": "success",
    "certificates": [
      {
        "student_name": "Nome do Estudante",
        "issue_date": 1700000000,
        "issuer_address": "0xEnderecoDoEmissor",
        "file_path": "/caminho/para/arquivo/armazenado"
      },
      {
        "student_name": "Nome do Estudante",
        "issue_date": 1700001000,
        "issuer_address": "0xOutroEnderecoDoEmissor",
        "file_path": "/caminho/para/arquivo/armazenado2"
      }
    ]
  }
  ```

### 3. Transferir Admin

- **Endpoint:** `/transfer_admin`
- **Método:** `POST`
- **Descrição:** Transfere privilégios de administrador para outro endereço.
- **Corpo da Requisição (JSON):**

  ```json
  {
    "new_admin_address": "0xNovoEnderecoAdmin"
  }
  ```

- **Resposta:**

  ```json
  {
    "status": "success",
    "transaction_hash": "0xTransactionHash"
  }
  ```

## Conectando ao Frontend (Vue.js)

Para conectar o backend com um frontend em Vue.js, você pode seguir estes passos após criar o projeto e fazer a configuração base do Axios:

### 1. Configurar o Projeto Frontend

```bash
vue create frontend
cd frontend
```

### 2. Instalar o Axios

```bash
npm install axios
```

### 3. Configurar o Axios

Crie uma instância do Axios apontando para a API do backend:

```javascript
// src/api/axios.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
});

export default api;
```

### 4. Consumir os Endpoints da API

Use a instância do Axios para fazer requisições à API do backend. Por exemplo, para registrar um certificado:

```javascript
// src/components/RegisterCertificate.vue
<template>
  <!-- Seu código de template -->
</template>

<script>
import api from '../api/axios';

export default {
  data() {
    return {
      certificateData: {
        certificate_hash: '',
        student_name: '',
        issue_date: '',
        issuer_private_key: '',
        file: null,
      },
    };
  },
  methods: {
    async registerCertificate() {
      const formData = new FormData();
      formData.append('certificate_hash', this.certificateData.certificate_hash);
      formData.append('student_name', this.certificateData.student_name);
      formData.append('issue_date', this.certificateData.issue_date);
      formData.append('issuer_private_key', this.certificateData.issuer_private_key);
      formData.append('file', this.certificateData.file);

      try {
        const response = await api.post('/register_certificate', formData);
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style>
/* Suas estilizações */
</style>
```

### 5. Manipulando Respostas

O backend envia respostas em JSON, então você pode manipulá-las em seus componentes Vue.js de acordo.

## Testes

O backend usa o **Pytest** para testes unitários. Para executar os testes:

```bash
pytest
```

Certifique-se de que todos os testes passam antes de implantar ou fazer alterações.