// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Academic Certificate Management on Blockchain
/// @notice Este contrato permite o registro, verificação e emissão de certificados acadêmicos de forma descentralizada e segura na blockchain.

contract AcademicCertificate {
    /// @notice Endereço do administrador do contrato
    address public admin;

    /// @notice Evento emitido quando um certificado é registrado
    /// @param certificateHash Hash único do certificado
    /// @param issuerAddress Endereço que emitiu o certificado
    event CertificateRegistered(bytes32 indexed certificateHash, address indexed issuerAddress);

    /// @notice Evento emitido quando a administração do contrato é transferida para outro endereço
    /// @param previousAdmin Endereço do administrador anterior
    /// @param newAdmin Endereço do novo administrador
    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

    /// @notice Estrutura que representa um certificado acadêmico
    /// @param certificateHash Hash único do certificado
    /// @param studentName Nome do aluno
    /// @param issueDate Data de emissão do certificado (timestamp)
    /// @param issuerAddress Endereço que emitiu o certificado
    struct Certificate {
        bytes32 certificateHash;
        string studentName;
        uint256 issueDate;
        address issuerAddress;
    }

    /// @notice Mapeamento que relaciona hashes de certificados com suas informações
    mapping(bytes32 => Certificate) public certificates;

    /// @notice Modificador que restringe o acesso a apenas o administrador do contrato
    modifier onlyAdmin() {
        require(msg.sender == admin, "Apenas o administrador pode executar esta funcao.");
        _;
    }

    /// @notice Construtor do contrato que define o administrador inicial
    constructor() {
        admin = msg.sender;
    }

    /// @notice Registra um novo certificado acadêmico
    /// @dev Qualquer pessoa pode chamar esta função
    /// @param _certificateHash Hash único do certificado
    /// @param _studentName Nome do aluno
    /// @param _issueDate Data de emissão do certificado (timestamp)
    function registerCertificate(
        bytes32 _certificateHash,
        string memory _studentName,
        uint256 _issueDate
    ) public {
        require(_certificateHash != bytes32(0), "Hash do certificado invalido.");
        require(bytes(_studentName).length > 0, "Nome do aluno e obrigatorio.");
        require(_issueDate > 0, "Data de emissao invalida.");
        require(certificates[_certificateHash].certificateHash == bytes32(0), "Certificado ja registrado.");

        certificates[_certificateHash] = Certificate(
            _certificateHash,
            _studentName,
            _issueDate,
            msg.sender
        );
        emit CertificateRegistered(_certificateHash, msg.sender);
    }

    /// @notice Retorna os detalhes de um certificado existente
    /// @dev A função reverte se o certificado não for encontrado
    /// @param _certificateHash Hash único do certificado a ser consultado
    /// @return studentName Nome do aluno
    /// @return issueDate Data de emissão do certificado (timestamp)
    /// @return issuerAddress Endereço que emitiu o certificado
    function getCertificate(bytes32 _certificateHash) public view returns (
        string memory studentName,
        uint256 issueDate,
        address issuerAddress
    ) {
        require(certificates[_certificateHash].certificateHash != bytes32(0), "Certificado nao encontrado.");
        Certificate memory cert = certificates[_certificateHash];
        return (cert.studentName, cert.issueDate, cert.issuerAddress);
    }

    /// @notice Transfere o papel de administrador para outro endereço
    /// @dev Apenas o administrador atual pode chamar esta função
    /// @param newAdmin Endereço para o qual a administração será transferida
    function transferAdmin(address newAdmin) public onlyAdmin {
        require(newAdmin != address(0), "Endereco invalido para o novo admin.");
        emit AdminTransferred(admin, newAdmin);
        admin = newAdmin;
    }
}