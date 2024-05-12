import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures


class TipoEmbalagem(ModelBase):
    __tablename__ = 'tipo_embalagem'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Tipo Embalagem(nome={self.nome})>'


    @staticmethod
    def insertTipoEmbalagem(nome: str) -> 'TipoEmbalagem' or None:
        """Insere um TipoEmbalagem na tabela tipo_embalagem
        :param nome: str: nome do TipoEmbalagem
        :return: TipoEmbalagem or None: Retorna o objeto TipoEmbalagem se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome não for string
        :raises ValueError: Se o nome não for informado
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o TipoEmbalagem, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do TipoEmbalagem deve ser uma string!')

            nome = nome.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do TipoEmbalagem não informado!')

            tipo_embalagem = TipoEmbalagem(nome=nome)

            with createSession() as session:
                print(f'Inserindo TipoEmbalagem: {tipo_embalagem}')
                session.add(tipo_embalagem)
                session.commit()

                print(f'Tipo Embalagem inserido com sucesso!')
                print(f'ID do TipoEmbalagem inserido: {tipo_embalagem.id}')
                print(f'Nome do TipoEmbalagem inserido: {tipo_embalagem.nome}')
                print(f'Data de criação do TipoEmbalagem inserido: {tipo_embalagem.data_criacao}')
            return tipo_embalagem

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'tipo_embalagem.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um TipoEmbalagem com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir TipoEmbalagem: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllTipoEmbalagens() -> list['TipoEmbalagem'] or []:
        """Seleciona todos os TipoEmbalagens na tabela tipo_embalagem
        :raises Exception: Informa erro inesperado ao selecionar TipoEmbalagens
        :return: list[TipoEmbalagem] or []: Retorna uma lista de objetos TipoEmbalagem se houver registros, [] caso contrário
        """
        try:
            with createSession() as session:
                tipo_embalagens = session.query(TipoEmbalagem).all()
                return tipo_embalagens

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos TipoEmbalagem: {exc}')

    @staticmethod
    def selectTipoEmbalagemPorId(id: int) -> 'TipoEmbalagem' or None:
        """Seleciona um TipoEmbalagem na tabela tipo_embalagem por id
        :param id: int: id do TipoEmbalagem
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: TipoEmbalagem or None: Retorna um objeto TipoEmbalagem se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do TipoEmbalagem deve ser um inteiro!')

            if not id:
                raise ValueError('id do TipoEmbalagem não informado!')

            with createSession() as session:
                tipo_embalagem = session.query(TipoEmbalagem).filter(TipoEmbalagem.id == id).first()
                return tipo_embalagem

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar TipoEmbalagem por id: {exc}')

    @staticmethod
    def selectTipoEmbalagemPorNome(nome: str) -> 'TipoEmbalagem' or None:
        """Seleciona um TipoEmbalagem na tabela tipo_embalagem por nome
        :param nome: str: nome do TipoEmbalagem
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :return: TipoEmbalagem or None: Retorna um objeto TipoEmbalagem se encontrado, None caso contrário
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do TipoEmbalagem deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do TipoEmbalagem não informado!')

            with createSession() as session:
                tipo_embalagem = session.query(TipoEmbalagem).filter(TipoEmbalagem.nome == nome).first()
                return tipo_embalagem

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar TipoEmbalagem por nome: {exc}')

    
    @staticmethod
    def updateTipoEmbalagem(id_tipo_embalagem: int, nome: str = '') -> 'TipoEmbalagem':
        """Atualiza um TipoEmbalagem na tabela tipo_embalagaem
        :param id_tipo_embalagem: int: id do tipo_embalagaem
        :param nome: str: nome do tipo_embalagaem
        :return: TipoEmbalagem: Retorna o objeto TipoEmbalagem se atualizado com sucesso, None caso contrário
        :raises TypeError: Se o id_tipo_embalagaem não for inteiro
        :raises TyperError: Se o nome não for string
        :raises ValueError: Se o nome não for informado ou for composto só por espaços
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o TipoEmbalagem, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is integer
            if not isinstance(id_tipo_embalagem, int):
                raise TypeError('id do TipoEmbalagem deve ser um inteiro!')

            if not isinstance(nome, str):
                raise TypeError('nome do TipoEmbalagem deve ser uma string!')

            # check if is string
            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do TipoEmbalagem não pode ser composto só por espaços!')

            nome = nome.strip().upper()

            with createSession() as session:
                tipo_embalagaem = session.query(TipoEmbalagem).filter_by(id=id_tipo_embalagem).first()

                if not tipo_embalagaem:
                    raise ValueError(f'TipoEmbalagem com id={id_tipo_embalagem} não cadastrado na base!')

                if nome:
                    tipo_embalagaem.nome = nome
                else:
                    nome = tipo_embalagaem.nome

                tipo_embalagaem.data_atualizacao = datetime.now()
                session.commit()
                return tipo_embalagaem

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'tipo_embalagem.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um TipoEmbalagem com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir TipoEmbalagem: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exp:
            raise Exception(f'Erro inesperado ao atualizar TipoEmbalagem: {exp}')

    @staticmethod
    def deleteTipoEmbalagemById(id_tipo_embalagem: int) -> 'TipoEmbalagem':
        """Deleta um TipoEmbalagem cadastrado no banco de dados a partir do id.
        :param id_tipo_embalagem: int: identificador do TipoEmbalagem
        :return: TipoEmbalagem: Retorna o objeto TipoEmbalagem deletado
        :raises TypeError: Se o id_tipo_embalagem não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o TipoEmbalagem, especificado para o
        id_tipo_embalagem, caso o TipoEmbalagem esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o TipoEmbalagem não for encontrado na base
        """
        try:
            if not isinstance(id_tipo_embalagem, int):
                raise TypeError('id do TipoEmbalagem deve ser um inteiro!')

            with createSession() as session:
                tipo_embalagem: TipoEmbalagem = session.query(TipoEmbalagem). \
                    filter_by(id=id_tipo_embalagem).first()

                if not tipo_embalagem:
                    raise ValueError(f'TipoEmbalagem com id={id_tipo_embalagem} não cadastrado na base!')

                session.delete(tipo_embalagem)
                session.commit()
                return tipo_embalagem

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=TipoEmbalagem.__tablename__)
                raise RuntimeError(f'TipoEmbalagem com id={id_tipo_embalagem} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar TipoEmbalagem: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar TipoEmbalagem: {exc}')



if __name__ == '__main__':
    # try:
    #     TipoEmbalagem.insertTipoEmbalagem(nome='Pote')
    # except Exception as e:
    #     print(f'Erro ao inserir TipoEmbalagem: {e}')
    #
    # try:
    #     TipoEmbalagem.insertTipoEmbalagem(nome='Pote')
    # except Exception as e:
    #     print(f'Erro ao inserir TipoEmbalagem: {e}')
    #
    # try:
    #     TipoEmbalagem.insertTipoEmbalagem(nome='Caixa')
    # except Exception as e:
    #     print(f'Erro ao inserir TipoEmbalagem: {e}')

    # tipo_embalagen = TipoEmbalagem.updateTipoEmbalagem(id_tipo_embalagem=4532,
    #                                                    nome='Pote')
    #
    # print(tipo_embalagen)


    try:
        tipo_embalagen = TipoEmbalagem.deleteTipoEmbalagemById(id_tipo_embalagem=71)
        print(tipo_embalagen)
    except Exception as e:
        print(f'Erro ao deletar TipoEmbalagem: {e}')
