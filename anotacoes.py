        <link rel="stylesheet" href="{{ url_for('static', filename='css/estilo_cafe.css') }}">



    
    
    
                session['user'] = v_pagador;
            session['projeto'] = v_id_projeto;
            user = session['user']
            cur  = db.execute('select  id_usuario, nome_pagador, email_pagador, cpf, display_pagador from cafe_pagador where id_projeto = ?', [v_id_projeto])
            r_lista_usuarios = cur.fetchall()
            return render_template('cafe_list_user.html', r_lista_usuarios=r_lista_usuarios,user=user)
        
        
        
        

    
    @app.route('/cafe_add_user', methods=['GET','POST'])
def cafe_add_user():
    db = get_db()
    if request.method == 'GET':    
        if 'user' in session:
            user = session['user']
            projeto = session['projeto']
            return render_template('cafe_add_user.html', projeto)
        return '<h1> Nao pode ser  Admin</h1>'
    else:
        v_nome = request.form['v_nome'] 
        v_display = request.form['v_display'] 
        v_email = request.form['v_email'] 
        v_senha = request.form['v_senha'] 
        return '<h1> Usuario: {}, Apelido: {} e Senha: {} </h1>'.format(v_nome, v_display, v_senha)