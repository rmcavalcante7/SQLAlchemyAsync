import asyncio

import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures

class Conservante(ModelBase):
    __tablename__ = 'conservante'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(45), nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Conservante (nome={self.nome}, descrição={self.descricao})>'

    @staticmethod
    async def insertConservante(nome: str, descricao: str) -> 'Conservante' or None:
        """Insere um Conservante na tabela conservante
        :param nome: str: nome do conservante
        :param descricao: str: fórmula química do conservante
        :return: Conservante or None: Retorna o objeto Conservante se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome ou a descrição não forem strings
        :raises ValueError: Se o nome ou a descrição não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o conservante, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Conservante deve ser uma string!')
            if not isinstance(descricao, str):
                raise TypeError('descricao do Conservante deve ser uma string!')

            nome = nome.strip().upper()
            descricao = descricao.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Conservante não informado!')
            if not descricao:
                raise ValueError('descricao do Conservante não informada!')

            conservante = Conservante(nome=nome, descricao=descricao)
            session = await createSession()
            async with session.begin():
                print(f'Inserindo Conservante: {conservante}')
                session.add(conservante)
                await session.commit()

                print(f'Conservante inserido com sucesso!')
                print(f'ID do Conservante inserido: {conservante.id}')
                print(f'Nome do Conservante inserido: {conservante.nome}')
                print(f'Descrição do Conservante inserido: {conservante.descricao}')
                print(f'Data de criação do Conservante inserido: {conservante.data_criacao}')
            return conservante

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'conservante.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Conservante com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir Conservante: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Conservante: {exc}')

        finally:
            if session:
                await session.close()

    @staticmethod
    def selectAllConservantes() -> list['Conservante'] or []:
        """Seleciona todos os Conservantes na tabela conservante
        :raises Exception: Informando erro inesperado ao selecionar os conservantes
        :return: list or []: Retorna uma lista de objetos Conservante se encontrado, [] caso contrário
        """
        try:
            with createSession() as session:
                conservantes = session.query(Conservante).all()
                return conservantes

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Conservantes: {exc}')

    @staticmethod
    def selectConservantePorID(id: int) -> 'Conservante' or None:
        """Seleciona um Conservante na tabela conservante por ID
        :param id: int: id do Conservante
        :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar o conservante
        :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
        """

        try:
            # check if is int
            if not isinstance(id, int):
                raise TypeError('id do Conservante deve ser um inteiro!')

            # validar se o id informado é válido
            if not id:
                raise ValueError('id do Conservante não informado!')

            with createSession() as session:
                conservante = session.query(Conservante).filter(Conservante.id == id).first()
                return conservante

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectConservantePorNome(nome: str) -> 'Conservante' or None:
        """Seleciona um Conservante na tabela conservante por nome
        :param nome: str: nome do Conservante
        :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar o conservante
        :return: Conservante or None: Retorna o objeto Conservante se encontrado, None caso contrário
        """

        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Conservante deve ser uma string!')

            nome = nome.strip().upper()

            # validar se o nome informado é válido
            if not nome:
                raise ValueError('nome do Conservante não informado!')

            with createSession() as session:
                conservante = session.query(Conservante).filter(Conservante.nome == nome).first()
                return conservante

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')


    @staticmethod
    def updateConservante(id_conservante: int, nome: str = '', descricao: str = '') -> 'Conservante':
        """Atualiza um Conservante na tabela conservante
        :param id_conservante: int: id do Conservante
        :param nome: str: nome do Conservante
        :param descricao: str: fórmula química do Conservante
        :return: Conservante: Retorna o objeto Conservante atualizado
        :raises TypeError: Se o id, nome ou a descrição não forem inteiros
        :raises ValueError: Se o id, nome ou a descrição não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o conservante, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        try:
            # check if is int
            if not isinstance(id_conservante, int):
                raise TypeError('id do Conservante deve ser um inteiro!')

            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Conservante deve ser uma string!')

            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do Conservante não pode ser composto só por espaços!')

            if not isinstance(descricao, str):
                raise TypeError('descricao do Conservante deve ser uma string!')

            if len(descricao) > 0 and all(caractere.isspace() for caractere in descricao):
                raise ValueError('descricao do Conservante não pode ser composto só por espaços!')

            nome = nome.strip().upper()
            descricao = descricao.strip().upper()

            with createSession() as session:
                conservante = session.query(Conservante).filter_by(id=id_conservante).first()

                if not conservante:
                    raise ValueError(f'Conservante com o ID {id_conservante} não cadastrado na base!')

                if nome:
                    conservante.nome = nome
                else:
                    nome = conservante.nome

                if descricao:
                    conservante.descricao = descricao

                conservante.data_atualizacao = datetime.now()
                session.commit()
                return conservante

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'conservante.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Conservante com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")

            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao atualizar Conservante: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao atualizar Conservante: {exc}')

    @staticmethod
    def deleteConservanteById(id_conservante: int) -> 'Conservante':
        """Deleta um Conservante cadastrado no banco de dados a partir do id.
        :param id_conservante: int: identificador do Conservante
        :return: Conservante: Retorna o objeto Conservante deletado
        :raises TypeError: Se o id não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o Conservante, especificado para o
        id, caso o Conservante esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o Conservante não for encontrado na base
        """
        try:
            if not isinstance(id_conservante, int):
                raise TypeError('id do Conservante deve ser um inteiro!')

            with createSession() as session:
                conservante: Conservante = session.query(Conservante). \
                    filter_by(id=id_conservante).first()

                if not conservante:
                    raise ValueError(f'Conservante com id={id_conservante} não cadastrado na base!')

                session.delete(conservante)
                session.commit()
                return conservante

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=Conservante.__tablename__)
                raise RuntimeError(f'Conservante com id={id_conservante} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar Conservante: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar Conservante: {exc}')


if __name__ == '__main__':
    # try:
    #     Conservante.insertConservante(nome='Sorbato de Potássio',
    #                                   descricao='Utilizado para conservar alimentos. '
    #                                             'Evita a proliferação de fungos e leveduras.')
    # except Exception as e:
    #     print(f'Erro ao inserir Conservante: {e}')
    #
    # try:
    #     Conservante.insertConservante(nome='Benzoato de Sódio',
    #                                   descricao='Utilizado para conservar alimentos. '
    #                                             'É útil para conservar alimentos ácidos, '
    #                                             'como sucos de frutas.')
    # except Exception as e:
    #     print(f'Erro ao inserir Conservante: {e}')

    # conservante = Conservante.updateConservante(id_conservante=1999,
    #                                             nome='',
    #                                             descricao='Utilizado para conservar alimentos. '
    #                                                       'Evita a proliferação de fungos e leveduras.'
    #                                                       ' Conservante muito utilizado na indústria alimentícia.'
    #                                             )
    # print(conservante)

    try:
        conservante = Conservante.deleteConservanteById(id_conservante=43)
        print(conservante)
    except Exception as e:
        print(f'Erro ao deletar Conservante: {e}')
