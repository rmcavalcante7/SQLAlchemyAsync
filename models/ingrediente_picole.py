import asyncio
from typing import Union

import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.picole import Picole
from models.ingrediente import Ingrediente
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class IngredientePicole(ModelBase):
    __tablename__ = 'ingrediente_picole'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True,
                        autoincrement=True)

    picole_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                               sa.ForeignKey('picole.id'),
                               nullable=False
                               )
    picole: Picole = orm.relationship('Picole', lazy='joined')

    ingrediente_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                    sa.ForeignKey('ingrediente.id'),
                                    nullable=False
                                    )
    ingrediente: Ingrediente = orm.relationship('Ingrediente', lazy='joined')

    # chave forte para impedir duplicidade
    ingrediente_picole: str = sa.Column(sa.String(200),
                                        unique=True,
                                        nullable=False)

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        return (f'IngredientePicole(id={self.id}, '
                f'picole_fk={self.picole_fk}, '
                f'ingrediente_fk={self.ingrediente_fk}), '
                )

    @staticmethod
    async def insertIngredientePicole(picole_fk: int, ingrediente_fk: int) -> 'IngredientePicole' or None:
        """Insere um IngredientePicole na tabela ingrediente_picole
        :param picole_fk: int: id do picolé
        :param ingrediente_fk: int: id do IngredientePicole
        :return: IngredientePicole or None: Retorna o objeto IngredientePicole se inserido com sucesso, None caso contrário
        :raises TypeError: Se o picole_fk ou o ingrediente_fk não forem inteiros
        :raises RuntimeError: Se as FKs picole_fk e ingrediente_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do IngredientePicole deve ser um inteiro!')
            if not isinstance(ingrediente_fk, int):
                raise TypeError('ingrediente_fk do IngredientePicole deve ser um inteiro!')

            ingrediente_picole = IngredientePicole(picole_fk=picole_fk,
                                                   ingrediente_fk=ingrediente_fk,
                                                   ingrediente_picole=f'{ingrediente_fk}-{picole_fk}'
                                                   )
            # Verificar se já existe um registro com o nome e a fórmula informados
            session = await createSession()
            async with session.begin():
                print(f'Inserindo IngredientePicole: {ingrediente_picole}')
                session.add(ingrediente_picole)
                await session.commit()

                print(f'IngredientePicole inserido com sucesso!')
                print(f'ID do IngredientePicole inserido: {ingrediente_picole.id}')
                print(f'picole_fk do IngredientePicole inserido: {ingrediente_picole.picole_fk}')
                print(f'picole.sabor do IngredientePicole inserido: {ingrediente_picole.picole.sabor}')
                print(f'ingrediente_fk do IngredientePicole inserido: {ingrediente_picole.ingrediente_fk}')
                print(f'ingrediente_fk.nome do IngredientePicole inserido: {ingrediente_picole.ingrediente.nome}')
            return ingrediente_picole

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir IngredientePicole. "
                                   f"Verifique se as FKs fornecidas existem: "
                                   f"{picole_fk=} | {ingrediente_fk=}"
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir IngredientePicole. 
                Já existe um IngredientePicole com a mesma combinação de picole_fk e ingrediente_fk: {picole_fk=} | {ingrediente_fk=}
                """)
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

        finally:
            if session:
                await session.close()

    @staticmethod
    def selectIngredientePicolePorId(id: int) -> 'IngredientePicole' or None:
        """Seleciona um IngredientePicole na tabela ingrediente_picole
        :param id: int: id do ingrediente_picole
        :return: IngredientePicole or None: Retorna o objeto IngredientePicole se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises RuntimeError: Se ocorrer um erro genérico ao buscar o IngredientePicole
        """

        try:
            # check if is string
            if not isinstance(id, int):
                raise TypeError('id do IngredientePicole deve ser um inteiro!')

            with createSession() as session:
                ingrediente_picole = session.query(IngredientePicole).filter(IngredientePicole.id == id).first()
                if ingrediente_picole:
                    return ingrediente_picole

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectAllIngredientePicole() -> list['IngredientePicole'] or []:
        """Seleciona todos os IngredientesPicole na tabela ingrediente_picole
        :raises Exception: Informando erro inesperado ao selecionar os ingredientes_picole
        :return: list[IngredientePicole] or []: Retorna uma lista de objetos IngredientePicole se encontrado, [] caso contrário
        """
        try:
            with createSession() as session:
                ingredientes_picole = session.query(IngredientePicole).all()
                return ingredientes_picole

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos IngredientePicole: {exc}')

    @staticmethod
    def selectAllIngPicPorPicoleFK(picole_fk: int) -> list['IngredientePicole'] or []:
        """Seleciona todos os IngredientesPicole na tabela ingrediente_picole por picole_fk
        :param picole_fk: int: id do picolé
        :return: list or []: Retorna uma lista de objetos IngredientePicole se encontrado, [] caso contrário
        :raises TypeError: Se o picole_fk não for um inteiro
        :raises RuntimeError: Se ocorrer um erro genérico ao buscar o IngredientePicole
        """

        try:
            # check if is string
            if not isinstance(picole_fk, int):
                raise TypeError('picole_fk do IngredientePicole deve ser um inteiro!')

            with createSession() as session:
                ingredientes_picole = session.query(IngredientePicole).filter(
                    IngredientePicole.picole_fk == picole_fk).all()
                return ingredientes_picole

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos IngredientePicole: {exc}')

    @staticmethod
    def selectAllIngPicPorIngredienteFK(ingrediente_fk: int) -> list['IngredientePicole'] or []:
        """Seleciona todos os IngredientesPicole na tabela ingrediente_picole por ingrediente_fk
        :param ingrediente_fk: int: id do ingrediente
        :return: list or []: Retorna uma lista de objetos IngredientePicole se encontrado, [] caso contrário
        :raises TypeError: Se o ingrediente_fk não for um inteiro
        :raises RuntimeError: Se ocorrer um erro genérico ao buscar o IngredientePicole
        """

        try:
            # check if is string
            if not isinstance(ingrediente_fk, int):
                raise TypeError('ingrediente_fk do IngredientePicole deve ser um inteiro!')

            with createSession() as session:
                ingredientes_picole = session.query(IngredientePicole).filter(
                    IngredientePicole.ingrediente_fk == ingrediente_fk).all()
                return ingredientes_picole

        except TypeError as te:
            raise TypeError(te)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos IngredientePicole: {exc}')

    @staticmethod
    def updateIngredientePicole(id_ing_picole: int,
                                picole_fk: Union[int, None],
                                ingrediente_fk: Union[int, None]) -> 'IngredientePicole':
        """Atualiza um IngredientePicole na tabela ingrediente_picole
        :param id_ing_picole: int: id do IngredientePicole
        :param picole_fk: int: id do picolé
        :param ingrediente_fk: int: id do ingrediente
        :return: IngredientePicole: Retorna o objeto IngredientePicole atualizado
        :raises TypeError: Se o id_ing_picole, picole_fk ou o ingrediente_fk não forem inteiros
        :raises ValueError: Se o id_ing_picole, picole_fk ou o ingrediente_fk não forem informados
        :raises RuntimeError: se as FKs picole_fk e ingrediente_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        try:
            if not isinstance(id_ing_picole, int):
                raise TypeError('id_ing_picole do IngredientePicole deve ser um inteiro!')

            if not isinstance(picole_fk, int) and picole_fk is not None:
                raise TypeError('picole_fk do IngredientePicole deve ser um inteiro ou não deve ser informado!')

            if not isinstance(ingrediente_fk, int) and ingrediente_fk is not None:
                raise TypeError('ingrediente_fk do IngredientePicole deve ser um inteiro ou não deve ser informado!')

            with createSession() as session:
                ingrediente_picole = session.query(IngredientePicole). \
                    filter_by(id=id_ing_picole).first()

                if not ingrediente_picole:
                    raise ValueError(f'IngredientePicole com id={id_ing_picole} não encontrado!')

                if picole_fk:
                    ingrediente_picole.picole_fk = picole_fk
                else:
                    picole_fk = ingrediente_picole.picole_fk

                if ingrediente_fk:
                    ingrediente_picole.ingrediente_fk = ingrediente_fk
                else:
                    ingrediente_fk = ingrediente_picole.ingrediente_fk

                ingrediente_picole.ingrediente_picole = (f'{ingrediente_picole.ingrediente_fk}-'
                                                         f'{ingrediente_picole.picole_fk}')
                ingrediente_picole.data_atualizacao = datetime.now()
                session.commit()
                return ingrediente_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"Erro de integridade ao inserir IngredientePicole. "
                                   f"Verifique se as FKs fornecidas existem: "
                                   f"{picole_fk=} | {ingrediente_fk=}"
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir IngredientePicole. 
                Já existe um IngredientePicole com a mesma combinação de picole_fk e ingrediente_fk: {picole_fk=} | {ingrediente_fk=}
                """)
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Lote: {intg_error}')

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao atualizar IngredientePicole: {exc}')

    @staticmethod
    def deleteIngredientePicoleById(id_ingr_picole: int) -> 'IngredientePicole':
        """Deleta um IngredientePicole na tabela ingrediente_picole
        :param id_ingr_picole: int: id do IngredientePicole
        :raises TypeError: Se o id_ingr_picole não for um inteiro
        :raises ValueError: Se o IngredientePicole não for encontrado
        :raises RuntimeError: Se ocorrer um erro ao deletar o IngredientePicole
        """

        try:
            if not isinstance(id_ingr_picole, int):
                raise TypeError('id_ingr_picole do IngredientePicole deve ser um inteiro!')

            with createSession() as session:
                ingrediente_picole = session.query(IngredientePicole).filter_by(
                    id=id_ingr_picole).first()
                if not ingrediente_picole:
                    raise ValueError(f'IngredientePicole com id={id_ingr_picole} não encontrado!')

                session.delete(ingrediente_picole)
                session.commit()
                return ingrediente_picole

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao deletar IngredientePicole: {exc}')


if __name__ == '__main__':
    # try:
    #     IngredientePicole.insertIngredientePicole(picole_fk=1, ingrediente_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir IngredientePicole: {e}')
    #
    # try:
    #     IngredientePicole.insertIngredientePicole(picole_fk=1, ingrediente_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir IngredientePicole: {e}')
    #
    # try:
    #     IngredientePicole.insertIngredientePicole(picole_fk=1, ingrediente_fk=2)
    # except Exception as e:
    #     print(f'Erro ao inserir IngredientePicole: {e}')
    #
    # try:
    #     IngredientePicole.insertIngredientePicole(picole_fk=100, ingrediente_fk=100)
    # except Exception as e:
    #     print(f'Erro ao inserir IngredientePicole: {e}')

    # ingredientes_picole = IngredientePicole.updateIngredientePicole(id_ing_picole=1234,
    #                                                                 picole_fk='None',
    #                                                                 ingrediente_fk=3)
    # print(ingredientes_picole)

    try:
        ingredientes_picole = IngredientePicole.deleteIngredientePicoleById(id_ingr_picole='1')
        print(ingredientes_picole)
    except Exception as e:
        print(f'Erro ao deletar IngredientePicole: {e}')