import asyncio
from typing import Union

import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.lote import Lote
from models.nota_fiscal import NotaFiscal
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError


class LoteNotaFiscal(ModelBase):
    __tablename__ = 'lote_nota_fiscal'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True,
                        autoincrement=True)

    nota_fiscal_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                    sa.ForeignKey('nota_fiscal.id'),
                                    nullable=False
                                    )
    nota_fiscal: NotaFiscal = orm.relationship('NotaFiscal', lazy='joined')

    lote_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                             sa.ForeignKey('lote.id'),
                             unique=True,  # um lote só pode estar vinculado a uma nota fiscal
                             nullable=False)
    lote: Lote = orm.relationship('Lote', lazy='joined')

    # chave forte para imedir se ser inserido o mesmo par de lote e nota fiscal
    lote_nota_fiscal: str = sa.Column(sa.String(200),
                                      unique=True,
                                      nullable=False)

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        return f'LoteNotaFiscal(id={self.id}, lote_fk={self.lote_fk}, nota_fiscal_fk={self.nota_fiscal_fk})'

    @staticmethod
    async def insertLoteNotaFiscal(nota_fiscal_fk: int, lote_fk: int) -> 'LoteNotaFiscal' or None:
        """Insere um LoteNotaFiscal na tabela lote_nota_fiscal
        :param nota_fiscal_fk: int: id da nota fiscal
        :param lote_fk: int: id do lote
        :return: LoteNotaFiscal or None: Retorna o objeto LoteNotaFiscal se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome ou a fórmula química não forem strings
        :raises ValueError: Se o nome ou a fórmula química não forem informados
        :raises RuntimeError: Se as FKs nota_fiscal_fk e lote_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(nota_fiscal_fk, int):
                raise TypeError('nota_fiscal_fk do LoteNotaFiscal deve ser um inteiro!')
            if not isinstance(lote_fk, int):
                raise TypeError('lote_fk do LoteNotaFiscal deve ser um inteiro!')

            lote_nota_fiscal = LoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk,
                                              lote_fk=lote_fk,
                                              lote_nota_fiscal=f'{lote_fk}-{nota_fiscal_fk}'
                                              )
            # Verificar se já existe um registro com o nome e a fórmula informados
            session = await createSession()
            async with session.begin():
                print(f'Inserindo LoteNotaFiscal: {lote_nota_fiscal}')
                session.add(lote_nota_fiscal)
                await session.commit()

                print(f'Lote Nota Fiscal inserido com sucesso!')
                print(f'ID do LoteNotaFiscal inserido: {lote_nota_fiscal.id}')
                print(f'nota_fiscal_fk do LoteNotaFiscal inserido: {lote_nota_fiscal.nota_fiscal_fk}')
                print(
                    f'nota_fiscal.numero_serie LoteNotaFiscal inserido: {str(lote_nota_fiscal.nota_fiscal.numero_serie)}')
                print(f'lote_fk do LoteNotaFiscal inserido: {lote_nota_fiscal.lote_fk}')
                print(f'lote.quantidade do LoteNotaFiscal inserido: {lote_nota_fiscal.lote.quantidade}')
            return lote_nota_fiscal

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                Verifique se as FKs fornecidas existem: {nota_fiscal_fk=} | {lote_fk=}"""
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                Já existe um LoteNotaFiscal com a mesma combinação de lote e nota fiscal: {nota_fiscal_fk=} | {lote_fk=}"""
                                   )

            else:
                raise RuntimeError(f'Erro de integridade ao inserir LoteNotaFiscal: {intg_error}')

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
    def selectAllLoteNotaFiscal() -> list['LoteNotaFiscal'] or []:
        """Seleciona todos os registros da tabela lote_nota_fiscal
        :raises Exception: Informando erro inesperado ao selecionar os LoteNotaFiscal
        :return: list[LoteNotaFiscal] or []: Retorna uma lista de objetos LoteNotaFiscal se houver registros, [] caso contrário
        """
        try:
            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal).all()
                return lote_nota_fiscal
        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos LoteNotaFiscal: {exc}')

    @staticmethod
    def selectLoteNotaFiscalPorId(id: int) -> 'LoteNotaFiscal' or None:
        """Seleciona um registro da tabela lote_nota_fiscal por ID
        :param id: int: id do LoteNotaFiscal
        :raise TypeError: Se o id não for um inteiro
        :raise ValueError: Se o id não for informado
        :return: LoteNotaFiscal or None: Retorna o objeto LoteNotaFiscal se encontrado, None caso contrário
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do LoteNotaFiscal deve ser um inteiro!')
            if not id:
                raise ValueError('id do LoteNotaFiscal não foi informado!')

            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal).filter(LoteNotaFiscal.id == id).first()
                return lote_nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar LoteNotaFiscal por ID: {exc}')

    @staticmethod
    def selectAllLoteNotaFiscalPorNotaFiscal(nota_fiscal_fk: int) -> list['LoteNotaFiscal'] or []:
        """Seleciona todos os registros da tabela lote_nota_fiscal por nota_fiscal_fk
        :param nota_fiscal_fk: int: id da nota fiscal
        :raise TypeError: Se o nota_fiscal_fk não for um inteiro
        :raise ValueError: Se o nota_fiscal_fk não for informado
        :return: list[LoteNotaFiscal] or []: Retorna uma lista de objetos LoteNotaFiscal se houver registros, [] caso contrário
        """
        try:
            if not isinstance(nota_fiscal_fk, int):
                raise TypeError('nota_fiscal_fk do LoteNotaFiscal deve ser um inteiro!')
            if not nota_fiscal_fk:
                raise ValueError('nota_fiscal_fk do LoteNotaFiscal não foi informado!')

            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal).filter(
                    LoteNotaFiscal.nota_fiscal_fk == nota_fiscal_fk).all()
                return lote_nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar LoteNotaFiscal por nota_fiscal_fk: {exc}')

    @staticmethod
    def selectLoteNotaFiscalPorLote(lote_fk) -> 'LoteNotaFiscal' or None:
        """Seleciona um registro da tabela lote_nota_fiscal por lote_fk
        :param lote_fk: int: id do lote
        :raise TypeError: Se o lote_fk não for um inteiro
        :raise ValueError: Se o lote_fk não for informado
        :return: LoteNotaFiscal or None: Retorna o objeto LoteNotaFiscal se encontrado, None caso contrário
        """
        try:
            if not isinstance(lote_fk, int):
                raise TypeError('lote_fk do LoteNotaFiscal deve ser um inteiro!')
            if not lote_fk:
                raise ValueError('lote_fk do LoteNotaFiscal não foi informado!')

            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal).filter(LoteNotaFiscal.lote_fk == lote_fk).first()
                return lote_nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar LoteNotaFiscal por lote_fk: {exc}')

    @staticmethod
    def updateLoteNotaFiscal(id_lote_nf: int,
                             lote_fk: Union[int, None],
                             nota_fiscal_fk: Union[int, None]) -> 'LoteNotaFiscal':
        """Atualiza um LoteNotaFiscal na tabela lote_nota_fiscal
        :param id_lote_nf: int: id do LoteNotaFiscal
        :param lote_fk: int: id do lote
        :param nota_fiscal_fk: int: id da nota fiscal
        :return: LoteNotaFiscal: Retorna o objeto LoteNotaFiscal atualizado
        :raises TypeError: Se o id_lote_nf, lote_fk ou o nota_fiscal_fk não forem inteiros
        :raises ValueError: Se o id_lote_nf, lote_fk ou o nota_fiscal_fk não forem informados
        :raises RuntimeError: se as FKs lote_fk e nota_fiscal_fk não existirem retorna um erro de integridade, caso
        contrário, retorna um erro genérico.
        """

        try:
            if not isinstance(id_lote_nf, int):
                raise TypeError('id_lote_nf do LoteNotaFiscal deve ser um inteiro!')

            if not isinstance(lote_fk, int) and lote_fk is not None:
                raise TypeError('lote_fk do LoteNotaFiscal deve ser um inteiro ou não deve ser informado!')

            if not isinstance(nota_fiscal_fk, int) and nota_fiscal_fk is not None:
                raise TypeError(
                    'nota_fiscal_fk do LoteNotaFiscal deve ser um inteiro ou não deve ser informado!')

            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal). \
                    filter_by(id=id_lote_nf).first()

                if not lote_nota_fiscal:
                    raise ValueError(f'LoteNotaFiscal com id={id_lote_nf} não encontrado!')

                if lote_fk:
                    lote_nota_fiscal.lote_fk = lote_fk
                else:
                    lote_fk = lote_nota_fiscal.lote_fk

                if nota_fiscal_fk:
                    lote_nota_fiscal.nota_fiscal_fk = nota_fiscal_fk
                else:
                    nota_fiscal_fk = lote_nota_fiscal.nota_fiscal_fk

                lote_nota_fiscal.lote_nota_fiscal = f'{lote_fk}-{nota_fiscal_fk}'
                lote_nota_fiscal.data_atualizacao = datetime.now()
                session.commit()
                return lote_nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                Verifique se as FKs fornecidas existem: {nota_fiscal_fk=} | {lote_fk=}"""
                                   )
            elif 'UNIQUE constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                Já existe um LoteNotaFiscal com a mesma combinação de lote e nota fiscal: {nota_fiscal_fk=} | {lote_fk=}"""
                                   )

            else:
                raise RuntimeError(f'Erro de integridade ao inserir LoteNotaFiscal: {intg_error}')

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao atualizar LoteNotaFiscal: {exc}')

    @staticmethod
    def deleteLoteNotaFiscalById(id_lote_nf: int) -> 'LoteNotaFiscal':
        """Deleta um LoteNotaFiscal na tabela lote_nota_fiscal
        :param id_lote_nf: int: id do LoteNotaFiscal
        :raises TypeError: Se o id_lote_nf não for um inteiro
        :raises ValueError: Se o LoteNotaFiscal não for encontrado
        :raises RuntimeError: Se ocorrer um erro ao deletar o LoteNotaFiscal
        """

        try:
            if not isinstance(id_lote_nf, int):
                raise TypeError('id_lote_nf do LoteNotaFiscal deve ser um inteiro!')

            with createSession() as session:
                lote_nota_fiscal = session.query(LoteNotaFiscal).filter_by(
                    id=id_lote_nf).first()
                if not lote_nota_fiscal:
                    raise ValueError(f'LoteNotaFiscal com id={id_lote_nf} não encontrado!')

                session.delete(lote_nota_fiscal)
                session.commit()
                return lote_nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            raise RuntimeError(f'Erro inesperado ao deletar LoteNotaFiscal: {exc}')



if __name__ == '__main__':
    # try:
    #     LoteNotaFiscal.insertLoteNotaFiscal(nota_fiscal_fk=1, lote_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir LoteNotaFiscal: {e}')
    #
    # try:
    #     LoteNotaFiscal.insertLoteNotaFiscal(nota_fiscal_fk=1, lote_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir LoteNotaFiscal: {e}')
    #
    # try:
    #     LoteNotaFiscal.insertLoteNotaFiscal(nota_fiscal_fk=1, lote_fk=2)
    # except Exception as e:
    #     print(f'Erro ao inserir LoteNotaFiscal: {e}')

    try:
        lote_nf = LoteNotaFiscal.deleteLoteNotaFiscalById(id_lote_nf=2)
        print(f'deletado:\n{lote_nf}')
    except Exception as e:
        print(f'Erro ao deletar LoteNotaFiscal: {e}')
