INSERT INTO usuario (nome, email, senha_hash, ativo) VALUES
('Jose Carlos Souza', 'jose.souza@gmail.com', 'hash_senha_jose', TRUE),
('Lucas Antônio', 'lucas@gmail.com', 'hash_senha_lucas', FALSE),
('Brian Martins', 'brian.martins@gmail.com', 'hash_senha_brian', TRUE),
('Nicolas', 'nicolas@gmail.com', 'hash_senha_nicolas', FALSE);

INSERT INTO permissao (nome) VALUES
('ADMIN'),
('FUNCIONARIO'),
('GERENTE'),
('VISUALIZADOR');

INSERT INTO usuario_permissao (id_usuario, id_permissao) VALUES
(1, 1);

INSERT INTO usuario_permissao (id_usuario, id_permissao) VALUES
(2, 2);

INSERT INTO usuario_permissao (id_usuario, id_permissao) VALUES
(3, 3);

SELECT * FROM usuario;
select * from auditoria;
select * from fazenda;

INSERT INTO fazenda(nome,localizacao,tamanho_ha) VALUES 
("Fazenda Azul","Machado-MG",200);