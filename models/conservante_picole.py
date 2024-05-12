import asyncio

from typing import Union

import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.picole import Picole
from models.conservante import Conservante
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class ConservantePicole(ModelBase):
    __tablename__ = 'conservante_picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True,
                        autoincrement=True)

    picole_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                               sa.ForeignKey('picole.id'),
                               nullable=False
                               )
    picole: Picole = orm.relationship('Picole', lazy='joined')

    conservante_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                    sa.ForeignKey('conservante.id'),
                                    nullable=False
                                    )
    conservante: Conservante = orm.relationship('Conservante', lazy='joined')

    # chave forte para impedir duplicidade
    conservante_picole: str = sa.Column(sa.String(200),
                                        unique=True,
                                        nullable=False)

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        return (f'ConservantePicole(id={self.id}, '
                f'picole_fk={self.picole_fk}, '
                f'conservante_fk={self.conservante_fk})'
                f'conservante_picole={self.conservante_picole}'
                )

    @staticmethod
    async def insertConservantePicole(picole_fk: int, conservante_fk: int) -> 'ConservantePicole' or None:
        """Insere um ConservantePicole na tabela conservante_picole
        :param picole_fk: int: id do picolé
        :param conservante_fk: int: id do conservante
        :return: ConservantePicole or None: Retorna o objeto ConservantePicole se inserido com sucesso, None caso contrário
        :raises TypeError: Se o picole_fk ou o conservante_fk não forem inteiros
        :raises RuntimeError: Se as FKs picole_fk e conservante_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do ConservantePicole deve ser um inteiro!')
            if not isinstance(conservante_fk, int):
                raise TypeError('conservante_fk do ConservantePicole deve ser um inteiro!')

            conservante_picole = ConservantePicole(picole_fk=picole_fk,
                                                   conservante_fk=conservante_fk,
                                                   conservante_picole=f'{conservante_fk}-{picole_fk}'
                                                   )
            # Verificar se já existe um registro com o nome e a fórmula informados
            session = await createSession()
            async with session.begin():
                print(f'Inserindo ConservantePicole: {conservante_picole}')
                session.add(conservante_picole)
                await session.commit()

                print(f'ConservantePicole inserido com sucesso!')
                print(f'ID do ConservantePicole inserido: {conservante_picole.id}')
                print(f'picole_fk do ConservantePicole inserido: {conservante_picole.picole_fk}')
                print(f'picole.sabor do ConservantePicole inserido: {conservante_picole.picole.sabor}')
                print(f'conservante_fk do ConservantePicole inserido: {conservante_picole.conservante_fk}')
                print(f'conservante.nome do ConservantePicole inserido: {conservante_picole.conservante.nome}')
            return conservante_picole

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir ConservantePicole. "
                                   f"Verifique se as FKs fornecidas existem: "
                                   f"{picole_fk=} | {conservante_fk=}"
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""
                Erro de integridade ao inserir ConservantePicole. 
                Já existe um ConservantePicole com a mesma combinação de picole_fk e conservante_fk: {picole_fk=} | {conservante_fk=}
                """)
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Conservante: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

        finally:
            if session:
                await session.close()

    @staticmethod
    def selectAllConservantePicole():
        """Seleciona todos os registros da tabela conservante_picole
            :raises Exception: Informando erro inesperado ao selecionar os ConservantePicole
            :return: List[ConservantePicole]: Retorna uma lista de objetos ConservantePicole
        """
        try:
            with createSession() as session:
                conservante_picole = session.query(ConservantePicole).all()
                return conservante_picole

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar ConservantePicole: {exc}')

    @staticmethod
    def selectConservantePicolePorId(id: int) -> 'ConservantePicole' or None:
        """Seleciona um registro da tabela conservante_picole por ID
        :param id: int: id do ConservantePicole
        :return: ConservantePicole or None: Retorna o objeto ConservantePicole se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar o ConservantePicole
        :return: ConservantePicole or None: Retorna o objeto ConservantePicole se encontrado, None caso contrário
        """

        try:
            # check if is int
            if not isinstance(id, int):
                raise TypeError('O id do ConservantePicole deve ser um inteiro!')
            if not id:
                raise ValueError('O id do ConservantePicole deve ser informado!')

            with createSession() as session:
                conservante_picole = session.query(ConservantePicole).filter(ConservantePicole.id == id).first()
                return conservante_picole

        except Exception as exc:
            raise RuntimeError(f'Erro ao selecionar ConservantePicole por ID: {exc}')

    @staticmethod
    def selectAllConservantePicolePorPicole(picole_fk: int) -> list['ConservantePicole'] or []:
        """Seleciona todos os registros da tabela conservante_picole por picole_fk
        :param picole_fk: int: id do picolé
        :raises TypeError: Se o picole_fk não for um inteiro
        :raises ValueError: Se o picole_fk não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar os ConservantePicole
        :return: List[ConservantePicole] or []: Retorna uma lista de objetos ConservantePicole se encontrado, [] caso contrário
        """
        try:
            # check if is int
            if not isinstance(picole_fk, int):
                raise TypeError('O picole_fk do ConservantePicole deve ser um inteiro!')
            if not picole_fk:
                raise ValueError('O picole_fk do ConservantePicole deve ser informado!')

            with createSession() as session:
                conservante_picole = session.query(ConservantePicole).filter(
                    ConservantePicole.picole_fk == picole_fk).all()
                return conservante_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao selecionar todos ConservantePicole por picole_fk: {exc}')

    @staticmethod
    def selectAllConservantePicolePorConservante(conservante_fk: int) -> list['ConservantePicole'] or []:
        """Seleciona todos os registros da tabela conservante_picole por conservante_fk
        :param conservante_fk: int: id do conservante
        :raises TypeError: Se o conservante_fk não for um inteiro
        :raises ValueError: Se o conservante_fk não for informado
        :raises RuntimeError: Se ocorrer um erro ao selecionar os ConservantePicole
        :return: List[ConservantePicole] or []: Retorna uma lista de objetos ConservantePicole se encontrado, [] caso contrário
        """
        try:
            # check if is int
            if not isinstance(conservante_fk, int):
                raise TypeError('O conservante_fk do ConservantePicole deve ser um inteiro!')
            if not conservante_fk:
                raise ValueError('O conservante_fk do ConservantePicole deve ser informado!')

            with createSession() as session:
                conservante_picole = session.query(ConservantePicole).filter(
                    ConservantePicole.conservante_fk == conservante_fk).all()
                return conservante_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao selecionar todos ConservantePicole por conservante_fk: {exc}')

    @staticmethod
    def updateConservantePicole(id_cons_picole: int,
                                picole_fk: Union[int, None],
                                conservante_fk: Union[int, None]) -> 'ConservantePicole':
        """Atualiza um ConservantePicole na tabela conservante_picole
        :param id_cons_picole: int: id do ConservantePicole
        :param picole_fk: int: id do picolé
        :param conservante_fk: int: id do conservante
        :return: ConservantePicole: Retorna o objeto ConservantePicole atualizado
        :raises TypeError: Se o id_cons_picole, picole_fk ou o conservante_fk não forem inteiros
        :raises RuntimeError: Se as FKs picole_fk e conservante_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
           """
        try:
            if not isinstance(id_cons_picole, int):
                raise TypeError('id_cons_picole do ConservantePicole deve ser um inteiro!')

            if not isinstance(picole_fk, int) and picole_fk is not None:
                raise TypeError('picole_fk do ConservantePicole deve ser um inteiro ou não deve ser informado!')

            if not isinstance(conservante_fk, int) and conservante_fk is not None:
                raise TypeError('conservante_fk do ConservantePicole deve ser um inteiro ou não deve ser informado!')

            with createSession() as session:
                conservante_picole = session.query(ConservantePicole). \
                    filter_by(id=id_cons_picole).first()

                if not conservante_picole:
                    raise ValueError(f'ConservantePicole com id={id_cons_picole} não encontrado!')


                if picole_fk:
                    conservante_picole.picole_fk = picole_fk
                else:
                    picole_fk = conservante_picole.picole_fk

                if conservante_fk:
                    conservante_picole.conservante_fk = conservante_fk
                else:
                    conservante_fk = conservante_picole.conservante_fk

                conservante_picole.conservante_picole = (f'{conservante_picole.conservante_fk}-'
                                                         f'{conservante_picole.picole_fk}')
                conservante_picole.data_atualizacao = datetime.now()
                session.commit()
                return conservante_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir ConservantePicole. "
                                   f"Verifique se as FKs fornecidas existem: "
                                   f"{picole_fk=} | {conservante_fk=}"
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""
                Erro de integridade ao inserir ConservantePicole. 
                Já existe um ConservantePicole com a mesma combinação de picole_fk e conservante_fk: {picole_fk=} | {conservante_fk=}
                """)
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao atualizar ConservantePicole: {exc}')

    @staticmethod
    def deleteConservantePicoleById(id_cons_picole: int) -> 'ConservantePicole':
        """Deleta um ConservantePicole na tabela conservante_picole
        :param id_cons_picole: int: id do ConservantePicole
        :raises TypeError: Se o id_cons_picole não for um inteiro
        :raises ValueError: Se o ConservantePicole não for encontrado
        :raises RuntimeError: Se ocorrer um erro ao deletar o ConservantePicole
        """

        try:
            if not isinstance(id_cons_picole, int):
                raise TypeError('id_cons_picole do ConservantePicole deve ser um inteiro!')

            with createSession() as session:
                conservante_picole = session.query(ConservantePicole).filter_by(
                    id=id_cons_picole).first()
                if not conservante_picole:
                    raise ValueError(f'ConservantePicole com id={id_cons_picole} não encontrado!')

                session.delete(conservante_picole)
                session.commit()
                return conservante_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao deletar ConservantePicole: {exc}')


if __name__ == '__main__':
    # try:
    #     ConservantePicole.insertConservantePicole(picole_fk=1, conservante_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir ConservantePicole: {e}')
    #
    # try:
    #     ConservantePicole.insertConservantePicole(picole_fk=1, conservante_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir ConservantePicole: {e}')
    #
    # try:
    #     ConservantePicole.insertConservantePicole(picole_fk=1, conservante_fk=2)
    # except Exception as e:
    #     print(f'Erro ao inserir ConservantePicole: {e}')
    #
    # try:
    #     ConservantePicole.insertConservantePicole(picole_fk=100, conservante_fk=100)
    # except Exception as e:
    #     print(f'Erro ao inserir ConservantePicole: {e}')

    # conser_picole = ConservantePicole.updateConservantePicole(id_cons_picole=1999,
    #                                                           picole_fk=1999,
    #                                                           conservante_fk=3
    #                                                           )
    # print(conser_picole)

    try:
        conser_picole = ConservantePicole.deleteConservantePicoleById(id_cons_picole='9')
        print(conser_picole)
    except Exception as e:
        print(f'Erro ao deletar ConservantePicole: {e}')

