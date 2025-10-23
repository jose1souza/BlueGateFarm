DELIMITER //
CREATE TRIGGER tr_insere_usuario 
AFTER INSERT ON usuario
FOR EACH ROW
BEGIN 
	INSERT INTO auditoria
(acao_realizada,
tabela,
data_time,
usuario)
VALUES
(CONCAT('INSERT INTO usuario (nome, email, senha_hash, ativo) VALUES (', 
        NEW.nome, ', ', NEW.email, ', ', NEW.senha_hash, ', ', NEW.ativo, ');'),
        
"Usuário",
NOW(),
USER());
END //
DELIMITER ;