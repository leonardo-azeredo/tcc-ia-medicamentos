from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_med'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Função para remover pontos e traços do CPF
def limpar_cpf(cpf):
    return re.sub(r'[^\d]', '', cpf)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastrar_paciente', methods=['GET', 'POST'])
def cadastrar_paciente():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = limpar_cpf(request.form['cpf'])  # Remover pontos e traços do CPF
        sexo = request.form['sexo']
        idade = request.form['idade']
        enfermidade_id = request.form['enfermidade']
        
        # Verificar se o CPF já existe no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM pacientes WHERE cpf = %s", [cpf])
        paciente_existente = cur.fetchone()
        cur.close()
        
        if paciente_existente:
            return "Já existe um paciente com este CPF. Por favor, verifique o CPF e tente novamente."
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pacientes (nome, cpf, sexo, idade, enfermidade_id) VALUES (%s, %s, %s, %s, %s)",
                    (nome, cpf, sexo, idade, enfermidade_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listar_pacientes'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM enfermidades")
    enfermidades = cur.fetchall()
    return render_template('cadastrar_paciente.html', enfermidades=enfermidades)


@app.route('/cadastrar_medicamento', methods=['GET', 'POST'])
def cadastrar_medicamento():
    if request.method == 'POST':
        nome_medicamento = request.form['nome_medicamento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicamentos (nome) VALUES (%s)", [nome_medicamento])
        mysql.connection.commit()
        cur.close()
    return render_template('cadastrar_medicamento.html')

@app.route('/atribuir_medicamento/<int:paciente_id>', methods=['GET', 'POST'])
def atribuir_medicamento(paciente_id):
    if request.method == 'POST':
        medicamento_id = request.form['medicamento_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicamentos_pacientes (paciente_id, medicamento_id) VALUES (%s, %s)",
                    (paciente_id, medicamento_id))
        mysql.connection.commit()
        cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pacientes WHERE id = %s", [paciente_id])
    paciente = cur.fetchone()
    cur.execute("SELECT * FROM medicamentos")
    medicamentos = cur.fetchall()
    return render_template('atribuir_medicamento.html', paciente=paciente, medicamentos=medicamentos)


@app.route('/cadastrar_enfermidade', methods=['GET', 'POST'])
def cadastrar_enfermidade():
    if request.method == 'POST':
        nome_enfermidade = request.form['nome_enfermidade']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO enfermidades (nome) VALUES (%s)", [nome_enfermidade])
        mysql.connection.commit()
        cur.close()
    return render_template('cadastrar_enfermidade.html')

@app.route('/listar_enfermidades')
def listar_enfermidades():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM enfermidades")
    enfermidades = cur.fetchall()
    return render_template('listar_enfermidades.html', enfermidades=enfermidades)

@app.route('/listar_medicamentos')
def listar_medicamentos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medicamentos")
    medicamentos = cur.fetchall()
    return render_template('listar_medicamentos.html', medicamentos=medicamentos)


@app.route('/listar_pacientes')
def listar_pacientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT pacientes.id, pacientes.nome, pacientes.cpf, pacientes.sexo, pacientes.idade, pacientes.enfermidade, GROUP_CONCAT(medicamentos.nome SEPARATOR ', ') AS medicamentos FROM pacientes LEFT JOIN medicamentos_pacientes ON pacientes.id = medicamentos_pacientes.paciente_id LEFT JOIN medicamentos ON medicamentos_pacientes.medicamento_id = medicamentos.id GROUP BY pacientes.id")
    pacientes = cur.fetchall()
    return render_template('listar_pacientes.html', pacientes=pacientes)


@app.route('/excluir_paciente/<int:paciente_id>', methods=['GET'])
def excluir_paciente(paciente_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = %s", [paciente_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_pacientes'))

@app.route('/excluir_enfermidade/<int:enfermidade_id>', methods=['GET'])
def excluir_enfermidade(enfermidade_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM enfermidades WHERE id = %s", [enfermidade_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_enfermidades'))

@app.route('/excluir_medicamento/<int:medicamento_id>', methods=['GET'])
def excluir_medicamento(medicamento_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM medicamentos WHERE id = %s", [medicamento_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar_medicamentos'))

if __name__ == '__main__':
    app.run(debug=True)
