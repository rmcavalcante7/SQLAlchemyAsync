import asyncio
import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from sqlalchemy.exc import IntegrityError
from conf.db_session import createSession
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures


class Ingrediente(ModelBase):
    __tablename__ = 'ingrediente'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(45), unique=True, nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Ingrediente (nome={self.nome})>'

    
    @staticmethod
    async def insertIngrediente(nome: str) -> 'Ingrediente' or None:
        """Insere um Ingrediente na tabela ingrediente
        :param nome: str: nome do ingrediente
        :return: Ingrediente or None: Retorna o objeto Ingrediente se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome ou não for strings
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o ingrediente, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Ingrediente deve ser uma string!')
    
            nome = nome.strip().upper()
    
            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Ingrediente não informado!')
    
            ingrediente = Ingrediente(nome=nome)
            session = await createSession()
            async with session.begin():
                print(f'Inserindo Ingrediente: {ingrediente}')
                session.add(ingrediente)
                await session.commit()
    
                print(f'Ingrediente inserido com sucesso!')
                print(f'ID do Ingrediente inserido: {ingrediente.id}')
                print(f'Nome do Ingrediente inserido: {ingrediente.nome}')
                print(f'Data de criação do Ingrediente inserido: {ingrediente.data_criacao}')
            return ingrediente
    
        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'ingrediente.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Ingrediente com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de Ingrediente ao inserir ingrediente: {intg_error}')
    
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
    def selectAllIngredientes() -> list['Ingrediente'] or []:
        """Seleciona todos os Ingredientes na tabela ingrediente
        :raises Exception: Informando erro inesperado
        :return: list or []: Retorna a lista de objetos Ingredientes se encontrados, [] caso contrário
        """
        try:
            with createSession() as session:
                ingredientes = session.query(Ingrediente).all()
                return ingredientes
    
        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar Ingredientes: {exc}')

    @staticmethod
    def selectIngredientePorId(id: int) -> 'Ingrediente' or None:
        """Seleciona um Ingrediente na tabela ingrediente por id
        :param id: int: id do ingrediente
        :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
        """
        try:
            # check if is integer
            if not isinstance(id, int):
                raise TypeError('id do Ingrediente deve ser um inteiro!')
    
            # validar se os parâmetros informados são válidos
            if not id:
                raise ValueError('id do Ingrediente não informado!')
    
            with createSession() as session:
                ingrediente = session.query(Ingrediente).filter(Ingrediente.id == id).first()
                return ingrediente
    
        except TypeError as te:
            raise TypeError(te)
    
        except ValueError as ve:
            raise ValueError(ve)
    
        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectIngredientePorNome(nome: str) -> 'Ingrediente' or None:
        """Seleciona um Ingrediente na tabela ingrediente por nome
        :param nome: str: nome do ingrediente
        :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        :return: Ingrediente or None: Retorna o objeto Ingrediente se encontrado, None caso contrário
        """
        try:
            # check if is string
            if not isinstance(nome, str):
                raise TypeError('nome do Ingrediente deve ser uma string!')
    
            nome = nome.strip().upper()
    
            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Ingrediente não informado!')
    
            with createSession() as session:
                ingrediente = session.query(Ingrediente).filter(Ingrediente.nome == nome).first()
                return ingrediente
    
        except TypeError as te:
            raise TypeError(te)
    
        except ValueError as ve:
            raise ValueError(ve)
    
        except Exception as exc:
            print(f'Erro inesperado: {exc}')


    @staticmethod
    def updateIngrediente(id_ingrediente: int, nome: str = '') -> 'Ingrediente':
        """Atualiza um Ingrediente na tabela ingrediente
        :param id_ingrediente: int: id do ingrediente
        :param nome: str: nome do ingrediente
        :return: Ingrediente: Retorna o objeto Ingrediente se atualizado com sucesso
        :raises TypeError: Se o id_ingrediente não for inteiro
        :raises TyperError: Se o nome não for string
        :raises ValueError: Se o nome não for informado ou for composto só por espaços
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o ingrediente, especificado para o nome. Caso
        seja por outro motivo, será lançado um erro genérico.
        """
        try:
            # check if is integer
            if not isinstance(id_ingrediente, int):
                raise TypeError('id do Ingrediente deve ser um inteiro!')

            if not isinstance(nome, str):
                raise TypeError('nome do Ingrediente deve ser uma string!')

            # check if is string
            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do Ingrediente não pode ser composto só por espaços!')

            nome = nome.strip().upper()

            with createSession() as session:
                ingrediente = session.query(Ingrediente).filter_by(id=id_ingrediente).first()

                if not ingrediente:
                    raise ValueError(f'Ingrediente com id={id_ingrediente} não cadastrado na base!')

                if nome:
                    ingrediente.nome = nome
                else:
                    nome = ingrediente.nome

                ingrediente.data_atualizacao = datetime.now()

                session.commit()
                return ingrediente

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'ingrediente.nome' in str(intg_error):
                    raise RuntimeError(f"Já existe um Ingrediente com o nome '{nome}' cadastrado. "
                                       f"O nome deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de Ingrediente ao inserir ingrediente: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exp:
            raise Exception(f'Erro inesperado ao atualizar Ingrediente: {exp}')

    @staticmethod
    def deleteIngredienteById(id_ingrediente: int) -> 'Ingrediente':
        """Deleta um Ingrediente cadastrado no banco de dados a partir do id.
        :param id_ingrediente: int: identificador do Ingrediente
        :return: Ingrediente: Retorna o objeto Ingrediente deletado
        :raises TypeError: Se o id não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o Ingrediente, especificado para o
        id, caso o Ingrediente esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o Ingrediente não for encontrado na base
        """
        try:
            if not isinstance(id_ingrediente, int):
                raise TypeError('id do Ingrediente deve ser um inteiro!')

            with createSession() as session:
                ingrediente: Ingrediente = session.query(Ingrediente). \
                    filter_by(id=id_ingrediente).first()

                if not ingrediente:
                    raise ValueError(f'Ingrediente com id={id_ingrediente} não cadastrado na base!')

                session.delete(ingrediente)
                session.commit()
                return ingrediente

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=Ingrediente.__tablename__)
                raise RuntimeError(f'Ingrediente com id={id_ingrediente} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')

            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar Ingrediente: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar Ingrediente: {exc}')


if __name__ == '__main__':
    try:
        Ingrediente.insertIngrediente(nome='sal2')
    except Exception as e:
        print(f'Erro ao inserir Ingrediente: {e}')

    # try:
    #     Ingrediente.insertIngrediente(nome='açúcar')
    # except Exception as e:
    #     print(f'Erro ao inserir Ingrediente: {e}')
    #

    # ingrediente = Ingrediente.updateIngrediente(id_ingrediente=3,
    #                                             nome='açucar')
    # print('ingrediente')

    try:
        ingrediente = Ingrediente.deleteIngredienteById(id_ingrediente=98)
        print(ingrediente)
    except Exception as e:
        print(f'Erro ao deletar Ingrediente: {e}')
