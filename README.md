A aplicação consiste em guardar pontos geograficos e disponibilizar pesquisa por proximidade, nome, categoria.
Usuario pode adicionar imagens, comentarios e favoritar os pontos geograficos.

Subir o ambiente:
 Primeiramente faça o clone do repositorio e execute o build do container:
  `git clone https://github.com/lucassempre/find`
  `docker-compose -f build/docker-compose-api.yml build`
 Se os comandos anteriores forem um sucesso, seu container esta elegível a subir com o comando a seguir:
  `docker-compose -f build/docker-compose-api.yml up`

Cada ponto geografico é salvo no banco relacional e referenciados num banco não relacional. 
O redis é utilizado para gerenciar a descoberta dos pontos por determinada distancia.
Caso o container não salve o estado do Redis, podemos recontruir ele com o comando:
  `python manager.py generate_geodb`
  Todos os pontos serão salvos novamento no redis e o processamento geografico de distancia estara funcional.

Retorna os pontos vinculados ao usuario logado.
    api/v1/me/point/
Retorna os comentarios vinculados ao usuario logado.
    api/v1/me/comment/
Retorna as imagens viculadas ao usuario logado.
    api/v1/me/image/
Retorna as categorias
    api/v1/category/
Retorna a categoria, editar, remover
    api/v1/category/<int:pk>/
Retorna comentario, editar, remover  
    api/v1/comment/<uuid:pk>/
Retorna imagem, editar, remover
    api/v1/image/<uuid:pk>/
Retorna os pontos que estão no raio especificado pelo parametro radius, partindo dos parametros de latitude e longitude 
    api/v1/point/<str:latitude>/<str:longitude>/radius/<int:radius>/
Retorna os pontos que estão na categoria no raio especificado pelos paramametros, partindo dos parametros de latitude e longitude 
    api/v1/point/<str:latitude>/<str:longitude>/radius/<int:radius>/category/<int:category>/
 Retorna o ponto, editar, remover
    api/v1/point/<uuid:pk>/
    
 Fazer login:
  `curl -X POST http://0.0.0.0:8000/api/v1/auth/login/ -d "password=lucas" -d "username=lucas"`
 Fazer request:
  `curl -X POST http://0.0.0.0:8000/api/v1/point/-25.441202/-49.246076/radius/10/ -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imx1Y2FzIiwiZXhwIjoxNTgyODI5OTg4LCJlbWFpbCI6Imx1Y2Fzcy5zZW1wcmVib21AZ21haWwuY29tIn0.7-of8CZQ-Kv1XnBPTObejwPgrmxFA4_xp_W1CEQMXWI"`
    
Arquivos principais da aplicação:
 Basicamento toda a aplicação e regra de negocio se encontra aqui:
 `find/api/snow/apps/points/rest_api/views/point_views.py`
 `find/api/snow/apps/points/rest_api/serializers/point.py`
 O banco relacional é descrito aqui:
 `find/api/snow/apps/points/models/point.py`
 Interface para disponibilizar a pesquisa por distancia se encontra aqui:
 `find/api/snow/apps/points/utils/redis.py`

Autenticação segue as definições:
https://github.com/Tivix/django-rest-auth/

Esqueleto da aplicação:
https://be.skeletons.djangostars.com/

 
