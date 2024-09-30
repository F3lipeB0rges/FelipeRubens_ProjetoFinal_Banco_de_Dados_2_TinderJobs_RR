from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

class DevForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades (separe por vírgula)', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit= SubmitField('Cadastrar')

class EmpresaForm(FlaskForm):
    name = StringField('Nome da Empresa', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades desejadas (separe por vírgula)', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

# lógica para página inicial
@app.route("/")
def home():
    return render_template("index.html")

# lógica para login de devs
@app.route("/dev/login", methods=["GET", "POST"])
def dev_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with open("devs-data.csv", mode="r", encoding="utf-8") as csv_file:
            for line in csv_file:
                if line.strip():
                    values = line.strip().split(", ")
                    if len(values) == 5:
                        name, email_csv, cel, habilidades, password_csv = line.strip().split(", ")
                        if email == email_csv and password == password_csv:
                            session['email'] = email_csv
                            return redirect(url_for('show_empresas'))

        flash("E-mail ou senha inválidos.", "danger")
        return render_template("dev_login.html")

    return render_template("dev_login.html")

# lógica para página para match de devs com empresas
@app.route("/dev/empresas/<int:current_index>")
@app.route("/dev/empresas")
def show_empresas():
    return render_template("show_empresas.html")

    with open("empresas-data.csv", mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            name, email, cel, habilidades, password = line.strip().split(", ")
            empresas.append({"name": name, "description": habilidades})
    
    if current_index < 0 or current_index >= len(empresas):
        return redirect(url_for('show_empresas', current_index=0))  # Redireciona se o índice for inválido

    return render_template("show_empresas.html", empresas=empresas, current_index=current_index)

@app.route("/dev/empresas/data")
def empresas_data():
    empresas = []
    try:
        with open("empresas-data.csv", mode="r", encoding="utf-8") as csv_file:
            for line in csv_file:
                if line.strip():  # Verifica se a linha não está vazia
                    name, email, cel, habilidades, password = line.strip().split(", ")
                    empresas.append({"name": name, "description": habilidades})

        print("Empresas carregadas:", empresas)  # Log para ver as empresas carregadas
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")  # Para depuração
        return jsonify({"error": str(e)}), 500  # Retorna um erro JSON para o cliente

    return jsonify(empresas)  # Retorna os dados em formato JSON

@app.route("/dev/habilidades")
def dev_habilidades():
    # Aqui você deve obter as habilidades do desenvolvedor logado
    email_logado = session.get('email')  # Supondo que você armazena o e-mail do dev na sessão
    habilidades_dev = []

    with open("devs-data.csv", mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            if line.strip():
                name, email_csv, cel, habilidades, password_csv = line.strip().split(", ")
                if email_csv == email_logado:
                    habilidades_dev = habilidades.split(", ")
                    break  # Encerra o loop assim que encontrar o desenvolvedor logado

    return jsonify({"habilidades": ", ".join(habilidades_dev)})  # Retorna as habilidades como JSON

# lógica para registro de devs
@app.route("/dev/register", methods=["GET", "POST"])
def dev_register():
    form = DevForm()
    if form.validate_on_submit():
        with open("devs-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"{form.name.data}, {form.email.data}, {form.cel.data}, {form.habilidades.data}, {form.password.data}\n")
        return redirect(url_for('home'))
    return render_template("dev_register.html", form=form)

# lógica para login de empresa
@app.route("/empresa/login", methods=["GET", "POST"])
def empresa_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with open("empresas-data.csv", mode="r", encoding="utf-8") as csv_file:
            for line in csv_file:
                if line.strip():
                    values = line.strip().split(", ")
                    if len(values) == 5:
                        name, email_csv, cel, habilidades, password_csv = values
                        if email == email_csv and password == password_csv:
                            session['email'] = email_csv
                            return redirect(url_for('show_devs'))

        flash("E-mail ou senha inválidos.", "danger")
        return render_template("empresa_login.html")

    return render_template("empresa_login.html")

# lógica para página para match de empresas com devs
@app.route("/empresa/devs/<int:current_index>")
@app.route("/empresa/devs")
def show_devs():
    devs = []  # Inicializa a lista de desenvolvedores

    # Lê os dados dos desenvolvedores do CSV
    with open("devs-data.csv", mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            if line.strip():  # Verifica se a linha não está vazia
                name, email, cel, habilidades, password = line.strip().split(", ")
                devs.append({"name": name, "skills": habilidades.split(", ")})  # Adiciona as habilidades em uma lista

    if len(devs) == 0:  # Se não houver desenvolvedores, redirecione ou mostre uma mensagem
        flash("Nenhum desenvolvedor encontrado.", "warning")
        return redirect(url_for('home'))  # Ou redirecione para outra página

    current_index = 0  # Define o índice atual

    if current_index < 0 or current_index >= len(devs):
        return redirect(url_for('show_devs', current_index=0))  # Redireciona se o índice for inválido

    return render_template("show_devs.html", devs=devs, current_index=current_index)

    
@app.route("/empresa/devs/data")
def devs_data():
    devs = []
    try:
        with open("devs-data.csv", mode="r", encoding="utf-8") as csv_file:
            for line in csv_file:
                if line.strip():  # Verifica se a linha não está vazia
                    values = line.strip().split(", ")
                    if len(values) == 5:  # Verifica se a linha tem o número correto de campos
                        name, email, cel, habilidades, password = values
                        devs.append({"name": name, "skills": habilidades.split(', ')})  # As habilidades agora são uma lista
                    else:
                        print(f"Linha inválida ignorada: {line.strip()}")  # Log para depuração

        print("Desenvolvedores carregados:", devs)  # Log para ver os desenvolvedores carregados
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return jsonify({"error": str(e)}), 500  # Retorna um erro JSON para o cliente

    return jsonify(devs)  # Retorna os dados dos devs em formato JSON

@app.route("/empresa/habilidades")
def emp_habilidades():
    email_logado = session.get('email')
    habilidades_emp = []

    with open("empresas-data.csv", mode="r", encoding="utf-8") as csv_file:
        for line in csv_file:
            name, email_csv, cel, habilidades, password_csv = line.strip().split(", ")
            if email_csv == email_logado:
                habilidades_emp = habilidades.split(",")
                break
    
    return jsonify({"habilidades": ", ".join(habilidades_emp)})

# lógica para registro de empresa
@app.route("/empresa/register", methods=["GET", "POST"])
def empresa_register():
    form = EmpresaForm()
    if form.validate_on_submit():
        with open("empresas-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"{form.name.data}, {form.email.data}, {form.cel.data}, {form.habilidades.data}, {form.password.data}\n")
        return redirect(url_for('home'))
    return render_template("empresa_register.html", form=form)

if __name__ == '__main__':
    app.run(debug=True, port=6001)
