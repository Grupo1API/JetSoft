drop table if exists usuarios;

create table usuarios(
    id serial primary key,
    nome text not null,
    username text not null unique,
    senha varchaR(20) not null
);

drop table if exists contrato;

create table contrato(
    id serial primary key,
    cliente text not null,
    cnpj varchar(14),
    endereco text not null,
    numero varchar(5),
    bairro text NOT NULL,
    cidade text NOT NULL,
    estado_uf varchar(2) NOT NULL,
    cep varchar(8) NOT NULL,
    contato varchar(20) not null,
    valor int not null,
    posto_trabalho text,
    escala varchar(20),
    data_admissao date NOT NULL
);

drop table if exists cliente;

create table cliente(
    id serial primary key,
    razao_social text not null,
    nome_fantasia text,
    cnpj varchar(14),
    endereco text not null,
    numero varchar(5),
    bairro text NOT NULL,
    cidade text NOT NULL,
    estado_uf varchar(2) NOT NULL,
    cep varchar(8) NOT NULL,
    contato int not null,
    email varchar(64) NOT NULL,
    data_admissao date NOT NULL
);

drop table if exists posto_trabalho;

create table posto_trabalho(
    id serial primary key,
    nome_posto text not null,
    descricao text not null,
    escala varchar(30) not null,
    qtd_colaborador int,
    cliente text not null
);

DROP TABLE IF EXISTS colaboradores;

CREATE TABLE colaboradores (
  codigo SERIAL PRIMARY KEY,
  nome_completo varchar(64) NOT NULL,
  cpf varchar(11) NOT NULL,
  matricula varchar(16) NOT NULL,
  funcao varchar(32) NOT NULL,
  data_admissao date NOT NULL,
  email varchar(32) NOT NULL,
  telefone varchar(11) NOT NULL,
  tipo_cobertura varchar(10) NOT NULL,
  posto_trabalho text not null
); 

DROP TABLE IF EXISTS controle_presenca;

CREATE TABLE controle_presenca (
  registro SERIAL PRIMARY KEY ,
  colaborador varchar(32) NOT NULL,
  posto_trabalho text not null,
  funcao varchar(32) NOT NULL,
  tipo_cobertura varchar(10) NOT NULL,
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
);
