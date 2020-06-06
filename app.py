from flask import Flask, request, url_for, redirect, render_template, g, session
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["IMAGE_UPLOADS"] = "/Users/fabio/flask/static/imagens"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


# conexao com o banco
# configuracao correta 

def connect_db():
    sql = sqlite3.connect('/Users/fabio/flask/condominio.db')
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
    
#
# termino da configuracao de conexao do bloco_faleconosco
#


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        if 'user' in session:
            db = get_db()
            user = session['user']
            admin = session['admin']
            v_visible = 'y'
            cur = db.execute('select id_pergunta, pergunta from cond_pergunta where visivel = ?', [v_visible])
            r_perguntas = cur.fetchall()                
            return render_template('condominio_inicio.html', r_perguntas=r_perguntas, user=user, admin=admin)                    
        else:
            return render_template('condominio_base.html')

        
@app.route('/login', methods=['GET','POST'])
def login():
    db = get_db()
    if request.method == 'GET':
        return render_template('condominio_login.html')
    else:
        v_andar     = request.form['form-cadastro-andar']
        v_apto      = request.form['form-cadastro-apto']
        v_senha     = request.form['form-cadastro-senha'] 
        v_tipo      = 'owner'
        cur = db.execute('select id, nome, senha, tipo, admin from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
        r_morador = cur.fetchone()        
        
        if not r_morador:
            return 'nao cadastrado ainda'
        
        if r_morador['senha'] == v_senha:
            session['user'] = r_morador['id']
            session['admin'] = r_morador['admin']
            user = session['user']
            admin = session['admin']
            v_visible = 'y'
            cur = db.execute('select id_pergunta, pergunta from cond_pergunta where visivel = ?', [v_visible])
            r_perguntas = cur.fetchall()                
            return render_template('condominio_inicio.html', r_perguntas=r_perguntas, user=user, admin=admin)        
        else:   
            return 'senha invalida'
    

@app.route('/new_login', methods=['GET','POST'])
def new_login():
    db = get_db()
    if request.method == 'GET':
        return render_template('condominio_base.html')
    else:
        v_apto      = request.form['f-login-apto']
        v_senha     = request.form['f-login-senha'] 
        v_tipo      = 'owner'

        cur = db.execute('select id, nome, andar||apto apto_morador, senha, tipo, admin from condominio_moradores where tipo = ? and cast(apto_morador as int) = ?',[v_tipo, v_apto])
        r_morador = cur.fetchone()        
            
        if not r_morador:
            return 'nao cadastrado ainda'
        
        if r_morador['senha'] == v_senha:
            session['user'] = r_morador['id']
            session['admin'] = r_morador['admin']
            user = session['user']
            admin = session['admin']
            v_visible = 'y'
            cur = db.execute('select id_pergunta, pergunta from cond_pergunta where visivel = ?', [v_visible])
            r_perguntas = cur.fetchall()                
            return render_template('condominio_inicio.html', r_perguntas=r_perguntas, user=user, admin=admin)        
        else:   
            return 'senha invalida'


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    db = get_db()
    if request.method == 'GET':
        return render_template('condominio_user_01_inicial.html')        
    else:
        v_andar     = request.form['form-cadastro-andar']
        v_apto      = request.form['form-cadastro-apto']
        v_nome      = request.form['form-cadastro-nome']
        v_email     = request.form['form-cadastro-email']       
        v_apelido   = request.form['form-cadastro-apelido']
        v_foto      = request.files['form-cadastro-foto']
        v_telefone  = request.form['form-cadastro-telefone']
        v_senha     = request.form['form-cadastro-senha']
        v_tipo      = 'owner'

        if v_foto.filename == "":
            return 'precisa enviar um arquivo com nome'

        if not allowed_image(v_foto.filename):
            return 'precisa enviar outro formato'
        
        cur = db.execute('select id from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
        r_morador = cur.fetchone()
        if r_morador:
            return 'morador ja exite'

        v_arquivo = str(v_andar)+str(v_apto)+'.jpg'
    
        v_foto.filename = v_arquivo
        v_foto.save(os.path.join(app.config["IMAGE_UPLOADS"], v_foto.filename))            
              
        cur = db.execute('INSERT INTO condominio_moradores (andar, apto, nome, apelido, email, telefone, senha, tipo, foto) VALUES (?,?,?,?,?,?,?,?,?)',[v_andar,v_apto,v_nome,v_apelido,v_email,v_telefone,v_senha,v_tipo,v_arquivo])

        cur  = db.execute('select id,admin from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
        r_morador = cur.fetchone()        
        
        session['user']  = r_morador['id']
        session['admin'] = r_morador['admin']
        user = session['user']
        admin = session['admin']
        db.commit()
        
        cur  = db.execute('select id, andar, apto, nome, apelido, email, telefone, nascimento, sobre_voce, sobre_familia, tipo, status, foto, admin from condominio_moradores where tipo = ? and andar = ? and apto = ?',[v_tipo, v_andar, v_apto])
        r_morador = cur.fetchone()                
            
        return render_template('condominio_user_02_modificar.html', r_morador=r_morador, user=user,  admin=admin)


@app.route('/atualiza_morador', methods=['POST', 'GET'])
def add_morador():
    db = get_db()
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            admin = session['admin']

            cur  = db.execute('select andar, apto, nome, apelido, email, telefone, nascimento, sobre_voce, sobre_familia, tipo, status, foto,filhos from condominio_moradores where id=?',[user])
            r_morador = cur.fetchone()                
            
            v_andar = r_morador['andar'] 
            v_apto  = r_morador['apto'] 
            v_tipo  = 'owner'
            
            cur  = db.execute('select id, nome, apelido, tipo,nascimento,sobre_voce,sobre_familia, foto, filhos from condominio_moradores where andar=? and apto=? and tipo<>? ',[v_andar, v_apto, v_tipo])
            r_todos = cur.fetchall()                
        
            return render_template('condominio_user_02_modificar.html', r_morador=r_morador, user=user,  admin=admin, r_todos = r_todos)     
        
        else:
            return 'Precisa estar logado'
            
    else:
        if 'user' in session:
            user = session['user']
            admin = session['admin']
            v_nome          = request.form['form-cadastro-nome']
            v_email         = request.form['form-cadastro-email']       
            v_apelido       = request.form['form-cadastro-apelido']
            v_telefone      = request.form['form-cadastro-telefone']
            v_nascimento    = request.form['form-cadastro-nascimento']
            v_filhos        = request.form['form-cadastro-filhos']
            v_sobre_voce    = request.form['form-cadastro-sobre_voce']
            v_sobre_familia = request.form['form-cadastro-sobre_familia']
            db.execute('update condominio_moradores set nome=?, apelido=?, email=?, telefone=?, nascimento=?, sobre_voce=?, sobre_familia=?, filhos=? where id = ?', [v_nome,v_apelido, v_email, v_telefone, v_nascimento, v_sobre_voce, v_sobre_familia, v_filhos, user])
            
            db.commit()    
            
            return redirect(url_for('index'))
        
        else:
            return 'Precisa estar logado'
        

@app.route('/add_integrante', methods=['POST', 'GET'])
def add_integrante():
    db = get_db()
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            admin = session['admin']

            cur  = db.execute('select andar, apto from condominio_moradores where id=?',[user])
            r_morador = cur.fetchone() 

            return render_template('condominio_user_03_addmorador.html', r_morador  = r_morador , user=user, admin=admin)
        else:
            return 'Precisa estar logado'        
    else:
            v_tipo          = request.form['form-cadastro-tipo']
            v_nome          = request.form['form-cadastro-nome']
            v_email         = request.form['form-cadastro-email']       
            v_telefone      = request.form['form-cadastro-telefone']
            v_apelido       = request.form['form-cadastro-apelido']
            v_nascimento    = request.form['form-cadastro-nascimento']
            v_sobre_voce    = request.form['form-cadastro-voce']

            user = session['user']
            admin = session['admin']

            cur  = db.execute('select andar, apto from condominio_moradores where id=?',[user])
            r_morador = cur.fetchone() 
            v_andar = r_morador['andar']
            v_apto  = r_morador['apto']
            v_senha = '1133557799'
  
            cur = db.execute('INSERT INTO condominio_moradores (andar, apto, nome, apelido, email, telefone, senha, tipo, nascimento, sobre_voce) VALUES (?,?,?,?,?,?,?,?,?,?)',[v_andar, v_apto, v_nome, v_apelido, v_email, v_telefone, v_senha, v_tipo, v_nascimento, v_sobre_voce])
            
            db.commit()
            
            return 'Inserido com sucesso'
        
        
@app.route('/lista_predio', methods=['POST', 'GET'])
def listar_predio():
    db = get_db()

    if 'user' in session:
        user = session['user']
        admin = session['admin']

        cur = db.execute('select id, nome, apelido, andar, apto from condominio_moradores order by andar, apto')
        r_lista_predio = cur.fetchall()

        return render_template('condominio_user_05_listar.html', r_lista_predio = r_lista_predio, user=user, admin=admin)
    else:
        return 'Precisa estar logado'


@app.route('/detalha_apartamento', methods=['POST', 'GET'])
def detalha_apartamento():
    db = get_db()
    if 'user' in session:
        user = session['user']
        admin = session['admin']
        v_id = request.args.get('id')
        cur = db.execute('select andar, apto, nome, apelido, email, telefone, nascimento, sobre_voce, sobre_familia, tipo, filhos,foto from condominio_moradores where id = ?',[v_id])
        r_detalha = cur.fetchone()                
        return render_template('condominio_detalha_morador.html', r_detalha = r_detalha, user=user, admin=admin)
    else:
        return 'Precisa estar logado'    
    

        
@app.route('/detalha_morador', methods=['POST', 'GET'])  
def detalha_morador():
    db = get_db()
    if request.method == 'GET':    
        v_id = request.args.get('id')
        cur = db.execute('select id, apto, andar, tipo, nome, apelido, email, telefone, nascimento, sobre_voce from condominio_moradores where id =?', [v_id])
        r_morador = cur.fetchone()
        return render_template('condominio_user_04_modifymorador.html', r_morador=r_morador)
    else:
            v_id            = request.form['form-cadastro-id']
            v_tipo          = request.form['form-cadastro-tipo']
            v_nome          = request.form['form-cadastro-nome']
            v_email         = request.form['form-cadastro-email']       
            v_apelido       = request.form['form-cadastro-apelido']
            v_telefone      = request.form['form-cadastro-telefone']
            v_nascimento    = request.form['form-cadastro-nascimento']
            v_voce          = request.form['form-cadastro-voce']
            db.execute('update condominio_moradores set tipo=?, nome=?, email=?, apelido=?, telefone=?, nascimento=?, sobre_voce=? where id=?', [v_tipo, v_nome, v_email, v_apelido, v_telefone, v_nascimento, v_voce, v_id])
            
            db.commit()    
            return 'Atualizado com sucesso'
        
# ***************************************************
# Parte da aplicacao das enquetes                   *
# ***************************************************

@app.route('/cond_enquete', methods=['POST', 'GET'])  
def cond_enquete():
    db = get_db()
    if request.method == 'GET':    
        if 'user' in session:
            user = session['user']
            admin = session['admin']
            v_visible = 'y'
            cur = db.execute('select id_pergunta, pergunta from cond_pergunta where visivel = ?', [v_visible])
            r_perguntas = cur.fetchall()    
            return render_template('cond_lista_enquete.html', r_perguntas=r_perguntas, user=user, admin=admin)

                
@app.route('/cond_opcoes', methods=['POST', 'GET'])  
def cond_opcoes(): 
    db = get_db()
    if request.method == 'GET':    
        if 'user' in session:
            user = session['user']
            admin = session['admin']
            v_id = request.args.get('id')
            
            cur = db.execute('select b.opcao opcao from cond_respostas a, cond_opcoes b where a.id_opcao = b.id_opcao and a.id_morador = ? and a.id_pergunta = ?', [user, v_id])
            r_morador = cur.fetchone()
            
            cur = db.execute('select pergunta from cond_pergunta where id_pergunta = ?', [v_id])
            r_pergunta = cur.fetchone()
            
            if r_morador:
                return render_template('condominio_votacao_erro.html', r_morador=r_morador,user=user, admin=admin)
            else:
                cur = db.execute('select id_pergunta, id_opcao, opcao from cond_opcoes where id_pergunta = ?', [v_id])
                r_opcoes = cur.fetchall()    
                
                cur = db.execute('select a.nome nome, b.comentario comentario from cond_forum_enquete b, condominio_moradores a where a.id = b.id_morador and b.id_enquete = ?', [v_id])
                r_forum = cur.fetchall()
        
                return render_template('cond_lista_opcoes.html', r_opcoes=r_opcoes,user=user, admin=admin, r_pergunta = r_pergunta, r_forum=r_forum)
    else:
        if 'user' in session:
            user = session['user']
            admin = session['admin']
            v_opcao    = request.form['form-enquete_opcao']
            v_pergunta = request.form['form-enquete_pergunta']
            
            cur = db.execute('INSERT INTO cond_respostas (id_pergunta,id_morador,id_opcao) VALUES (?,?,?)',[v_pergunta,user,v_opcao])
            
            db.commit()
            
            cur = db.execute('select b.opcao opcao, count(a.id_opcao) votos from cond_respostas a, cond_opcoes b where a.id_pergunta = ? and a.id_opcao = b.id_opcao group by a.id_opcao', [v_pergunta])
            r_enquete_placar = cur.fetchall()
            
            cur = db.execute('select id_pergunta, pergunta from cond_pergunta where id_pergunta = ?', [v_pergunta])
            r_pergunta = cur.fetchone()
    
            cur = db.execute('select a.nome nome, b.comentario comentario from cond_forum_enquete b, condominio_moradores a where a.id = b.id_morador and b.id_enquete = ?', [v_pergunta])
            r_forum = cur.fetchall()
            
            return render_template('cond_enquete_placar.html', r_enquete_placar=r_enquete_placar,user=user, admin=admin, r_pergunta = r_pergunta, r_forum=r_forum)
        
        
@app.route('/cond_enquete_placar', methods=['POST', 'GET'])  
def cond_enquete_placar(): 
    db = get_db()
    if 'user' in session:
        user = session['user']
        admin = session['admin']        
        v_pergunta = request.args.get('id')
       
        cur = db.execute('select b.opcao opcao, count(a.id_opcao) votos from cond_respostas a, cond_opcoes b where a.id_pergunta = ? and a.id_opcao = b.id_opcao group by a.id_opcao', v_pergunta)
        r_enquete_placar = cur.fetchall()    
        
        cur = db.execute('select id_pergunta, pergunta from cond_pergunta where id_pergunta = ?', [v_pergunta])
        r_pergunta = cur.fetchone()        
        
        cur = db.execute('select a.nome nome, b.comentario comentario from cond_forum_enquete b, condominio_moradores a where a.id = b.id_morador and b.id_enquete = ?', [v_pergunta])
        r_forum = cur.fetchall()        
        
        return render_template('cond_enquete_placar.html', r_enquete_placar=r_enquete_placar,user=user, admin=admin, r_pergunta = r_pergunta, r_forum = r_forum) 
    
@app.route('/add_comentario_enquete', methods=['POST', 'GET'])
def add_comentario_enquete(): 
    db = get_db()
    if 'user' in session:
        user    = session['user']
        admin   = session['admin']        
        v_comentario  = request.form['add-com-enquete']
        v_id_pergunta = request.form['id-pergunta-forum']
        
        cur = db.execute('INSERT INTO cond_forum_enquete (id_enquete, id_morador, comentario) VALUES (?,?,?)',[v_id_pergunta,user,v_comentario])

        db.commit()

        cur = db.execute('select b.opcao opcao, count(a.id_opcao) votos from cond_respostas a, cond_opcoes b where a.id_pergunta = ? and a.id_opcao = b.id_opcao group by a.id_opcao', [v_id_pergunta])
        r_enquete_placar = cur.fetchall()    
        
        cur = db.execute('select id_pergunta, pergunta from cond_pergunta where id_pergunta = ?', [v_id_pergunta])
        r_pergunta = cur.fetchone()        
        
        cur = db.execute('select a.nome nome, b.comentario comentario from cond_forum_enquete b, condominio_moradores a where a.id = b.id_morador and b.id_enquete = ?', [v_id_pergunta])
        r_forum = cur.fetchall()        
        
        return render_template('cond_enquete_placar.html', r_enquete_placar=r_enquete_placar, user=user, admin=admin, r_pergunta = r_pergunta, r_forum = r_forum)                 
    
@app.route('/cond_agendar_visita', methods=['POST', 'GET'])  
def cond_agendar_visita(): 
    db = get_db()
    if 'user' in session:
        user = session['user']
        admin = session['admin']        
        if request.method == 'POST':    
            v_nome      = request.form['form-agenda-nome']
            v_doc       = request.form['form-agenda-doc']
            v_detalhe   = request.form['form-agenda-detalhe']
            v_data      = request.form['form-agenda-data']
            v_turno     = request.form['form-agenda-turno']
            
            cur = db.execute('insert into cond_agenda_visitas (nome,doc,detalhe,id_usuario,data_visita, turno) values (?,?,?,?,?,?)',[v_nome,v_doc,v_detalhe,user,v_data,v_turno])
            
            db.commit()
        
        cur  = db.execute('select andar, apto from condominio_moradores where id=?',[user])
        r_morador = cur.fetchone()         
        
        cur_visitas  = db.execute('select nome, doc, data_visita, turno from cond_agenda_visitas where id_usuario = ? order by data_visita',[user])
        r_visitas = cur_visitas.fetchall()         
        
        return render_template('condominio_agendar_vista.html',user=user, admin=admin, r_morador=r_morador, r_visitas=r_visitas)
    else:
        return 'precisa logar'

# ***************************************************************
# Agenda do Salaao de Festa                                     *
# ***************************************************************
    
@app.route('/cond_agendar_salao', methods=['POST', 'GET'])  
def cond_agendar_salao(): 
    db = get_db()
    if 'user' in session:
        user = session['user']
        admin = session['admin']        
        if request.method == 'POST':    
            v_detalhe   = request.form['form-agenda-detalhe']
            v_data      = request.form['form-agenda-data']
            v_turno     = request.form['form-agenda-turno']
            
            cur = db.execute('insert into cond_agenda_salao (id_morador, data_reserva, turno_reserva, observacao) values (?,?,?,?)',[user,v_data,v_turno,v_detalhe])
            
            db.commit()
        
        cur  = db.execute('select andar, apto from condominio_moradores where id=?',[user])
        r_morador = cur.fetchone()         
        
        cur_visitas  = db.execute('select id_morador,data_reserva,turno_reserva,observacao from cond_agenda_salao where id_morador=?',[user])
        r_visitas = cur_visitas.fetchall()         
        
        return render_template('condominio_agendar_salao.html',user=user, admin=admin, r_morador=r_morador, r_visitas=r_visitas)
    else:
        return 'precisa logar'
    
    
    
# ***************************************************************
# Administracao da Pagina
# ***************************************************************
    
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'GET':
        if 'user' in session:
            db = get_db()
            user = session['user']
            admin = session['admin']

            cur = db.execute('select a.id_usuario morador, b.andar andar, b.apto apto, count(*) from cond_agenda_visitas a, condominio_moradores b where a.id_usuario = b.id group by a.id_usuario')
            r_un_apto = cur.fetchall()    
            
            cur = db.execute('select b.id morador, b.apelido morador, b.andar andar, b.apto apto, a.nome visitante, a.doc doc, a.data_visita data_visita, a.turno turno, strftime(\'%d\',a.data_visita) dia_visita, strftime(\'%m\',\'now\') mes_visita from cond_agenda_visitas a, condominio_moradores b where a.id_usuario = b.id and strftime(\'%d\',a.data_visita) = strftime(\'%d\',datetime(\'now\',\'-3 hour\')) and strftime(\'%m\',a.data_visita) = strftime(\'%m\',datetime(\'now\',\'-3 hour\')) order by a.data_visita')
            r_agenda_dia = cur.fetchall()    
            
            cur = db.execute('select a.nome nome, a.andar, a.apto, b.data_reserva data_reserva, b.turno_reserva turno_reserva, b.observacao observacao from condominio_moradores a, cond_agenda_salao b where a.id = b.id_morador and b.data_reserva >= date(\'now\') order by b.data_reserva')
            r_agenda_salao = cur.fetchall()    

            return render_template('condominio_admin.html', r_agenda_dia = r_agenda_dia, user=user, admin=admin, r_agenda_salao = r_agenda_salao, r_un_apto = r_un_apto)     

    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))             