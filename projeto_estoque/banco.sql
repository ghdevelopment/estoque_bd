-- banco.sql — CRIAÇÃO DO BANCO E DA TABELA
-- Execute este arquivo UMA vez no MySQL ou no MariaDB (Workbench, HeidiSQL,
-- phpMyAdmin ou terminal). Os comandos são iguais nos dois.

-- 1. Cria o banco, caso ainda não exista.
CREATE DATABASE IF NOT EXISTS escola_teste
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. Seleciona o banco para os próximos comandos.
USE escola_teste;

-- 3. Cria a tabela de produtos.
-- id: AUTO_INCREMENT (AI), NOT NULL (NN) e UNIQUE.
--     O próprio banco gera o número: 1, 2, 3...
-- nome: texto de até 100 caracteres.
-- preco: DECIMAL(10,2) -> até 10 dígitos, sendo 2 depois da vírgula.
-- quantidade: número inteiro de itens em estoque.
CREATE TABLE IF NOT EXISTS produtos (
    id         INT NOT NULL AUTO_INCREMENT UNIQUE,
    nome       VARCHAR(100) NOT NULL,
    preco      DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (id)
);

-- 4. Para conferir os dados depois de cadastrar pelo formulário:
-- SELECT * FROM produtos;
