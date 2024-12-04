# Academic Certificate Blockchain

## **Introdução**

O **Academic Certificate Blockchain** é um sistema descentralizado desenvolvido em Solidity, utilizando o framework Hardhat e a biblioteca Ethers.js. Este sistema permite o registro, verificação e emissão de certificados acadêmicos de forma segura e transparente na blockchain. Além disso, oferece funcionalidades de administração para gerenciar as permissões e responsabilidades dentro do contrato inteligente.

## **Estrutura do Projeto**

A estrutura do projeto está organizada da seguinte forma:

```
Blockchain/
├── contracts/
│   └── AcademicCertificate.sol
├── scripts/
│   └── deploy.js
├── test/
│   └── AcademicCertificate.test.js
├── hardhat.config.js
├── package.json
└── README.md
```

### **1. contracts/**
- **AcademicCertificate.sol**: Contém o contrato inteligente principal que gerencia o registro e emissão de certificados, bem como a transferência de administração.

### **2. scripts/**
- **deploy.js**: Script responsável por compilar e fazer o deploy do contrato inteligente na rede especificada.

### **3. test/**
- **AcademicCertificate.test.js**: Conjunto de testes automatizados utilizando o framework Hardhat com Chai para garantir que todas as funcionalidades do contrato estão funcionando conforme o esperado.

### **4. hardhat.config.js**
Arquivo de configuração do Hardhat que define parâmetros como a versão do compilador Solidity, redes de blockchain a serem usadas e plugins utilizados.

### **5. package.json**
Gerencia as dependências do projeto, scripts de execução e metadados do projeto.

## **Funcionalidades do Contrato Inteligente**

O contrato **AcademicCertificate** oferece as seguintes funcionalidades:

1. **Emissão de Certificados**
   - **Qualquer pessoa** pode emitir certificados acadêmicos únicos, identificados por um hash.
   - Evita a emissão de certificados duplicados utilizando hashes únicos.

2. **Consulta de Certificados**
   - Permite a qualquer pessoa consultar os detalhes de um certificado utilizando seu hash ou o nome do estudante.
   - Retorna todos os certificados registrados para um determinado nome de estudante.

3. **Administração**
   - O administrador pode transferir suas responsabilidades para outro endereço.
   - Assegura que apenas o administrador pode executar funções administrativas.
   - Previne a transferência de administração para o endereço zero.

## **Como Executar o Sistema**

Siga os passos abaixo para configurar, compilar, testar e interagir com o contrato inteligente.

### **1. Pré-requisitos**

- **Node.js**: Certifique-se de ter o Node.js instalado. Você pode baixar na [página oficial](https://nodejs.org/).
- **Git**: Necessário para clonar o repositório. Baixe na [página oficial](https://git-scm.com/).

### **2. Clone o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd Blockchain
```

### **3. Instale as Dependências**

Execute o seguinte comando para instalar todas as dependências necessárias:

```bash
npm install
```

### **4. Compile os Contratos Inteligentes**

Para compilar os contratos Solidity, execute:

```bash
npx hardhat compile
```

### **5. Execute os Testes Automatizados**

Antes de fazer o deploy, é importante garantir que todos os testes passem com sucesso:

```bash
npx hardhat test
```

**Saída Esperada:**

```
  AcademicCertificate Contract
    Deployment
      ✔ Deve definir o admin corretamente
    Register Certificate
      ✔ Deve permitir que qualquer pessoa registre um certificado
      ✔ Não deve permitir registrar um certificado com hash inválido (0x0)
      ✔ Não deve permitir registrar um certificado com nome vazio
      ✔ Não deve permitir registrar um certificado com data de emissão inválida (0)
      ✔ Não deve permitir registrar o mesmo certificado duas vezes
    Get Certificate
      ✔ Deve retornar os detalhes de um certificado existente
      ✔ Não deve retornar detalhes para um certificado inexistente
    Transfer Admin
      ✔ Deve permitir que o admin transfira sua função para outro endereço
      ✔ Não deve permitir que não-admins transfiram a função de admin
      ✔ Não deve permitir transferir admin para o endereço zero


  11 passing (3s)
```

### **6. Fazer o Deploy do Contrato na Rede Local**

Para testar o contrato em uma rede local, utilize o Hardhat Network.

1. **Inicie a Rede Local:**

   Em um terminal separado, execute:

   ```bash
   npx hardhat node
   ```

   Isso iniciará uma instância local da blockchain.

2. **Deploy do Contrato:**

   Em outro terminal, execute o script de deploy:

   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

   **Saída Esperada:**

   ```
   Deploying contracts with the account: 0x...
   Account balance: X ETH
   AcademicCertificate deployed to: 0x...
   ```

## **Considerações Finais**

O **Academic Certificate Blockchain** oferece uma solução robusta e segura para a gestão de certificados acadêmicos, aproveitando os benefícios da tecnologia blockchain, como transparência, imutabilidade e descentralização. Com a estrutura modular e as funcionalidades implementadas, o sistema pode ser adaptado e expandido conforme as necessidades dos usuários finais.