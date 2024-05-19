from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Conexão com banco de dados
dados_conexao = (
    "Driver={SQL Server};"
    "Server=W-VAIO\SQLEXPRESS;"
    "Database=gerador_pedido"
)

def conectar_sql_server():
    try:
        # Estabelecer a conexão com o SQL Server
        conexao = pyodbc.connect(dados_conexao)
        return conexao
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao SQL Server: {e}")
        return None

conexao = conectar_sql_server()
cursor = conexao.cursor()

# Rotas

@app.route("/")
def home():
    # cursor.close()
    # conexao.close()
    conexao
    return render_template("index.html")

@app.route("/empresa")
def empresa():
    cursor.execute("SELECT id, nome, cnpj, endereco, telefone FROM empresa1")
    empresas = cursor.fetchall()
    return render_template('empresa.html', empresas=empresas)

@app.route("/clientes")
def clientes():
    cursor.execute("SELECT id, nome, cpf, endereco, telefone FROM clientes1")
    clientes = cursor.fetchall()
    return render_template("clientes.html", clientes=clientes)

@app.route("/produtos")
def produtos():
    cursor.execute("SELECT id, descricao, estoque, valorUnitario FROM produtos")
    produtos = cursor.fetchall()
    return render_template("produtos.html", produtos=produtos)

@app.route('/cadastrar-empresa', methods=['POST'])
def cadastrar_empresa():
    if request.method == 'POST':
        nomeEmpresa = request.form['nomeEmpresa']
        cnpj = request.form['cnpj']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        if conexao:
            try:
                comando = "INSERT INTO empresa1 (nome, cnpj, endereco, telefone) VALUES (?, ?, ?, ?)"
                cursor.execute(comando, (nomeEmpresa, cnpj, endereco, telefone))
                cursor.commit()
                # cursor.close()
                return f"""Sucesso ao cadastrar empresa, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""

            except pyodbc.Error as e:
                print(f"Erro ao inserir dados no banco de dados: {e}")
                return f"""Erro ao cadastrar empresa, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""
        else:
            return "Erro ao conectar ao banco de dados."
        
@app.route('/cadastrar-cliente', methods=['POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        if conexao:
            try:
                comando = "INSERT INTO clientes1 (nome, cpf, endereco, telefone) VALUES (?, ?, ?, ?)"
                cursor.execute(comando, (nome, cpf, endereco, telefone))
                cursor.commit()
                # cursor.close()
                return f"""Sucesso ao cadastrar cliente, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""

            except pyodbc.Error as e:
                print(f"Erro ao inserir dados no banco de dados: {e}")
                return f"""Erro ao cadastrar cliente, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""
        else:
            return "Erro ao conectar ao banco de dados."

@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        estoque = request.form['estoque']
        valorUnitario = request.form['valorUnitario']

        if conexao:
            try:
                comando = "INSERT INTO produtos (descricao, estoque, valorUnitario) VALUES (?, ?, ?)"
                cursor.execute(comando, (descricao, estoque, valorUnitario))
                cursor.commit()
                return f"""Sucesso ao cadastrar produto, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""

            except pyodbc.Error as e:
                print(f"Erro ao inserir dados no banco de dados: {e}")
                return f"""Erro ao cadastrar produto, clique no botão para voltar para a home
                        <a href="/">
                            <button>Voltar</button>
                        </a>"""
        else:
            return "Erro ao conectar ao banco de dados."

if __name__ == "__main__":
    app.run(debug=True)