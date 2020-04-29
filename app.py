from flask import Flask, request, url_for, redirect, render_template, g
import sqlite3

app = Flask(__name__)

#
# conexao com o banco
#

def connect_db():
    sql = sqlite3.connect('/Users/fabio/flask/data.db')
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

@app.route('/', methods=['GET','POST'])
def index():
    db = get_db()
    if request.method == 'GET':
        cur  = db.execute('select cpf, display from pagador')
        results = cur.fetchall()
        return render_template('cafe.html',results=results)
    else:
        aux1 = request.form['v_cpf']
        aux2 = request.form['v_quantidade']
        
        db.execute('insert into conta_cafe (cpf, quantidade) values (?,?)',[aux1,aux2])
        db.commit()
        
        cur = db.execute('select sum(quantidade) as v_quant from conta_cafe')
        r_soma_cafe = cur.fetchall()
        
        cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade from conta_cafe a, pagador b where a.cpf = b.cpf and strftime(\'%m\', a.data) = strftime(\'%m\', \'now\') group by a.cpf order by a.quantidade;')
        r_consumo_mes_atual = cur.fetchall()
        
        cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade from conta_cafe a, pagador b where a.cpf = b.cpf group by a.cpf order by a.quantidade;')
        results2 = cur.fetchall()
        
        return render_template('lista_cafe.html', r_soma_cafe=r_soma_cafe, r_consumo_mes_atual=r_consumo_mes_atual, r_consumo_total=r_consumo_total)



@app.route('/cafe', methods=['GET','POST'])
def cafe():
    db = get_db()
    if request.method == 'GET':
        cur  = db.execute('select cpf, display from pagador')
        results = cur.fetchall()
        return render_template('cafe.html',results=results)
    else:
        aux1 = request.form['v_cpf']
        aux2 = request.form['v_quantidade']
        
        db.execute('insert into conta_cafe (cpf, quantidade) values (?,?)',[aux1,aux2])
        db.commit()
        
        cur = db.execute('select sum(quantidade) as v_quant from conta_cafe')
        r_soma_cafe = cur.fetchall()
        
        cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade from conta_cafe a, pagador b where a.cpf = b.cpf and strftime(\'%m\', a.data) = strftime(\'%m\', \'now\') group by a.cpf order by a.quantidade;')
        r_consumo_mes_atual = cur.fetchall()
        
        cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade from conta_cafe a, pagador b where a.cpf = b.cpf group by a.cpf order by a.quantidade;')
        results2 = cur.fetchall()
        
        return render_template('lista_cafe.html', r_soma_cafe=r_soma_cafe, r_consumo_mes_atual=r_consumo_mes_atual, r_consumo_total=r_consumo_total)

@app.route('/lista', methods=['GET'])
def lista():
    db = get_db()
    
    cur = db.execute('select sum(quantidade) as v_quant from conta_cafe')
    r_soma_cafe = cur.fetchall()

    cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade \
        from conta_cafe a, pagador b \
        where a.cpf = b.cpf and strftime(\'%m\', a.data) = strftime(\'%m\', \'now\') \
        group by a.cpf \
        order by a.quantidade;')
    r_consumo_mes_atual = cur.fetchall()

    cur = db.execute('select a.cpf cpf, b.display display, sum(a.quantidade) quantidade \
        from conta_cafe a, pagador b \
        where a.cpf = b.cpf \
        group by a.cpf \
        order by a.quantidade;')
    r_consumo_total = cur.fetchall()
    
    return render_template('lista_cafe.html', r_soma_cafe=r_soma_cafe, r_consumo_mes_atual=r_consumo_mes_atual, r_consumo_total=r_consumo_total)


