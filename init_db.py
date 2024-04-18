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
      DELETE FROM textos
    """)

    quem_somos_texto = """<p>A Semear Americana é uma Organização da Sociedade Civil, inscrita sob o CNPJ 32.787.100/0001-04, fundada em 2016 que atende mais de 150 crianças e adolescentes em situação de vulnerabilidade social na comunidade do Zincão e arredores, localizada no bairro Parque da Liberdade, cidade de Americana. Estamos empenhados em proporcionar um ambiente enriquecedor de oportunidades que contribuam para o desenvolvimento integral desses jovens, promovendo transformações positivas em suas vidas e impactando na comunidade em que estão inseridos.
<br><br>
Em 2016 nasceu a Semear, um sonho realizado de nossa presidente e fundadora Bianca Vanessa Cordasso Ferraz, uma voluntária que dedica sua vida à este trabalho com muito amor e determinação!</p>"""

    visao_semear_texto = """<p>Buscamos ser referência na transformação de vidas, reconhecendo que a mudança em crianças e adolescentes reverbera em suas famílias. Apresentamos diversas possibilidades e recursos, visando criar uma comunidade em que todos possuam acesso aos meios necessários para construir uma realidade distinta da experienciada, promovendo assim autonomia e superação de adversidades iniciais. Nosso compromisso reside em impactar positivamente não apenas indivíduos, mas também as estruturas familiares e a comunidade como um todo.</p>"""

    c.execute("""
      INSERT INTO textos (quem_somos, visao_semear, missao_semear, sobre_a_comunidade, nossa_historia, atividades, parceiros, transparencia, novidades, semeie_voluntariado, semeie_colaboradores, semeie_refeicoes, semeie_veiculo, semeie_sede_propria, semeie_colaboracoes_mensais, semeie_colaboracoes_eventuais, semeie_doacao_materiais, semeie_empresa_que_semeia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (quem_somos_texto, visao_semear_texto, 'missao_semear', 'sobre_a_comunidade', 'nossa_historia', 'atividades', 'parceiros', 'transparencia', 'novidades', 'semeie_voluntariado', 'semeie_colaboradores', 'semeie_refeicoes', 'semeie_veiculo', 'semeie_sede_propria', 'semeie_colaboracoes_mensais', 'semeie_colaboracoes_eventuais', 'semeie_doacao_materiais', 'semeie_empresa_que_semeia'))

    conn.commit()
    conn.close()
