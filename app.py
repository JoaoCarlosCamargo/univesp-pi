import sqlite3
from flask import Flask, render_template
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

@app.route('/')
def index():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  contato = conn.execute('SELECT whatsapp, facebook, instagram, email, endereco FROM contato').fetchall()
  mensagem_bottom = conn.execute('SELECT texto FROM mensagem_bottom').fetchall()
  conn.close()
  return render_template('index.html', posts=posts, contato=contato, mensagem_bottom=mensagem_bottom)
  #return render_template('index.html')

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/semeie')
def semeie():
  return render_template('semeie.html')

if __name__ == "__main__":
  app.run()
