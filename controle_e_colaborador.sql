SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS clientes;

CREATE TABLE `clientes` (
  `ID` SERIAL PRIMARY KEY,
  `razao_social` varchar(64) NOT NULL,
  `cnpj` varchar(14) NOT NULL,
  `endereco` varchar(64) NOT NULL,
  `numero` varchar(5) NOT NULL,
  `bairro` varchar(32) NOT NULL,
  `cidade` varchar(32) NOT NULL,
  `estado_uf` varchar(2) NOT NULL,
  `cep` varchar(8) NOT NULL,
  `telefone` varchar(11) NOT NULL,
  `email` varchar(64) NOT NULL,
  `descricao` text NOT NULL,
  `ativo` bit(1) NOT NULL,
  `criado_em` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS colaboradores;

CREATE TABLE `colaboradores` (
  `codigo` SERIAL PRIMARY KEY,
  `nome_completo` varchar(64) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `matricula` varchar(16) NOT NULL,
  `funcao` varchar(32) NOT NULL,
  `data_admissao` date NOT NULL,
  `email` varchar(32) NOT NULL,
  `telefone` varchar(11) NOT NULL,
  `tipo_cobertura` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS controle_presenca;

CREATE TABLE `controle_presenca` (
  `registro` SERIAL PRIMARY KEY ,
  `colaborador` varchar(32) NOT NULL,
  `funcao` varchar(32) NOT NULL,
  `tipo_cobertura` varchar(10) NOT NULL
  `'1'` varchar(1) NOT NULL,
  `'2'` varchar(1) NOT NULL,
  `'3'` varchar(1) NOT NULL,
  `'4'` varchar(1) NOT NULL,
  `'5'` varchar(1) NOT NULL,
  `'6'` varchar(1) NOT NULL,
  `'7'` varchar(1) NOT NULL,
  `'8'` varchar(1) NOT NULL,
  `'9'` varchar(1) NOT NULL,
  `'10'` varchar(1) NOT NULL,
  `'11'` varchar(1) NOT NULL,
  `'12'` varchar(1) NOT NULL,
  `'13'` varchar(1) NOT NULL,
  `'14'` varchar(1) NOT NULL,
  `'15'` varchar(1) NOT NULL,
  `'16'` varchar(1) NOT NULL,
  `'17'` varchar(1) NOT NULL,
  `'18'` varchar(1) NOT NULL,
  `'19'` varchar(1) NOT NULL,
  `'20'` varchar(1) NOT NULL,
  `'21'` varchar(1) NOT NULL,
  `'22'` varchar(1) NOT NULL,
  `'23'` varchar(1) NOT NULL,
  `'24'` varchar(1) NOT NULL,
  `'25'` varchar(1) NOT NULL,
  `'26'` varchar(1) NOT NULL,
  `'27'` varchar(1) NOT NULL,
  `'28'` varchar(1) NOT NULL,
  `'29'` varchar(1) NOT NULL,
  `'30'` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
