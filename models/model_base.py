# Este módulo é responsável por criar a classe ModelBase, que é uma classe base para todos os modelos que serão criados
# para representar as tabelas do banco de dados.

import sqlalchemy.ext.declarative


# ModelBase is a class that will be inherited by all the models we create
ModelBase = sqlalchemy.ext.declarative.declarative_base()
