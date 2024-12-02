// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Academic Certificate Management on Blockchain
/// @author Arthur Azevedo
/// @notice Este contrato permite o registro, verificação e emissão de certificados acadêmicos por instituições educacionais de forma descentralizada e segura na blockchain.
/// @dev Utiliza as versões Solidity ^0.8.0. É recomendado auditar o contrato antes do uso em produção.

contract AcademicCertificate {
    /// @notice Endereço do administrador do contrato
    address public admin;

    /// @notice Evento emitido quando uma instituição é registrada
    /// @param institutionAddress Endereço da instituição registrada
    /// @param name Nome da instituição registrada
    event InstitutionRegistered(address indexed institutionAddress, string name);

    /// @notice Evento emitido quando uma instituição é verificada pelo administrador
    /// @param institutionAddress Endereço da instituição verificada
    /// @param isVerified Status de verificação da instituição
    event InstitutionVerified(address indexed institutionAddress, bool isVerified);

    /// @notice Evento emitido quando um certificado é registrado
    /// @param certificateHash Hash único do certificado
    /// @param institutionAddress Endereço da instituição que emitiu o certificado
    event CertificateRegistered(bytes32 indexed certificateHash, address indexed institutionAddress);

    /// @notice Evento emitido quando a administração do contrato é transferida para outro endereço
    /// @param previousAdmin Endereço do administrador anterior
    /// @param newAdmin Endereço do novo administrador
    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

    /// @notice Estrutura que representa uma instituição educacional
    /// @param name Nome da instituição
    /// @param cnpj CNPJ da instituição
    /// @param responsible Responsável pela instituição
    /// @param isVerified Status de verificação da instituição
    struct Institution {
        string name;
        string cnpj;
        string responsible;
        bool isVerified;
    }

    /// @notice Estrutura que representa um certificado acadêmico
    /// @param certificateHash Hash único do certificado
    /// @param studentName Nome do aluno
    /// @param issueDate Data de emissão do certificado (timestamp)
    /// @param institutionAddress Endereço da instituição que emitiu o certificado
    struct Certificate {
        bytes32 certificateHash;
        string studentName;
        uint256 issueDate;
        address institutionAddress;
    }

    /// @notice Mapeamento que relaciona endereços de instituições com suas informações
    mapping(address => Institution) public institutions;

    /// @notice Mapeamento que relaciona hashes de certificados com suas informações
    mapping(bytes32 => Certificate) public certificates;

    /// @notice Modificador que restringe o acesso a apenas o administrador do contrato
    modifier onlyAdmin() {
        require(msg.sender == admin, "Apenas o administrador pode executar esta funcao.");
        _;
    }

    /// @notice Modificador que restringe o acesso a apenas instituições verificadas
    modifier onlyVerifiedInstitution() {
        require(institutions[msg.sender].isVerified, "Instituicao nao verificada.");
        _;
    }

    /// @notice Construtor do contrato que define o administrador inicial
    constructor() {
        admin = msg.sender;
    }

    /// @notice Registra uma nova instituição no contrato
    /// @dev Apenas qualquer pessoa pode registrar uma instituição, mas ela precisa ser verificada pelo admin posteriormente
    /// @param _name Nome da instituição
    /// @param _cnpj CNPJ da instituição
    /// @param _responsible Responsável pela instituição
    function registerInstitution(
        string memory _name,
        string memory _cnpj,
        string memory _responsible
    ) public {
        require(bytes(_name).length > 0, "Nome da instituicao e obrigatorio.");
        require(bytes(_cnpj).length > 0, "CNPJ e obrigatorio.");
        require(bytes(_responsible).length > 0, "Responsavel e obrigatorio.");
        require(!isInstitutionRegistered(msg.sender), "Instituicao ja registrada.");

        institutions[msg.sender] = Institution(_name, _cnpj, _responsible, false);
        emit InstitutionRegistered(msg.sender, _name);
    }

    /// @notice Verifica uma instituição previamente registrada
    /// @dev Apenas o administrador pode chamar esta função
    /// @param _institutionAddress Endereço da instituição a ser verificada
    function verifyInstitution(address _institutionAddress) public onlyAdmin {
        require(isInstitutionRegistered(_institutionAddress), "Instituicao nao registrada.");
        institutions[_institutionAddress].isVerified = true;
        emit InstitutionVerified(_institutionAddress, true);
    }

    /// @notice Registra um novo certificado acadêmico emitido por uma instituição verificada
    /// @dev Apenas instituições verificadas podem chamar esta função
    /// @param _certificateHash Hash único do certificado
    /// @param _studentName Nome do aluno
    /// @param _issueDate Data de emissão do certificado (timestamp)
    function registerCertificate(
        bytes32 _certificateHash,
        string memory _studentName,
        uint256 _issueDate
    ) public onlyVerifiedInstitution {
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
    /// @return institutionAddress Endereço da instituição que emitiu o certificado
    function getCertificate(bytes32 _certificateHash) public view returns (
        string memory studentName,
        uint256 issueDate,
        address institutionAddress
    ) {
        require(certificates[_certificateHash].certificateHash != bytes32(0), "Certificado nao encontrado.");
        Certificate memory cert = certificates[_certificateHash];
        return (cert.studentName, cert.issueDate, cert.institutionAddress);
    }

    /// @notice Transfere o papel de administrador para outro endereço
    /// @dev Apenas o administrador atual pode chamar esta função
    /// @param newAdmin Endereço para o qual a administração será transferida
    function transferAdmin(address newAdmin) public onlyAdmin {
        require(newAdmin != address(0), "Endereco invalido para o novo admin.");
        emit AdminTransferred(admin, newAdmin);
        admin = newAdmin;
    }

    /// @notice Verifica se uma instituição já está registrada
    /// @param _institutionAddress Endereço da instituição a ser verificada
    /// @return bool Indica se a instituição está registrada
    function isInstitutionRegistered(address _institutionAddress) public view returns (bool) {
        return bytes(institutions[_institutionAddress].name).length > 0;
    }
}