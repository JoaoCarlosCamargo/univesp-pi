import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.exceptions import abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlite3 import connect
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
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if usuario:
        return Usuario(usuario[0], usuario[1])
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
            login_user(Usuario(usuario[0], usuario[1]))
            return redirect(url_for('admin'))
        flash('Login inválido!')
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', usuario=current_user)

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
  #return render_template('index.html')

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

if __name__ == "__main__":
  criar_tabelas()
  app.run()
