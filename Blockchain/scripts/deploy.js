const hre = require("hardhat");

async function main() {
  // Compila o contrato
  await hre.run('compile');

  // Obtém a factory do contrato
  const AcademicCertificate = await hre.ethers.getContractFactory("AcademicCertificate");
  
  // Deploy do contrato
  const academicCertificate = await AcademicCertificate.deploy();
  
  await academicCertificate.deployed();

  console.log("AcademicCertificate deployed to:", academicCertificate.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });