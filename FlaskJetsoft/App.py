# importando framework flask e bibliotecas para usar servicoes web
from flask import Flask, render_template, request, redirect, url_for, flash

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

# rota para a página inicial


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/controle_presenca', methods=['GET', 'POST'])
def controle():

    con = mysql.connect()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM controle_presenca order by posto_trabalho, tipo_cobertura ,registro")
    data = cur.fetchall()

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
        return render_template('/controle_presenca.html', controle=data)

# rota para a página de destino (cadastro de colaboradores)


@app.route('/cadastro_colaboradores', methods=['GET', 'POST'])
# função para tratamento dos dados
def cadastro():
    # código de conectividade com banco de dados
    con = mysql.connect()
    cur = con.cursor()
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
        cur.execute("INSERT INTO `colaboradores`(`nome_completo`,`cpf`,`matricula`,`funcao`,`data_admissao`,`email`,`telefone`,`tipo_cobertura`,`posto_trabalho` ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s)",
                    (nome, cpf, matricula, funcao, admissao,
                     email, telefone, tipo_cobertura, posto_trabalho)
                    )
        cur.execute(
            "INSERT INTO `controle_presenca` (`colaborador`,`posto_trabalho`,`funcao`, `tipo_cobertura`) VALUES (%s, %s, %s, %s)", (
                nome, posto_trabalho, funcao, tipo_cobertura)
        )
        con.commit()
        return redirect(url_for('cadastro'))
    else:
        return render_template('/cadastro_colaboradores.html')


@app.route('/contrato', methods=['GET', 'POST'])
def contrato():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        cliente = request.form["cliente"]
        cnpj = request.form["cnpj"]
        endereco = request.form["endereco"]
        bairro = request.form["bairro"]
        numero = request.form["numero"]
        cidade = request.form["cidade"]
        estado_uf = request.form["estado_uf"]
        cep = request.form["cep"]
        posto_trabalho = request.form["posto_trabalho"]
        contato = request.form["contato"]
        valor = request.form["valor"]
        escala = request.form["escala"]
        data_admissao = request.form["data_admissao"]

        cur.execute("INSERT INTO `contrato`(`cliente`,`cnpj`,`endereco`,`bairro`,`numero`,`cidade`,`estado_uf`,`cep`,`posto_trabalho`,`contato`,`valor`,`escala`,`data_admissao`) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (cliente, cnpj, endereco, bairro, numero, cidade, estado_uf, cep, posto_trabalho, contato, valor, escala, data_admissao))
        con.commit()
        return redirect(url_for('contrato'))
    else:
        return render_template('cadastro_contrato.html')

# config pro phpmyadmin em caso de o erro: "Field ''1'' doesn't have a default value no wampserver
# select @@GLOBAL.sql_mode
# set GLOBAL sql_mode='ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'


@app.route('/cadastro_posto_trabalho', methods=['GET', 'POST'])
def posto_trabalho():
    con = mysql.connect()
    cur = con.cursor()
    if request.method == "POST":
        flash("Dados gravados com sucesso!")
        nome_posto = request.form["nome_posto"]
        escala = request.form["escala"]
        cliente = request.form["cliente"]
        qtd_colaborador = request.form["qtd_colaborador"]
        descricao = request.form["descricao"]

        cur.execute("INSERT INTO `posto_trabalho`(`nome_posto`,`escala`,`cliente`,`qtd_colaborador`,`descricao`) Values(%s, %s, %s, %s, %s)",
                    (nome_posto, escala, cliente, qtd_colaborador, descricao))
        con.commit()
        return redirect(url_for('posto_trabalho'))
    else:
        return render_template('/cadastro_posto_trabalho.html')


@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    con = mysql.connect()
    cur = con.cursor()
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
        return render_template('/cadastro_cliente.html')


if __name__ == "__main__":
    app.run(debug=True)
