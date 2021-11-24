# importando framework flask e bibliotecas para usar servicoes web
from flask import Flask, render_template, request, redirect, url_for, flash, session

from functools import wraps
# importando biblioteca para conectar com mysql
from flaskext.mysql import MySQL

mysql = MySQL()
# iniciando variavel app
app = Flask(__name__)
app.secret_key = "flash message"

# configurando conexão com banco de dados
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'jetsoft'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
# python -m pip install --upgrade pip setuptools virtualenv- para atualizar o env
# rota para a página inicial
# config pro phpmyadmin em caso de o erro: "Field ''1'' doesn't have a default value no wampserver
# select @@GLOBAL.sql_mode
# set GLOBAL sql_mode='ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/index')
@login_required
def index():

    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM  cliente order by id DESC limit 10")
    quadro_cliente = cur.fetchall()
    cur.execute("SELECT  nome_posto,descricao,escala, qtd_colaborador,cliente.nome_fantasia FROM posto_trabalho inner join cliente on posto_trabalho.cliente_id=cliente.id order by posto_trabalho.id DESC limit 10 ")
    data = cur.fetchall()
    cur.execute(
        "select count(id) from cliente")
    numeroCliente = cur.fetchall()
    cur.execute(
        "select count(id) from posto_trabalho")
    numeroPostos = cur.fetchall()
    cur.execute(
        "select count(id) from colaboradores")
    numeroColaboradores = cur.fetchall()

    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()
    return render_template('/index.html', data=data, quadro_cliente=quadro_cliente, numeroColaboradores=numeroColaboradores, numeroPostos=numeroPostos, numeroCliente=numeroCliente, nome=nome, nivel=nivel)


@app.route('/controle_presenca', methods=['GET', 'POST'])
@login_required
def controle():

    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM controle_presenca order by posto_trabalho, tipo_cobertura ,registro")
    data = cur.fetchall()
    cur.execute(
        "SELECT nome_completo FROM colaboradores"
    )
    colaborador = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        colaborador = request.form["colaborador"]
        dia = request.form["dia"]
        pouf = request.form["pouf"]

        cur.execute(
            "UPDATE `controle_presenca` SET `%s` = %s WHERE `colaborador` = %s", (
                dia, pouf, colaborador)
        )
        con.commit()
        return redirect(url_for('controle'))
    else:
        return render_template('/controle_presenca.html', controle=data, colaborador=colaborador, nome=nome, nivel=nivel)

# rota para a página de destino (cadastro de colaboradores)


