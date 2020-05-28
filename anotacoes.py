select andar,apto, andar||apto x from condominio_moradores where cast(x as int) = 122;
            
            
            
            


##

        <link rel="stylesheet" href="{{ url_for('static', filename='css/estilo_cafe.css') }}">
   
## Backup do Menu
##

                <div class="menu">
                <ul class="menu-list">
                  {% if admin == 'y' %}
                      <li> <a href="/admin"> Admin </a>
                          <ul class="sub-menu">
                            <li><a href="#">List User</a></li>
                            <li><a href="#">Add User</a></li>
                          </ul>
                      </li>
                  {% endif %}
                      <li><a href="/cafe_inserir">Pagar</a></li>
                      <li><a href="/cafe_lista">Quem Paga?</a></li>
                  {% if not user %}
                      <li><a href="/"> Login </a></li>
                  {% endif %}
                  {% if user %}
                      <li><a href="/"> Logout </a></li>
                  {% endif %}      
                </ul>
                </div>       
                
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
