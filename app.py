import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from init_db import criar_tabelas, login
from werkzeug.exceptions import abort

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
