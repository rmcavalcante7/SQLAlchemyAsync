import asyncio
import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures


class Sabor(ModelBase):
    __tablename__ = 'sabor'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Sabor(nome={self.nome})>'


    @staticmethod
    async def insertSabor(nome: str) -> 'Sabor' or None:
        """Insere um Sabor na tabela sabor
        :param nome: str: nome do Sabor
        :return: Sabor or None: Retorna o objeto Sabor se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome não for string
        :raises ValueError: Se o nome não for informado
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o sabor, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Sabor deve ser uma string!')

            nome = nome.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Sabor não informado!')

            sabor = Sabor(nome=nome)
            session = await createSession()
            async with session.begin():
                print(f'Inserindo Sabor: {sabor}')
                session.add(sabor)
                await session.commit()

                print(f'Sabor inserido com sucesso!')
                print(f'ID do Sabor inserido: {sabor.id}')
                print(f'Nome do Sabor inserido: {sabor.nome}')
                print(f'Data de criação do Sabor inserido: {sabor.data_criacao}')
            return sabor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'sabor.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Sabor com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir sabor: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

        finally:
            if session:
                await session.close()

    @staticmethod
    def selectAllSabores() -> list['Sabor'] or []:
        """Seleciona todos os Sabores na tabela sabor
        raises Exception: Informa erro inesperado ao selecionar Sabores
        :return: list[Sabor] or []: Retorna uma lista de objetos Sabor se houver registros, [] caso contrário
        """
        try:
            with createSession() as session:
                sabores = session.query(Sabor).all()
                return sabores
        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Sabor: {exc}')

    @staticmethod
    def selectSaborPorId(id: int) -> 'Sabor' or None:
        """Seleciona um Sabor na tabela sabor por id
        :param id: int: id do Sabor
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: Sabor or None: Retorna o objeto Sabor se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do Sabor deve ser um inteiro!')

            if not id:
                raise ValueError('id do Sabor não informado!')

            with createSession() as session:
                sabor = session.query(Sabor).filter(Sabor.id == id).first()
                return sabor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Sabor por id: {exc}')

    @staticmethod
    def selectSaborPorNome(nome: str) -> 'Sabor' or None:
        """Seleciona um Sabor na tabela sabor por nome
        :param nome: str: nome do Sabor
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :return: Sabor or None: Retorna o objeto Sabor se encontrado, None caso contrário
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Sabor deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do Sabor não informado!')

            with createSession() as session:
                sabor = session.query(Sabor).filter(Sabor.nome == nome).first()
                return sabor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Sabor por nome: {exc}')

    @staticmethod
    def updateSabor(id_sabor: int, nome: str = '') -> 'Sabor':
        """Atualiza um Sabor na tabela sabor
        :param id_sabor: int: id do Sabor
        :param nome: str: nome do Sabor
        :return: Sabor: Retorna o objeto Sabor atualizado
        :raises TypeError: Se o id_sabor não for inteiro
        :raises TyperError: Se o nome não for string
        :raises ValueError: Se o nome não for informado ou for composto só por espaços
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o sabor, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is int
            if not isinstance(id_sabor, int):
                raise TypeError('id do Sabor deve ser um inteiro!')

            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Sabor deve ser uma string!')

            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do Sabor não pode ser composto só por espaços!')

            nome = nome.strip().upper()

            with createSession() as session:
                sabor = session.query(Sabor).filter_by(id=id_sabor).first()

                if not sabor:
                    raise ValueError(f'Sabor com o ID {id_sabor} não cadastrado na base!')

                if nome:
                    sabor.nome = nome
                else:
                    nome = sabor.nome

                sabor.data_atualizacao = datetime.now()
                session.commit()
                return sabor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'sabor.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Sabor com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir sabor: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao atualizar Sabor: {exc}')

    @staticmethod
    def deleteSaborById(id_sabor: int) -> 'Sabor':
        """Deleta um Sabor cadastrado no banco de dados a partir do id.
        :param id_sabor: int: identificador do Sabor
        :return: Sabor: Retorna o objeto Sabor deletado
        :raises TypeError: Se o id_sabor não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o Sabor, especificado para o
        id_sabor, caso o Sabor esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o Sabor não for encontrado na base
        """
        try:
            if not isinstance(id_sabor, int):
                raise TypeError('id_sabor do Sabor deve ser um inteiro!')

            with createSession() as session:
                sabor: Sabor = session.query(Sabor). \
                    filter_by(id=id_sabor).first()

                if not sabor:
                    raise ValueError(f'Sabor com id={id_sabor} não cadastrado na base!')

                session.delete(sabor)
                session.commit()
                return sabor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=Sabor.__tablename__)
                raise RuntimeError(f'Sabor com id={id_sabor} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar Sabor: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar Sabor: {exc}')


if __name__ == '__main__':
    # try:
    #     Sabor.insertSabor(nome='Morango')
    # except Exception as e:
    #     print(f'Erro ao inserir Sabor: {e}')
    #
    # try:
    #     Sabor.insertSabor(nome='Morango')
    # except Exception as e:
    #     print(f'Erro ao inserir Sabor: {e}')
    #
    # try:
    #     Sabor.insertSabor(nome='Coco')
    # except Exception as e:
    #     print(f'Erro ao inserir Sabor: {e}')
    #
    # print('fim')

    # sabor = Sabor.updateSabor(id_sabor=2,
    #                           nome='  ')
    # print(sabor)
    
    try:
        sabor = Sabor.deleteSaborById(id_sabor=90)
        print(sabor)
    except Exception as e:
        print(f'Erro ao deletar Sabor: {e}')

        