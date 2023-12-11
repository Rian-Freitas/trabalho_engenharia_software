-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-12-05 11:19:35.106

-- tables
-- Table: artista
CREATE TABLE artista (
    cod_artista integer NOT NULL CONSTRAINT artista_pk PRIMARY KEY,
    nome_artista varchar(400) NOT NULL,
    email_artista varchar(255) NOT NULL,
    senha_artista varchar(30) NOT NULL,
    cpf_artista varchar(15) NOT NULL,
    associacao_cod_associacao double precision NOT NULL,
    CONSTRAINT artista_associacao FOREIGN KEY (associacao_cod_associacao)
    REFERENCES associacao (cod_associacao)
);

-- Table: associacao
CREATE TABLE associacao (
    cod_associacao integer NOT NULL CONSTRAINT associacao_pk PRIMARY KEY,
    nome_associacao varchar(50) NOT NULL,
    email_associacao varchar(255) NOT NULL,
    senha_associacao varchar(30) NOT NULL,
    cnpj_associacao varchar(18) NOT NULL
);

-- Table: estabelecimento
CREATE TABLE estabelecimento (
    cod_estabelecimento integer NOT NULL CONSTRAINT estabelecimento_pk PRIMARY KEY,
    cnpj_estabelecimento varchar(18) NOT NULL,
    razao_social varchar(255) NOT NULL,
    tipo_estabelecimento varchar(30) NOT NULL,
    numero_ambientes integer,
    proprietario_cod_proprietario integer NOT NULL,
    CONSTRAINT estabelecimento_proprietario FOREIGN KEY (proprietario_cod_proprietario)
    REFERENCES proprietario (cod_proprietario)
);

-- Table: obra
CREATE TABLE obra (
    cod_obra integer NOT NULL CONSTRAINT obra_pk PRIMARY KEY,
    titulo_obra varchar(400) NOT NULL,
    composicao text NOT NULL,
    data_criacao date NOT NULL
);

-- Table: pagamento_rubrica
CREATE TABLE pagamento_rubrica (
    cod_pagamento integer NOT NULL,
    obra_cod_obra integer NOT NULL,
    associacao_cod_associacao double precision NOT NULL,
    estabelecimento_cod_estabelecimento integer NOT NULL,
    data_pagamento date NOT NULL,
    valor_arrecadado float NOT NULL,
    CONSTRAINT pagamento_rubrica_pk PRIMARY KEY (cod_pagamento,obra_cod_obra,associacao_cod_associacao,estabelecimento_cod_estabelecimento),
    CONSTRAINT pagamento_rubrica_obra FOREIGN KEY (obra_cod_obra)
    REFERENCES obra (cod_obra),
    CONSTRAINT pagamento_rubrica_associacao FOREIGN KEY (associacao_cod_associacao)
    REFERENCES associacao (cod_associacao),
    CONSTRAINT pagamento_rubrica_estabelecimento FOREIGN KEY (estabelecimento_cod_estabelecimento)
    REFERENCES estabelecimento (cod_estabelecimento)
);

-- Table: proprietario
CREATE TABLE proprietario (
    cod_proprietario integer NOT NULL CONSTRAINT proprietario_pk PRIMARY KEY,
    cpf_proprietario varchar(15) NOT NULL,
    nome_proprietario varchar(400) NOT NULL,
    email_proprietario varchar(255) NOT NULL,
    senha_proprietario varchar(30) NOT NULL
);

-- Table: relacao_artista_obra
CREATE TABLE relacao_artista_obra (
    obra_cod_obra integer NOT NULL,
    artista_cod_artista integer NOT NULL,
    tipo_artista varchar(40) NOT NULL,
    porcentagem_diretos float NOT NULL,
    CONSTRAINT relacao_artista_obra_pk PRIMARY KEY (obra_cod_obra,tipo_artista,artista_cod_artista),
    CONSTRAINT relacao_artista_obra_obra FOREIGN KEY (obra_cod_obra)
    REFERENCES obra (cod_obra),
    CONSTRAINT relacao_artista_obra_artista FOREIGN KEY (artista_cod_artista)
    REFERENCES artista (cod_artista)
);

-- End of file.

