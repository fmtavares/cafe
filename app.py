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
        cur  = db.execute('select id_projeto, display_projeto from cafe_projetos')
        r_lista_projetos = cur.fetchall()
        return render_template('cafe_admin.html',r_lista_projetos=r_lista_projetos)
    else:
        v_id_projeto    = request.form['v_id_projeto']
        v_pagador       = request.form['v_pagador']
        v_senha         = request.form['v_senha']        
        cur  = db.execute('select senha, admin from cafe_pagador where id_projeto = ? and display_pagador = ?', [v_id_projeto, v_pagador])
        r_senha = cur.fetchone()
        if v_senha == r_senha['senha'] and r_senha['admin']=='y':
            session['user'] = v_pagador;            
            return '<h1> Uuario {} do Projeto {} com senha digitada {} e senha do banco {}: COM SUCESSO </h1>'.format(v_id_projeto, v_pagador, v_senha, r_senha['senha'])
        return '<h1> Uuario {} do Projeto {} com senha digitada {} e senha do banco {}: SEM SUCESSO </h1>'.format(v_id_projeto, v_pagador, v_senha, r_senha['senha'])

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
        cur  = db.execute('select senha from cafe_pagador where id_projeto = ? and display_pagador = ?', [v_id_projeto, v_pagador])
        r_senha = cur.fetchone()
        if v_senha == r_senha['senha']:
            session['user'] = v_pagador;
            session['projeto'] = v_id_projeto;
            cur  = db.execute('select id_usuario, display_pagador from cafe_pagador where id_projeto = ?', [v_id_projeto])
            r_lista_usuarios = cur.fetchall()
            return render_template('cafe_inserir.html', r_lista_usuarios=r_lista_usuarios)     

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
            return render_template('cafe_inserir.html',r_lista_usuarios=r_lista_usuarios)
        else: 
            return '<h1> PRECISA LOGAR </h1>' 
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
        
        return render_template('cafe_lista.html', r_soma_total=r_soma_total, r_soma_periodo=r_soma_periodo, r_distribuicao_mes=r_distribuicao_mes, r_distribuicao_total=r_distribuicao_total)
        
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
        
        return render_template('cafe_lista.html', r_soma_total=r_soma_total, r_soma_periodo=r_soma_periodo, r_distribuicao_mes=r_distribuicao_mes, r_distribuicao_total=r_distribuicao_total)
    
    return '<h1> Nao esta logado </h1>'
  
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