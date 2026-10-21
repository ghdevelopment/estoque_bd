# Estoque de Produtos — Python + Flask + MySQL/MariaDB

Projeto simples para mostrar como o Python se conecta a um banco de dados
e como um formulário em uma página web consegue **gravar dados direto no banco**.

O que acontece quando você clica em **Cadastrar**:

```
Navegador (formulário)  →  Flask (app.py)  →  PyMySQL  →  Banco escola_teste
                                                            tabela produtos
```

Depois de gravar, a página recarrega e mostra a tabela atualizada com os produtos do banco.

---

## 1. O que tem em cada arquivo

```
projeto_estoque/
├── app.py              → o servidor Flask: recebe o formulário e fala com o banco
├── banco.sql           → script que cria o banco escola_teste e a tabela produtos
├── requirements.txt    → lista de bibliotecas Python que precisam ser instaladas
├── templates/
│   └── index.html      → a página com o formulário e a tabela de produtos
└── static/
    └── style.css       → o visual da página (bem simples)
```

| Arquivo | Para que serve |
|---|---|
| `banco.sql` | Cria o banco e a tabela. Roda **uma vez só**, no MySQL ou MariaDB. |
| `app.py` | É o "cérebro". Tem duas rotas: `/` (mostra os produtos) e `/cadastrar` (grava um produto novo). |
| `templates/index.html` | O que o aluno vê no navegador. O Flask procura os HTML **obrigatoriamente** na pasta `templates`. |
| `static/style.css` | Arquivos fixos (CSS, imagens). O Flask procura esses arquivos na pasta `static`. |
| `requirements.txt` | Permite instalar todas as bibliotecas com um único comando. |

### A tabela `produtos`

| Coluna | Tipo | Observação |
|---|---|---|
| `id` | INT | AUTO_INCREMENT, NOT NULL, UNIQUE (chave primária). O banco gera sozinho. |
| `nome` | VARCHAR(100) | Nome do produto. |
| `preco` | DECIMAL(10,2) | Até 10 dígitos, 2 depois da vírgula. Ex.: `12345678.90` |
| `quantidade` | INT | Quantidade em estoque. |

---

## 2. Bibliotecas usadas

- **Flask** — cria o servidor web, que recebe o formulário e devolve a página.
- **PyMySQL** — faz a conexão entre o Python e o banco.
  Funciona **tanto com MySQL quanto com MariaDB**, sem mudar nada no código,
  porque os dois usam o mesmo protocolo de comunicação.

---

## 3. Passo a passo para executar

### Passo 1 — Ter o banco funcionando

Você precisa de **um** destes instalados e ligados:

- **MySQL** (ou MySQL Workbench), ou
- **MariaDB**, ou
- **XAMPP** (já vem com MariaDB — basta clicar em *Start* no módulo **MySQL** do painel).

### Passo 2 — Criar o banco e a tabela

Abra o arquivo `banco.sql` no programa que você usa para o banco
(Workbench, HeidiSQL, phpMyAdmin...) e execute todo o conteúdo.

Pelo terminal também funciona:

```
mysql -u root -p < banco.sql
```

> No phpMyAdmin (XAMPP): aba **SQL** → cole o conteúdo do `banco.sql` → **Executar**.

### Passo 3 — Instalar as bibliotecas Python

Abra o terminal **dentro da pasta `projeto_estoque`** e rode:

```
pip install -r requirements.txt
```

(Se o `pip` não for reconhecido, tente `python -m pip install -r requirements.txt`.)

### Passo 4 — Conferir usuário e senha do banco

No início do `app.py` existe o bloco `CONFIG_BANCO`:

```python
CONFIG_BANCO = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "escola_teste",
    "charset": "utf8mb4",
}
```

Troque `user` e `password` pelos dados do banco da sua máquina.
No XAMPP, normalmente é `root` com senha vazia (`""`), então não precisa mudar nada.

### Passo 5 — Ligar o servidor Flask

Ainda no terminal, dentro da pasta `projeto_estoque`:

```
python app.py
```

Deve aparecer algo assim:

