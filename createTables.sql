CREATE DATABASE  IF NOT EXISTS agricultura;
USE agricultura;

CREATE TABLE auditoria (
id_auditoria  INT AUTO_INCREMENT PRIMARY KEY,
acao_realizada  VARCHAR(400) NOT NULL,
tabela VARCHAR(50) NOT NULL,
data_time DATETIME NOT NULL,
usuario VARCHAR(50) NOT NULL
);

CREATE TABLE usuario (
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE permissao (
    id_permissao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE usuario_permissao (
    id_usuario INT NOT NULL,
    id_permissao INT NOT NULL,
    PRIMARY KEY (id_usuario, id_permissao),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_permissao) REFERENCES permissao(id_permissao)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE funcionario (
  id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  cargo VARCHAR(50),
  salario_hora DECIMAL(10,2),
  contato VARCHAR(100),
  id_cultura_fk INT,
  FOREIGN KEY (id_cultura_fk) REFERENCES cultura(id_cultura)
);

CREATE TABLE atividade_funcionario (
  id_atividade INT AUTO_INCREMENT PRIMARY KEY,
  id_funcionario INT NOT NULL,
  data DATE NOT NULL,
  descricao VARCHAR(255),
  horas_trabalhadas DECIMAL(5,2),
  FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

CREATE TABLE maquinario (
  id_maquina INT AUTO_INCREMENT PRIMARY KEY,
  tipo VARCHAR(50),
  modelo VARCHAR(100),
  data_aquisicao DATE,
  valor_hora DECIMAL(10,2),
  consumo_medio DECIMAL(10,2),
  id_cultura_fk INT,
  FOREIGN KEY (id_cultura_fk) REFERENCES cultura(id_cultura)
);

CREATE TABLE uso_maquinario (
  id_uso INT AUTO_INCREMENT PRIMARY KEY,
  id_maquina INT NOT NULL,
  id_funcionario INT NOT NULL,
  data DATE NOT NULL,
  horas_utilizadas DECIMAL(5,2),
  combustivel_consumido DECIMAL(10,2),
  FOREIGN KEY (id_maquina) REFERENCES maquinario(id_maquina),
  FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

CREATE TABLE cultura (
  id_cultura INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  classificacao_mercado VARCHAR(50)
);

CREATE TABLE cultivo (
  id_cultivo INT AUTO_INCREMENT PRIMARY KEY,
  id_cultura_fk INT NOT NULL,
  data_plantio DATE,
  data_colheita DATE,
  producao DECIMAL(10,2),
  FOREIGN KEY (id_cultura_fk) REFERENCES cultura(id_cultura)
);

CREATE TABLE estoque (
  id_estoque INT AUTO_INCREMENT PRIMARY KEY,
  tipo_grao VARCHAR(100),
  quantidade_sacas INT,
  qualidade_saca VARCHAR(50),
  data_entrada DATE
);

CREATE TABLE fazenda (
  id_fazenda INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  localizacao VARCHAR(255),
  tamanho_ha DECIMAL(10,2)
);
