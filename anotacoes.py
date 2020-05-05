##

        <link rel="stylesheet" href="{{ url_for('static', filename='css/estilo_cafe.css') }}">

    
    
## Backup do Menu
##

{% macro show_menu(user) %}
    <nav>
        <ul>
            {% if not user %}
                <li><a href="/">Login</a></li>
            {% endif %}
            <li><a href="/cafe_inserir">Tomou?</a></li>
            <li><a href="/cafe_lista">Quem?</a></li>
            {% if user %}
                <li><a href="/logout">Logout</a></li>
            {% endif %}
        </ul>
    </nav>
{% endmacro %}

##
## Script Banco de Dados
##



insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 100,10,5,'2020-03-10' )

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 200,10,4,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 300,10,6,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 400,10,3,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 100,10,4,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 200,10,6,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 300,10,3,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 400,10,5,'2020-04-10' );



insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 500,20,4,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 500,20,6,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 600,20,3,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 600,20,5,'2020-04-10' );


insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 504,30,7,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 505,30,8,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 506,30,6,'2020-03-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 504,30,5,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 505,30,4,'2020-04-10' );

insert into cafe_ordens( id_pagador, id_projeto, quantidade, data )
values( 506,30,5,'2020-04-10' );
