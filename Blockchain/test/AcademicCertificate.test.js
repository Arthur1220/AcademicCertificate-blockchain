const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AcademicCertificate Contract", function () {
  let AcademicCertificate;
  let academicCertificate;
  let admin;
  let addr1;
  let addr2;
  let addrs;

  beforeEach(async function () {
    // Obter o contrato factory e as contas
    AcademicCertificate = await ethers.getContractFactory("AcademicCertificate");
    [admin, addr1, addr2, ...addrs] = await ethers.getSigners();

    // Fazer o deploy do contrato
    academicCertificate = await AcademicCertificate.deploy();
    await academicCertificate.deployed();
  });

  describe("Deployment", function () {
    it("Deve definir o admin corretamente", async function () {
      expect(await academicCertificate.admin()).to.equal(admin.address);
    });
  });

  describe("Register Certificate", function () {
    it("Deve permitir que qualquer pessoa registre um certificado", async function () {
      const certificateHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("Certificado1")
      );
      const studentName = "Maria Silva";
      const issueDate = Math.floor(Date.now() / 1000);

      await expect(
        academicCertificate.connect(addr1).registerCertificate(
          certificateHash,
          studentName,
          issueDate
        )
      )
        .to.emit(academicCertificate, "CertificateRegistered")
        .withArgs(certificateHash, addr1.address);

      const cert = await academicCertificate.getCertificate(certificateHash);
      expect(cert.studentName).to.equal(studentName);
      expect(cert.issueDate).to.equal(issueDate);
      expect(cert.issuerAddress).to.equal(addr1.address);
    });

    it("Não deve permitir registrar um certificado com hash inválido (0x0)", async function () {
      const invalidHash = ethers.constants.HashZero;
      const studentName = "João Souza";
      const issueDate = Math.floor(Date.now() / 1000);

      await expect(
        academicCertificate.connect(addr2).registerCertificate(
          invalidHash,
          studentName,
          issueDate
        )
      ).to.be.revertedWith("Hash do certificado invalido.");
    });

    it("Não deve permitir registrar um certificado com nome vazio", async function () {
      const certificateHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("Certificado2")
      );
      const emptyName = "";
      const issueDate = Math.floor(Date.now() / 1000);

      await expect(
        academicCertificate.connect(addr1).registerCertificate(
          certificateHash,
          emptyName,
          issueDate
        )
      ).to.be.revertedWith("Nome do aluno e obrigatorio.");
    });

    it("Não deve permitir registrar um certificado com data de emissão inválida (0)", async function () {
      const certificateHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("Certificado3")
      );
      const studentName = "Ana Paula";
      const invalidIssueDate = 0;

      await expect(
        academicCertificate.connect(addr1).registerCertificate(
          certificateHash,
          studentName,
          invalidIssueDate
        )
      ).to.be.revertedWith("Data de emissao invalida.");
    });

    it("Não deve permitir registrar o mesmo certificado duas vezes", async function () {
      const certificateHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("Certificado4")
      );
      const studentName = "Pedro Henrique";
      const issueDate = Math.floor(Date.now() / 1000);

      // Registrar o certificado pela primeira vez
      await academicCertificate.connect(addr1).registerCertificate(
        certificateHash,
        studentName,
        issueDate
      );

      // Tentar registrar novamente com o mesmo hash
      await expect(
        academicCertificate.connect(addr2).registerCertificate(
          certificateHash,
          "Outra Pessoa",
          issueDate
        )
      ).to.be.revertedWith("Certificado ja registrado.");
    });
  });

  describe("Get Certificate", function () {
    it("Deve retornar os detalhes de um certificado existente", async function () {
      const certificateHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("Certificado5")
      );
      const studentName = "Lucas Oliveira";
      const issueDate = Math.floor(Date.now() / 1000);

      // Registrar o certificado
      await academicCertificate.connect(addr1).registerCertificate(
        certificateHash,
        studentName,
        issueDate
      );

      // Obter os detalhes do certificado
      const cert = await academicCertificate.getCertificate(certificateHash);
      expect(cert.studentName).to.equal(studentName);
      expect(cert.issueDate).to.equal(issueDate);
      expect(cert.issuerAddress).to.equal(addr1.address);
    });

    it("Não deve retornar detalhes para um certificado inexistente", async function () {
      const nonExistentHash = ethers.utils.keccak256(
        ethers.utils.toUtf8Bytes("CertificadoInexistente")
      );

      await expect(
        academicCertificate.getCertificate(nonExistentHash)
      ).to.be.revertedWith("Certificado nao encontrado.");
    });
  });

  describe("Transfer Admin", function () {
    it("Deve permitir que o admin transfira sua função para outro endereço", async function () {
      await expect(
        academicCertificate.connect(admin).transferAdmin(addr1.address)
      )
        .to.emit(academicCertificate, "AdminTransferred")
        .withArgs(admin.address, addr1.address);

      expect(await academicCertificate.admin()).to.equal(addr1.address);
    });

    it("Não deve permitir que não-admins transfiram a função de admin", async function () {
      await expect(
        academicCertificate.connect(addr1).transferAdmin(addr2.address)
      ).to.be.revertedWith("Apenas o administrador pode executar esta funcao.");
    });

    it("Não deve permitir transferir admin para o endereço zero", async function () {
      await expect(
        academicCertificate.connect(admin).transferAdmin(ethers.constants.AddressZero)
      ).to.be.revertedWith("Endereco invalido para o novo admin.");
    });
  });
});
