
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
    cur.execute("SELECT * FROM controle_presenca")
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
        cur.execute("INSERT INTO `colaboradores`(`nome_completo`,`cpf`,`matricula`,`funcao`,`data_admissao`,`email`,`telefone`,`tipo_cobertura`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nome, cpf, matricula, funcao, admissao,
                     email, telefone, tipo_cobertura)
                    )
        cur.execute(
            "INSERT INTO `controle_presenca` (`colaborador`,`funcao`,`tipo_cobertura`) VALUES (%s, %s, %s)", (
                nome, funcao, tipo_cobertura)
        )
        con.commit()
        return redirect(url_for('cadastro'))
    else:
        return render_template('/cadastro_colaboradores.html')


if __name__ == "__main__":
    app.run(debug=True)