@app.route('/cadastro_colaboradores', methods=['GET', 'POST'])
# função para tratamento dos dados
@login_required
def cadastro():
    # código de conectividade com banco de dados
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT nome_posto FROM posto_trabalho"
    )
    posto_trabalho = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        matricula = request.form["matricula"]
        funcao = request.form["funcao"]
        admissao = request.form["admissao"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        tipo_cobertura = request.form["devweb"]
        posto_trabalho = request.form["posto_trabalho"]

        cur.execute(
            "SELECT id FROM posto_trabalho WHERE nome_posto = %s ", (posto_trabalho))
        posto_trabalho_id = cur.fetchall()

        cur.execute("INSERT INTO `colaboradores`(`nome_completo`,`cpf`,`matricula`,`funcao`,`data_admissao`,`email`,`telefone`,`tipo_cobertura`,`posto_trabalho_id` ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s)",
                    (nome, cpf, matricula, funcao, admissao,
                     email, telefone, tipo_cobertura, posto_trabalho_id)
                    )

        cur.execute(
            "SELECT id FROM colaboradores WHERE nome_completo = %s ", (nome))
        colaborador_id = cur.fetchall()

        cur.execute(
            "INSERT INTO `controle_presenca` (`colaborador`, `colaborador_id`,`posto_trabalho`, `posto_trabalho_id`,`funcao`, `tipo_cobertura`) VALUES (%s, %s, %s, %s, %s, %s)", (
                nome, colaborador_id, posto_trabalho, posto_trabalho_id, funcao, tipo_cobertura)
        )
        con.commit()
        return redirect(url_for('cadastro'))
    else:
        return render_template('/cadastro_colaboradores.html', posto_trabalho=posto_trabalho, nome=nome, nivel=nivel)


@app.route('/contrato', methods=['GET', 'POST'])
@login_required
def contrato():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT cliente.razao_social , posto_trabalho.nome_posto FROM cliente INNER JOIN posto_trabalho ON cliente.id = posto_trabalho.cliente_id"
    )
    cliente = cur.fetchall()

    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        clienteposto = request.form["clienteposto"]
        valor = request.form["valor"]
        data_admissao = request.form["data_admissao"]
        cliente = clienteposto.split(" | ")[0]
        posto_trabalho = clienteposto.split(" | ")[1]

        cur.execute(
            "SELECT id FROM cliente WHERE razao_social = %s ", (cliente))
        cliente_id = cur.fetchall()

        cur.execute(
            "SELECT id FROM posto_trabalho WHERE nome_posto = %s ", (posto_trabalho))
        posto_trabalho_id = cur.fetchall()

        cur.execute(
            "SELECT escala FROM posto_trabalho WHERE nome_posto = %s ", (posto_trabalho))
        escala = cur.fetchall()

        cur.execute("INSERT INTO `contrato`(`cliente_id`,`posto_trabalho_id`,`valor`,`escala`,`data_admissao`) Values(%s, %s, %s, %s, %s)",
                    (cliente_id, posto_trabalho_id, valor, escala, data_admissao))
        con.commit()
        return redirect(url_for('contrato'))
    else:
        return render_template('cadastro_contrato.html', cliente=cliente, nome=nome, nivel=nivel)


@app.route('/cadastro_posto_trabalho', methods=['GET', 'POST'])
@login_required
def posto_trabalho():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT razao_social FROM cliente"
    )
    cliente = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        nome_posto = request.form["nome_posto"]
        escala = request.form["escala"]
        cliente = request.form["cliente"]
        qtd_colaborador = request.form["qtd_colaborador"]
        descricao = request.form["descricao"]

        cur.execute("SELECT id FROM cliente WHERE razao_social = %s", (cliente))
        cliente_id = cur.fetchall()

        cur.execute("INSERT INTO `posto_trabalho`(`nome_posto`,`escala`,`cliente_id`,`qtd_colaborador`,`descricao`) Values(%s, %s, %s, %s, %s)",
                    (nome_posto, escala, cliente_id, qtd_colaborador, descricao))
        con.commit()
        return redirect(url_for('posto_trabalho'))
    else:
        return render_template('/cadastro_posto_trabalho.html', cliente=cliente, nome=nome, nivel=nivel)


