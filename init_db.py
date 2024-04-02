import sqlite3

def connect():
    return sqlite3.connect('database.db')

def criar_tabelas():
    conn = connect()
    c = conn.cursor()
   
    with open('schema.sql') as f:
        c.executescript(f.read())
   
    c.execute("""
      INSERT OR IGNORE INTO usuarios (nome, senha) VALUES (?, ?)
    """, ('admin', 'senha_admin'))
   
    c.execute("""
      INSERT OR IGNORE INTO usuarios (nome, senha) VALUES (?, ?)
    """, ('usuario1', 'senha_usuario1'))

    c.execute("""INSERT INTO contato (whatsapp, facebook, instagram, email, endereco) VALUES (?, ?, ?, ?, ?)
    """, ('+5519996848921', 'https://www.facebook.com/semearamericana?mibextid=JRoKGi', 'https://www.instagram.com/semearamericana_?igsh=ZGV6ajRmcmt6Zm9u', 'semearamericana@gmail.com', 'R. Serra de Maracajú, 124 - Parque da Liberdade - Americana - SP, 13470-441'))
   
    c.execute("""INSERT INTO mensagem_bottom (texto) VALUES (?)
    """, ('© 2024 Website desenvolvido por alunos da UNIVESP para o Projeto Integrador em Computação.',))

    c.execute("""
      INSERT INTO posts (title, content) VALUES (?, ?)
    """, ('Publicação teste 1', 'Esta é uma publicação teste para exibição de postagens.'))

    c.execute("""
      INSERT INTO posts (title, content) VALUES (?, ?)
    """, ('Publicação teste 2', 'Esta é uma publicação teste para exibição de postagens.'))

    c.execute("""
      INSERT INTO posts (title, content) VALUES (?, ?)
    """, ('Publicação teste 3', 'Esta é uma publicação teste para exibição de postagens.'))

    conn.commit()
    conn.close()
