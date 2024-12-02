const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AcademicCertificate Contract", function () {
  let AcademicCertificate;
  let academicCertificate;
  let admin;
  let institution;
  let otherAccount;

  beforeEach(async function () {
    // Obtém as contas de teste
    [admin, institution, otherAccount] = await ethers.getSigners();

    // Obtém a factory e deploya o contrato
    AcademicCertificate = await ethers.getContractFactory("AcademicCertificate");
    academicCertificate = await AcademicCertificate.connect(admin).deploy();
    await academicCertificate.deployed();
  });

  describe("Deployment", function () {
    it("Deve definir o admin corretamente", async function () {
      expect(await academicCertificate.admin()).to.equal(admin.address);
    });
  });

  describe("Register Institution", function () {
    it("Deve permitir que uma instituição registre-se", async function () {
      await expect(
        academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana")
      )
        .to.emit(academicCertificate, "InstitutionRegistered")
        .withArgs(institution.address, "Instituição ABC");

      const registeredInstitution = await academicCertificate.institutions(institution.address);
      expect(registeredInstitution.name).to.equal("Instituição ABC");
      expect(registeredInstitution.cnpj).to.equal("98.765.432/0001-10");
      expect(registeredInstitution.responsible).to.equal("Prof. Ana");
      expect(registeredInstitution.isVerified).to.equal(false);
    });

    it("Não deve permitir que uma instituição já registrada seja registrada novamente", async function () {
      await academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana");
      
      await expect(
        academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana")
      ).to.be.revertedWith("Instituicao ja registrada.");
    });
  });

  describe("Verify Institution", function () {
    it("Deve permitir que o admin verifique uma instituição", async function () {
      await academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana");
      
      await expect(
        academicCertificate.connect(admin).verifyInstitution(institution.address)
      )
        .to.emit(academicCertificate, "InstitutionVerified")
        .withArgs(institution.address, true);

      const verifiedInstitution = await academicCertificate.institutions(institution.address);
      expect(verifiedInstitution.isVerified).to.equal(true);
    });

    it("Não deve permitir que não-admins verifiquem instituições", async function () {
      await academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana");
      
      await expect(
        academicCertificate.connect(otherAccount).verifyInstitution(institution.address)
      ).to.be.revertedWith("Apenas o administrador pode executar esta funcao.");
    });

    it("Não deve permitir verificar uma instituição não registrada", async function () {
      await expect(
        academicCertificate.connect(admin).verifyInstitution(otherAccount.address)
      ).to.be.revertedWith("Instituicao nao registrada.");
    });
  });

  describe("Register Certificate", function () {
    const certificateHash = ethers.utils.formatBytes32String("CERT123456"); // Usar ethers.utils.formatBytes32String

    beforeEach(async function () {
      // Registrar e verificar a instituição
      await academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana");
      await academicCertificate.connect(admin).verifyInstitution(institution.address);
    });

    it("Deve permitir que uma instituição verificada registre um certificado", async function () {
      const issueDate = Math.floor(Date.now() / 1000);

      await expect(
        academicCertificate.connect(institution).registerCertificate(certificateHash, "João Silva", issueDate)
      )
        .to.emit(academicCertificate, "CertificateRegistered")
        .withArgs(certificateHash, institution.address);

      const certificate = await academicCertificate.certificates(certificateHash);
      expect(certificate.studentName).to.equal("João Silva");
      expect(certificate.issueDate).to.equal(issueDate);
      expect(certificate.institutionAddress).to.equal(institution.address);
    });

    it("Não deve permitir que uma instituição não verificada registre um certificado", async function () {
      // Registrar uma nova instituição sem verificar
      await academicCertificate.connect(otherAccount).registerInstitution("Instituição DEF", "11.222.333/0001-44", "Prof. Maria");

      const newCertificateHash = ethers.utils.formatBytes32String("CERT654321"); // Usar ethers.utils.formatBytes32String
      await expect(
        academicCertificate.connect(otherAccount).registerCertificate(newCertificateHash, "Pedro Souza", Math.floor(Date.now() / 1000))
      ).to.be.revertedWith("Instituicao nao verificada.");
    });

    it("Não deve permitir registrar um certificado com hash já existente", async function () {
      const issueDate = Math.floor(Date.now() / 1000);
      await academicCertificate.connect(institution).registerCertificate(certificateHash, "João Silva", issueDate);
      
      await expect(
        academicCertificate.connect(institution).registerCertificate(certificateHash, "Maria Oliveira", issueDate)
      ).to.be.revertedWith("Certificado ja registrado.");
    });
  });

  describe("Get Certificate", function () {
    const certificateHash = ethers.utils.formatBytes32String("CERT123456"); // Usar ethers.utils.formatBytes32String
    const issueDate = Math.floor(Date.now() / 1000);

    beforeEach(async function () {
      // Registrar e verificar a instituição
      await academicCertificate.connect(institution).registerInstitution("Instituição ABC", "98.765.432/0001-10", "Prof. Ana");
      await academicCertificate.connect(admin).verifyInstitution(institution.address);

      // Registrar um certificado
      await academicCertificate.connect(institution).registerCertificate(certificateHash, "João Silva", issueDate);
    });

    it("Deve retornar os detalhes de um certificado existente", async function () {
      const certificate = await academicCertificate.getCertificate(certificateHash);
      expect(certificate.studentName).to.equal("João Silva");
      expect(certificate.issueDate).to.equal(issueDate);
      expect(certificate.institutionAddress).to.equal(institution.address);
    });

    it("Não deve retornar detalhes para um certificado inexistente", async function () {
      const nonExistentHash = ethers.utils.formatBytes32String("CERT999999"); // Usar ethers.utils.formatBytes32String
      await expect(
        academicCertificate.getCertificate(nonExistentHash)
      ).to.be.revertedWith("Certificado nao encontrado.");
    });
  });

  describe("Transfer Admin", function () {
    it("Deve permitir que o admin transfira sua função para outro endereço", async function () {
      await expect(
        academicCertificate.connect(admin).transferAdmin(otherAccount.address)
      )
        .to.emit(academicCertificate, "AdminTransferred")
        .withArgs(admin.address, otherAccount.address);

      expect(await academicCertificate.admin()).to.equal(otherAccount.address);
    });

    it("Não deve permitir que não-admins transfiram a função de admin", async function () {
      await expect(
        academicCertificate.connect(otherAccount).transferAdmin(institution.address)
      ).to.be.revertedWith("Apenas o administrador pode executar esta funcao.");
    });

    it("Não deve permitir transferir admin para o endereço zero", async function () {
      await expect(
        academicCertificate.connect(admin).transferAdmin(ethers.constants.AddressZero)
      ).to.be.revertedWith("Endereco invalido para o novo admin.");
    });
  });
});