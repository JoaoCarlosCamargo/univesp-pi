DROP TABLE IF EXISTS contato;

CREATE TABLE contato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    whatsapp TEXT NOT NULL,
    facebook TEXT NOT NULL,
    instagram TEXT NOT NULL,
    email TEXT NOT NULL,
    endereco TEXT NOT NULL
);

DROP TABLE IF EXISTS mensagem_bottom;

CREATE TABLE mensagem_bottom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    texto TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nome TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT NOT NULL,
  report_file BLOB NOT NULL,
  report_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS textos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  quem_somos TEXT NOT NULL,
  visao_semear TEXT NOT NULL,
  missao_semear TEXT NOT NULL,
  sobre_a_comunidade TEXT NOT NULL,
  nossa_historia TEXT NOT NULL,
  atividades TEXT NOT NULL,
  parceiros TEXT NOT NULL,
  transparencia TEXT NOT NULL,
  novidades TEXT NOT NULL,
  semeie_voluntariado TEXT NOT NULL,
  semeie_colaboradores TEXT NOT NULL,
  semeie_refeicoes TEXT NOT NULL,
  semeie_veiculo TEXT NOT NULL,
  semeie_sede_propria TEXT NOT NULL,
  semeie_colaboracoes_mensais TEXT NOT NULL,
  semeie_colaboracoes_eventuais TEXT NOT NULL,
  semeie_doacao_materiais TEXT NOT NULL,
  semeie_empresa_que_semeia TEXT NOT NULL
);