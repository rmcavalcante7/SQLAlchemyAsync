import sqlalchemy as sa
from conf.db_session import createSession


class DataBaseFeatures:

    @staticmethod
    def findTabelsWithFkTo(table_name: str):
        """Encontra todas as tabelas que têm uma FK para a tabela especificada.
        :param table_name: Nome da tabela para a qual você deseja encontrar as FKs.
        :param engine: Objeto de conexão do SQLAlchemy.
        :return: Lista de nomes de tabelas que têm FK para a tabela especificada.
        """
        try:
            engine = createSession().get_bind()
            inspector = sa.inspect(engine)
            fk_tables = []

            for table in inspector.get_table_names():
                for fk in inspector.get_foreign_keys(table):
                    if fk['referred_table'] == table_name:
                        fk_tables.append(table)

            return fk_tables
        except Exception as e:
            print(f'Erro ao tentar encontrar tabelas com FK para "{table_name}": {e}')
            return []