@app.route('/cadastro_cliente', methods=['GET', 'POST'])
@login_required
def cadastro_cliente():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        razao_social = request.form["razao_social"]
        nome_fantasia = request.form["nome_fantasia"]
        cnpj = request.form["cnpj"]
        endereco = request.form["endereco"]
        numero = request.form["numero"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        estado_uf = request.form["estado_uf"]
        cep = request.form["cep"]
        contato = request.form["contato"]
        email = request.form["email"]
        data_admissao = request.form["data_admissao"]

        cur.execute("INSERT INTO `cliente`(`razao_social`,`nome_fantasia`,`cnpj`,`endereco`,`numero`,`bairro`,`cidade`,`estado_uf`,`cep`,`contato`,`email`,`data_admissao`) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (razao_social, nome_fantasia, cnpj, endereco, numero, bairro,  cidade, estado_uf, cep, contato, email, data_admissao))
        con.commit()
        return redirect(url_for('cadastro_cliente'))
    else:
        return render_template('/cadastro_cliente.html', nome=nome, nivel=nivel)


@app.route('/evento', methods=['GET', 'POST'])
@login_required
def evento():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM evento")
    data = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Eventos gravados com sucesso!")
        nome_evento = request.form["nome_evento"]
        data_evento = request.form["data_evento"]
        descricao = request.form["descricao"]
        cur.execute("INSERT INTO `evento`(nome_evento,data_evento,descricao) Values(%s,%s,%s)",
                    (nome_evento, data_evento, descricao))
        con.commit()

        return redirect(url_for('evento'))
    else:
        return render_template('/evento.html', controle=data, nome=nome, nivel=nivel)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(
            'SELECT * FROM usuarios WHERE username=%s AND password=%s', (username, password,))
        account = cur.fetchone()
        if account:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            msg = 'Login ou senha incorreta!'
    return render_template('login.html', msg=msg)


@app.route("/logout")
def logout():
    # session.pop('username',None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/quadro_cliente')
@login_required
def quadro_cliente():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM  cliente order by id")
    quadro_cliente = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    return render_template('/quadro_cliente.html', quadro_cliente=quadro_cliente, nome=nome, nivel=nivel)


@app.route('/index_tatico')
@login_required
def index_tatico():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()
    return render_template('/index_tatico.html', nome=nome, nivel=nivel)


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()

    if request.method == "POST":
        flash("Eventos gravados com sucesso!")
        nome = request.form["nome"]
        username = request.form["username"]
        password = request.form["password"]
        nivel = request.form["nivel"]
        cur.execute("INSERT INTO `usuarios`(nome,username,password,nivel) Values(%s,%s,%s,%s)",
                    (nome, username, password, nivel))
        con.commit()

        return redirect(url_for('cadastro_usuario'))
    else:
        return render_template('/cadastro_usuario.html', nome=nome, nivel=nivel)


@app.route('/quadro_colaborador', methods=['GET'])
@login_required
def quadro_colaborador():
    con = mysql.connect()
    cur = con.cursor()

    cur.execute("SELECT nome_completo,funcao,tipo_cobertura,posto_trabalho.nome_posto,posto_trabalho.escala FROM colaboradores inner join posto_trabalho on colaboradores.posto_trabalho_id=posto_trabalho.id")
    quadro_colaborador = cur.fetchall()

    cur.execute('SELECT nome FROM usuarios')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios')
    nivel = cur.fetchall()

    return render_template('/quadro_colaborador.html', quadro_colaborador=quadro_colaborador, nome=nome, nivel=nivel)


@app.route('/postos_trabalho', methods=['GET'])
@login_required
def postos_trabalho():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("SELECT  nome_posto,descricao,escala, qtd_colaborador,cliente.nome_fantasia FROM posto_trabalho inner join cliente on posto_trabalho.cliente_id=cliente.id ")
    data = cur.fetchall()
    cur.execute('SELECT nome FROM usuarios ')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios ')
    nivel = cur.fetchall()
    return render_template('/postos_trabalho.html', data=data, nome=nome, nivel=nivel)


@app.route('/quadro_contrato', methods=['GET'])
@login_required
def quadro_contrato():
    con = mysql.connect()
    cur = con.cursor()

    cur.execute("SELECT contrato.id,cliente.razao_social,cliente.cnpj,posto_trabalho.nome_posto,contrato.escala,contrato.valor,contrato.data_admissao FROM contrato inner join cliente on contrato.cliente_id=cliente.id inner join posto_trabalho on contrato.posto_trabalho_id=posto_trabalho.id")
    quadro_contrato = cur.fetchall()

    cur.execute('SELECT nome FROM usuarios')
    nome = cur.fetchall()
    cur.execute('SELECT nivel FROM usuarios')
    nivel = cur.fetchall()

    return render_template('/quadro_contrato.html', quadro_contrato=quadro_contrato, nome=nome, nivel=nivel)


if __name__ == "__main__":
    app.run(debug=True)