```
 * Running on http://127.0.0.1:5000
```

### Passo 6 — Usar o sistema

1. Abra o navegador em **http://127.0.0.1:5000**
2. Preencha nome, preço e quantidade.
3. Clique em **Cadastrar**.
4. O produto aparece na tabela logo abaixo.

### Passo 7 — Provar que foi para o banco de verdade

Abra o Workbench / phpMyAdmin / HeidiSQL e execute:

```sql
SELECT * FROM escola_teste.produtos;
```

O produto cadastrado pela página estará lá. 🎯
Esse é o ponto principal da aula: **o Python alterou o banco de dados.**

Para parar o servidor: no terminal, aperte **Ctrl + C**.

---

## 4. Entendendo o `app.py` por partes

O arquivo está dividido em seções numeradas, iguais às do roteiro:

1. **Importações** — trazemos o Flask e o PyMySQL.
2. **Configuração da conexão** — endereço, usuário, senha e nome do banco.
3. **Criação da aplicação** — `app = Flask(__name__)`.
4. **Função `conectar()`** — abre a conexão com o banco.
5. **Rota `/`** — faz um `SELECT` e manda os produtos para o HTML.
6. **Rota `/cadastrar`** — lê o formulário e faz um `INSERT` no banco.
7. **Iniciar o servidor** — `app.run(debug=True)`.

### A "receita" para falar com o banco

Todo acesso ao banco segue a mesma sequência:

```python
conexao = conectar()                 # 1. abrir a conexão
cursor = conexao.cursor()            # 2. criar o cursor
cursor.execute("SQL aqui", valores)  # 3. executar o comando
conexao.commit()                     # 4. confirmar (só quando ALTERA o banco)
cursor.close()                       # 5. fechar o cursor
conexao.close()                      # 6. fechar a conexão
```

- `SELECT` só **lê** → não precisa de `commit`.
- `INSERT`, `UPDATE` e `DELETE` **alteram** → precisam de `commit`, senão nada é salvo.

### Por que usar `%s` no SQL?

```python
sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
cursor.execute(sql, (nome, preco, quantidade))
```

Os `%s` são lugares reservados. O PyMySQL coloca os valores ali de forma segura.
Nunca monte o SQL somando textos (`"... VALUES ('" + nome + "')"`),
porque isso permite um ataque chamado **SQL Injection**.

### Como o formulário chega no Python

No HTML, cada campo tem um `name`:

```html
<input type="text" name="nome">
```

No Python, pegamos o valor pelo mesmo nome:

```python
nome = request.form["nome"]
```

Tudo chega como **texto**, por isso usamos `float()` no preço e `int()` na quantidade
(lembra da aula de entrada e conversão? É a mesma ideia do `input()`).

---

## 5. Problemas comuns

| Mensagem de erro | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` (ou `pymysql`) | Bibliotecas não instaladas | Rode o Passo 3 |
| `Can't connect to MySQL server on 'localhost'` | Banco desligado | Ligue o MySQL/MariaDB (no XAMPP: *Start* em MySQL) |
| `Access denied for user 'root'@'localhost'` | Usuário ou senha errados | Ajuste `CONFIG_BANCO` no `app.py` |
| `Unknown database 'escola_teste'` | Banco não foi criado | Rode o `banco.sql` (Passo 2) |
| `Table 'escola_teste.produtos' doesn't exist` | Tabela não foi criada | Rode o `banco.sql` (Passo 2) |
| `TemplateNotFound: index.html` | HTML fora da pasta certa | O arquivo precisa estar em `templates/index.html` |
| Porta 3306 diferente | Banco instalado em outra porta | Mude `"port"` no `CONFIG_BANCO` |

---

## 6. Ideias para as próximas aulas

- Botão para **excluir** um produto (`DELETE`).
- Tela para **editar** preço e quantidade (`UPDATE`).
- Destacar produtos com **estoque baixo** (ex.: quantidade menor que 5).
- Mostrar o **valor total do estoque** (`SUM(preco * quantidade)`).
- Tratar erros de entrada com `try/except` (arquivo 16 do roteiro).
