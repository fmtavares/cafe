from flask import Flask, request, url_for, redirect, render_template, g, session
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.config["IMAGE_UPLOADS"] = "/Users/fabio/flask/static/imagens"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 5 * 1024 * 1024


# conexao com o banco
# configuracao correta 

def connect_db():
    sql = sqlite3.connect('condominio.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return  g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False
        
        
        
#
# termino da configuracao de conexao do bloco_faleconosco
#
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    db = get_db()
    if request.method == 'GET':
        return render_template('condominio_user_01_inicial.html')
    else:
        v_andar       = request.form['form-cadastro-andar']
        v_apto        = request.form['form-cadastro-apto']
        v_nome        = request.form['form-cadastro-nome']
        v_apelido     = request.form['form-cadastro-apelido']        
        v_email       = request.form['form-cadastro-email']
        v_telefone    = request.form['form-cadastro-telefone']
        v_senha       = request.form['form-cadastro-senha']
        v_tipo        = 'owner'

        cur  = db.execute('select id from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
        r_morador = cur.fetchone()
        
        if r_morador:
            return 'morador ja exite'
        else:        
            db.execute('INSERT INTO condominio_moradores (andar, apto, nome, apelido, email, telefone, senha, tipo) VALUES (?,?,?,?,?,?,?,?)',[v_andar, v_apto, v_nome, v_apelido, v_email, v_telefone, v_senha, v_tipo])
            db.commit()

            cur  = db.execute('select id from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
            r_morador = cur.fetchone()        

            return 'Morador com ID {}'.format(r_morador['id'])
            session['user'] = r_senha['display_pagador'];

            return 'Inserido com sucesso'


@app.route('/teste', methods=['GET', 'POST'])
def teste():
    db = get_db()
    if request.method == 'POST':
        if request.files:
            v_nome = request.form['form-nome']
            image = request.files["image"]
            
            if image.filename == "":
                return 'precisa enviar um arquivo com nome'

            if not allowed_image(image.filename):
                return 'precisa enviar outro formato'
        
            db.execute('INSERT INTO teste (name) values (?)', [v_nome])
            db.commit()

            cur = db.execute('select id from teste where name = ?', [v_nome])
            r_morador = cur.fetchone()      

            aux = str(r_morador['id'])+'.jpg'

            image.filename = aux
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))            
            return render_template('teste.html', aux = aux)
    return render_template('condominio_teste.html')



