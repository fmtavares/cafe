from flask import Flask, request, url_for, redirect, render_template, g, session
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
#
# conexao com o banco
# configuracao correta 

def connect_db():
    sql = sqlite3.connect('/Users/fabio/flask/teste.db')
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

#
# termino da configuracao de conexao do bloco_faleconosco
#

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            projeto = session['projeto'] 
            cur  = db.execute('select admin from cafe_pagador where display_pagador = ?', [user])
            r_senha = cur.fetchone()    
            if r_senha['admin']=='y':
                return render_template('cafe_admin.html', user=user, projeto=projeto)
            return '<h1> NEM VENHA QUE NAO EH ADMIN </h1>'
        return '<h1> PRECISA LOGAR </h1>'
    
@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    if request.method == 'GET':
        cur  = db.execute('select id_projeto, display_projeto from cafe_projetos')
        r_lista_projetos = cur.fetchall()
        return render_template('cafe_inicio.html',r_lista_projetos=r_lista_projetos)
    else:
        v_id_projeto    = request.form['v_id_projeto']
        v_pagador       = request.form['v_pagador']
        v_senha         = request.form['v_senha']        
        cur  = db.execute('select senha from cafe_pagador where id_projeto = ? and lower(display_pagador) = lower(?)', [v_id_projeto, v_pagador])
        r_senha = cur.fetchone()
        if r_senha and v_senha == r_senha['senha']:
            session['user'] = v_pagador;
            session['projeto'] = v_id_projeto;
            user = session['user']
            projeto = session['projeto'] 
            cur  = db.execute('select id_usuario, display_pagador from cafe_pagador where id_projeto = ?', [v_id_projeto])
            r_lista_usuarios = cur.fetchall()
            return render_template('cafe_inserir.html', r_lista_usuarios=r_lista_usuarios,user=user, projeto=projeto)
        return render_template('cafe_erro_autenticacao.html')

@app.route('/cafe_inserir', methods=['GET','POST'])
def cafe_inserir():
    db = get_db()
    projeto = None
    user = None
    if request.method == 'GET':
        if 'user' in session:
            user = session['user']
            projeto = session['projeto'] 
            cur  = db.execute('select id_usuario, display_pagador from cafe_pagador where id_projeto = ?', [projeto])
            r_lista_usuarios = cur.fetchall()
            return render_template('cafe_inserir.html',r_lista_usuarios=r_lista_usuarios,user=user)
        else: 
            return render_template('cafe_nao.html')
    else:
        user = session['user']
        projeto = session['projeto'] 
        v_id = request.form['v_id']
        v_quantidade = request.form['v_quantidade'] 
        db.execute('insert into cafe_ordens (id_pagador, id_projeto, quantidade) values (?,?,?)',[v_id, projeto, v_quantidade])
        db.commit()
        
        cur = db.execute('select sum(quantidade) soma from cafe_ordens where id_projeto=?', [projeto])
        r_soma_total = cur.fetchone()   
        
        cur = db.execute('select sum(quantidade) soma from cafe_ordens where id_projeto = ? and strftime(\'%m\', data) = strftime(\'%m\', \'now\')', [projeto])
        r_soma_periodo = cur.fetchone()   
        
        cur = db.execute('select b.nome_pagador display, sum(a.quantidade) quantidade from cafe_ordens a, cafe_pagador b where a.id_projeto = ? and a.id_pagador = b.id_usuario and strftime(\'%m\', a.data) = strftime(\'%m\', \'now\') group by a.id_pagador order by 2 desc', [projeto])
        r_distribuicao_mes = cur.fetchall()
        
        cur = db.execute('select b.nome_pagador display, sum(a.quantidade) quantidade from cafe_ordens a, cafe_pagador b where a.id_projeto = ? and a.id_pagador = b.id_usuario group by a.id_pagador order by 2 desc', [projeto])
        r_distribuicao_total = cur.fetchall()
        
        return render_template('cafe_lista.html', r_soma_total=r_soma_total, r_soma_periodo=r_soma_periodo, r_distribuicao_mes=r_distribuicao_mes, r_distribuicao_total=r_distribuicao_total,user=user)
        
@app.route('/cafe_lista', methods=['GET'])
def lista():
    db = get_db()
    if 'user' in session:
        user = session['user']
        projeto = session['projeto'] 
    
        cur = db.execute('select sum(quantidade) soma from cafe_ordens where id_projeto=?', [projeto])
        r_soma_total = cur.fetchone()   
        
        cur = db.execute('select sum(quantidade) soma from cafe_ordens where id_projeto = ? and strftime(\'%m\', data) = strftime(\'%m\', \'now\')', [projeto])
        r_soma_periodo = cur.fetchone()   
        
        cur = db.execute('select b.nome_pagador display, sum(a.quantidade) quantidade from cafe_ordens a, cafe_pagador b where a.id_projeto = ? and a.id_pagador = b.id_usuario and strftime(\'%m\', a.data) = strftime(\'%m\', \'now\') group by a.id_pagador order by 2 desc', [projeto])
        r_distribuicao_mes = cur.fetchall()
        
        cur = db.execute('select b.nome_pagador display, sum(a.quantidade) quantidade from cafe_ordens a, cafe_pagador b where a.id_projeto = ? and a.id_pagador = b.id_usuario group by a.id_pagador order by 2 desc', [projeto])
        r_distribuicao_total = cur.fetchall()
        
        return render_template('cafe_lista.html', r_soma_total=r_soma_total, r_soma_periodo=r_soma_periodo, r_distribuicao_mes=r_distribuicao_mes, r_distribuicao_total=r_distribuicao_total,user=user)
    
    return render_template('cafe_nao.html')
  
@app.route('/cafe_add_user', methods=['GET','POST'])
def cafe_add_user():
    db = get_db()
    if request.method == 'GET':    
        if 'user' in session:
            user = session['user']
            projeto = session['projeto']
            return render_template('cafe_add_user.html', projeto=projeto)
        return '<h1> Nao pode ser  Admin</h1>'
    else:
        v_nome      = request.form['v_nome'] 
        v_apelido  = request.form['v_apelido'] 
        v_email     = request.form['v_email'] 
        v_senha     = request.form['v_senha'] 
        user = session['user']
        projeto = session['projeto']
        db.execute('insert into cafe_pagador (nome_pagador, display_pagador, id_projeto, senha) values (?,?,?,?)',[v_nome, v_apelido, projeto, v_senha])
        db.commit()      
        cur = db.execute('select id_usuario, nome_pagador, email_pagador, display_pagador from cafe_pagador where id_projeto=?', [projeto])
        r_list_user = cur.fetchall()        
        return render_template('cafe_list_user.html', r_list_user = r_list_user)


@app.route('/cafe_list_user', methods=['GET','POST'])
def cafe_list_user():
    db = get_db()
    if request.method == 'GET':    
        if 'user' in session:
            user = session['user']
            projeto = session['projeto']
            cur = db.execute('select id_usuario, nome_pagador, email_pagador, display_pagador from cafe_pagador where id_projeto=?', [projeto])
            r_list_user = cur.fetchall()
            return render_template('cafe_list_user.html', r_list_user = r_list_user)    
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index')) 

@app.route('/teste')
def teste():
    projeto = None
    user = None
    if 'user' in session:
        user = session['user']
        projeto = session['projeto'] 
    return render_template('teste.html', user=user, projeto=projeto)