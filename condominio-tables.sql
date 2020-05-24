Pergunta
    Id_Pergunta (PK)
    Pergunta
    Visivel
    Owner
    Data

Opcoes
    Id_Opcoes (PK)
    Opcao
    Id_Pergunta (FK)
    
cond_respostas
    id_pergunta
    id_morador (PK)
    id_opcao
    data






DROP TABLE IF EXISTS 'condominio_moradores';

CREATE TABLE IF NOT EXISTS 'condominio_moradores' 
    ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 
     'andar' INTEGER NOT NULL, 
     'apto' INTEGER NOT NULL, 
     'nome'  VARCHAR NOT NULL , 
     'apelido' VARCHAR NOT NULL, 
     'email' VARCHAR, 
     'telefone' VARCHAR, 
     'senha'  VARCHAR NOT NULL, 
     'nascimento' DATETIME, 
     'sobre_voce' VARCHAR,
     'sobre_familia' VARCHAR,    
     'tipo' VARCHAR NOT NULL,
     'status' VARCHAR default 'block',
     'foto' VARCHAR,
     'filhos' integer,
     'admin' VARCHAR default 'n'
    );


INSERT INTO 'condominio_moradores' 
    ('andar', 
     'apto', 
     'nome', 
     'apelido', 
     'email', 
     'telefone', 
     'senha', 
     'tipo'
    )
VALUES (
    12,
    1,
    'FABIO TAVARES',
    'TAVARES',
    'mendonca.tavares@gmail.com',
    '982225527',
    '11111',
    'admin'
    );
    