# app.py — CADASTRO DE PRODUTOS COM FLASK + MYSQL/MARIADB
# Ideia central: um formulário na página envia dados ao Python,
# e o Python grava esses dados direto na tabela produtos do banco.
#
# Caminho da informação:
# navegador (formulário) -> Flask (app.py) -> PyMySQL -> banco escola_teste

# 1. IMPORTAÇÕES
# Flask: cria o servidor web.
# render_template: abre um arquivo HTML da pasta templates.
# request: dá acesso ao que foi enviado pelo formulário.
# redirect e url_for: mandam o navegador de volta para a página inicial.
# pymysql: biblioteca que conversa com o MySQL e com o MariaDB.
from flask import Flask, render_template, request, redirect, url_for
import pymysql

# 2. CONFIGURAÇÃO DA CONEXÃO
# Ajuste estes valores de acordo com o banco instalado na sua máquina.
# A porta padrão do MySQL e do MariaDB é 3306.
# Se você usa XAMPP, normalmente o usuário é "root" e a senha é vazia "".
CONFIG_BANCO = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "sesidb",
    "database": "escola_teste",
    "charset": "utf8mb4",
}

# 3. CRIAÇÃO DA APLICAÇÃO
# __name__ informa ao Flask onde está este arquivo,
# para ele encontrar as pastas templates e static.
app = Flask(__name__)


# 4. FUNÇÃO QUE ABRE A CONEXÃO COM O BANCO
# Cada vez que precisarmos do banco, chamamos esta função.
# O ** "desempacota" o dicionário: é o mesmo que escrever
# pymysql.connect(host="localhost", port=3306, user="root", ...)
def conectar():
    return pymysql.connect(**CONFIG_BANCO)


# 5. ROTA DA PÁGINA INICIAL — LISTA OS PRODUTOS
# @app.route("/") diz: quando acessarem o endereço "/", execute esta função.
@app.route("/")
def index():
    conexao = conectar()
    # O cursor é quem envia os comandos SQL e recebe as respostas.
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, preco, quantidade FROM produtos ORDER BY id")
    # fetchall devolve todas as linhas encontradas, como uma lista de tuplas.
    # Exemplo: [(1, "Caneta", Decimal("2.50"), 100), (2, "Caderno", ...)]
    produtos = cursor.fetchall()
    # Sempre fechamos o que abrimos.
    cursor.close()
    conexao.close()

    # Envia a lista de produtos para o HTML exibir na tabela.
    return render_template("index.html", produtos=produtos)


# 6. ROTA QUE RECEBE O FORMULÁRIO E GRAVA NO BANCO
# methods=["POST"]: esta rota só aceita envio de formulário.
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    # request.form guarda os campos do formulário pelo atributo name do HTML.
    # Tudo chega como texto (str), por isso convertemos.
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    quantidade = int(request.form["quantidade"])

    conexao = conectar()
    cursor = conexao.cursor()

    # Os %s são "espaços reservados". O PyMySQL coloca os valores no lugar
    # deles com segurança. NUNCA monte o SQL juntando textos com +,
    # pois isso abre espaço para um ataque chamado SQL Injection.
    # O id não aparece aqui: o AUTO_INCREMENT do banco gera sozinho.
    sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nome, preco, quantidade))

    # commit confirma a alteração. Sem ele, o INSERT NÃO fica salvo no banco.
    conexao.commit()

    cursor.close()
    conexao.close()

    # Volta para a página inicial, que já mostrará o novo produto na tabela.
    return redirect(url_for("index"))


# 7. INICIA O SERVIDOR
# Este if garante que o servidor só sobe quando rodamos: python app.py
# debug=True reinicia o servidor ao salvar o arquivo e mostra erros detalhados.
# Use debug=True apenas em sala de aula / desenvolvimento.
if __name__ == "__main__":
    app.run(debug=True)

# PARA O CADERNO
# Conectar -> criar cursor -> executar SQL -> (commit, se alterou) -> fechar.
# SELECT apenas lê; INSERT, UPDATE e DELETE alteram e precisam de commit.
# Os %s protegem o banco: os valores nunca são colados direto no texto do SQL.
