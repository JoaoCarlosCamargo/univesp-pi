import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_file
from werkzeug.exceptions import abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlite3 import connect
from io import BytesIO
from init_db import criar_tabelas

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta'

login_manager = LoginManager()
login_manager.init_app(app)

class Usuario(UserMixin):
    def __init__(self, id, created, nome):
        self.id = id
        self.created = created
        self.nome = nome

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if usuario:
        return Usuario(usuario[0], usuario[1], usuario[2])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (nome, senha))
        usuario = cursor.fetchone()
        con.close()
        if usuario:
            login_user(Usuario(usuario[0], usuario[1], usuario[2]))
            return redirect(url_for('admin'))
        flash('Login inválido!')
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    contato = conn.execute('SELECT * FROM contato').fetchall()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    reports = conn.execute('SELECT * FROM reports').fetchall()
    conn.close()
    return render_template('admin.html', usuario=current_user.nome, posts=posts, contato=contato, usuarios=usuarios, reports=reports)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

imagens = ['img/fotos/imagem1.png', 'img/fotos/imagem2.png', 'img/fotos/imagem3.png']
indice_atual = 0

@app.route('/')
def index():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  contato = conn.execute('SELECT whatsapp, facebook, instagram, email, endereco FROM contato').fetchall()
  mensagem_bottom = conn.execute('SELECT texto FROM mensagem_bottom').fetchall()
  conn.close()
  global indice_atual
  imagem_atual = imagens[indice_atual]
  return render_template('index.html', posts=posts, contato=contato, mensagem_bottom=mensagem_bottom, imagem=imagem_atual)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/semeie')
def semeie():
  return render_template('semeie.html')

@app.route('/proxima')
def proxima():
    global indice_atual
    indice_atual = (indice_atual + 1) % len(imagens)
    return jsonify({'imagem': imagens[indice_atual]})

@app.route('/anterior')
def anterior():
    global indice_atual
    indice_atual = (indice_atual - 1) % len(imagens)
    return jsonify({'imagem': imagens[indice_atual]})

@app.route("/admin/excluir_post/<int:id>")
def excluir_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Postagem excluída!')
    return redirect(url_for("admin"))

# Route for creating a new post
@app.route('/admin/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        flash('Postagem criada com sucesso!')
        return redirect(url_for('admin'))
    return render_template('create_post.html')

# Route for editing a post
@app.route('/admin/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (id,))
    post = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        flash('Postagem alterada com sucesso!')
        return redirect(url_for('admin'))

    return render_template('edit_post.html', post=post)

@app.route("/admin/excluir_usuario/<int:id>")
def excluir_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Usuário excluído!')
    return redirect(url_for("admin"))

# Route for creating a new usuario
@app.route('/admin/create_usuario', methods=['GET', 'POST'])
@login_required
def create_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', (nome, senha))
        conn.commit()
        conn.close()
        flash('Usuário criado com sucesso!')
        return redirect(url_for('admin'))
    return render_template('create_usuario.html')

# Route for editing a usuario
@app.route('/admin/edit_usuario/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET nome = ?, senha = ? WHERE id = ?', (nome, senha, id))
        conn.commit()
        conn.close()
        flash('Usuário alterado com sucesso!')
        return redirect(url_for('admin'))

    return render_template('edit_usuario.html', usuario=usuario)

# Rota para upload de novo relatório
@app.route('/reports/new', methods=['GET', 'POST'])
@login_required
def create_report():
    if request.method == 'POST':
        description = request.form['description']
        if 'report_file' not in request.files:
            flash('Selecione um arquivo PDF para upload')
            return redirect(url_for('create_report'))

        report_file = request.files['report_file']
        if report_file.filename.endswith('.pdf'):
            report_data = report_file.read()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO reports (description, report_file) VALUES (?, ?)', (description, report_data))
            conn.commit()
            conn.close()
            flash('Relatório enviado com sucesso!')
            return redirect(url_for('admin'))
        else:
            flash('Apenas arquivos PDF são permitidos')
            return redirect(url_for('create_report'))

    return render_template('create_report.html')

@app.route('/reports/<int:id>/download')
def download_report(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE id = ?', (id,))
    report = cursor.fetchone()
    conn.commit()
    conn.close()

    if report is None:
        abort(404)

    # Retrieve the PDF data from the database
    pdf_data = report[2]

    # Specify the download name (optional but recommended)
    download_name = f"{report[1]}.pdf"

    response = send_file(BytesIO(pdf_data), as_attachment=True, mimetype='application/pdf', download_name=download_name)
    return response

@app.route("/admin/excluir_report/<int:id>")
def excluir_report(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Relatório excluído!')
    return redirect(url_for("admin"))

if __name__ == "__main__":
  criar_tabelas()
  app.run()
