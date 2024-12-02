# Academic Certificate Backend

## Visão Geral

Este repositório contém o **componente backend** do projeto Blockchain de Certificados. O backend é construído usando **Flask** e integra-se com uma **rede blockchain Ethereum** para registrar e verificar certificados acadêmicos. O objetivo principal é fornecer uma maneira segura e imutável de armazenar e verificar credenciais acadêmicas usando tecnologia blockchain.

## Funcionalidades

- **Registro de Certificados**: Instituições podem registrar novos certificados na blockchain.
- **Verificação de Certificados**: Usuários podem verificar a autenticidade de um certificado.
- **Registro de Instituições**: Novas instituições podem ser registradas e verificadas.
- **Gerenciamento de Administradores**: O administrador pode transferir privilégios de administração para outro endereço.

## Arquitetura

O backend serve como intermediário entre a aplicação frontend e a blockchain. Ele expõe endpoints de API RESTful que o frontend pode consumir para realizar ações como registrar certificados, verificar instituições e buscar detalhes de certificados.

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
git clone https://github.com/seuusuario/CertificateBlockchain.git
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

### 1. Registrar Instituição

- **Endpoint:** `/register_institution`
- **Método:** `POST`
- **Descrição:** Registra uma nova instituição na blockchain.
- **Corpo da Requisição (JSON):**

  ```json
  {
    "name": "Nome da Instituição",
    "cnpj": "12.345.678/0001-90",
    "responsible": "Pessoa Responsável"
  }
  ```

- **Resposta:**

  ```json
  {
    "status": "success",
    "transaction_hash": "0xTransactionHash"
  }
  ```

### 2. Verificar Instituição

- **Endpoint:** `/verify_institution`
- **Método:** `POST`
- **Descrição:** Verifica uma instituição (apenas admin).
- **Corpo da Requisição (JSON):**

  ```json
  {
    "institution_address": "0xEnderecoDaInstituicao"
  }
  ```

- **Resposta:**

  ```json
  {
    "status": "success",
    "transaction_hash": "0xTransactionHash"
  }
  ```

### 3. Registrar Certificado

- **Endpoint:** `/register_certificate`
- **Método:** `POST`
- **Descrição:** Registra um novo certificado.
- **Corpo da Requisição (Form Data):**

  - `certificate_hash`: O hash do certificado.
  - `student_name`: Nome do estudante.
  - `issue_date`: Data de emissão em formato timestamp.
  - `institution_address`: Endereço Ethereum da instituição.
  - `file`: O arquivo do certificado (PDF ou imagem).

- **Resposta:**

  ```json
  {
    "status": "success",
    "transaction_hash": "0xTransactionHash",
    "file_path": "/caminho/para/arquivo/armazenado"
  }
  ```

### 4. Obter Certificado

- **Endpoint:** `/get_certificate/<certificate_hash>`
- **Método:** `GET`
- **Descrição:** Recupera os detalhes de um certificado.
- **Resposta:**

  ```json
  {
    "status": "success",
    "certificate": {
      "student_name": "Nome do Estudante",
      "issue_date": 1700000000,
      "institution_address": "0xEnderecoDaInstituicao",
      "file_path": "/caminho/para/arquivo/armazenado"
    }
  }
  ```

### 5. Transferir Admin

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

Para conectar o backend com um frontend em Vue.js, você pode seguir estes passos apos criar o projeto e fazer a configuração base do Axios:


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
        institution_address: '',
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
      formData.append('institution_address', this.certificateData.institution_address);
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