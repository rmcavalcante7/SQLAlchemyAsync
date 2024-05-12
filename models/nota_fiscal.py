import asyncio
import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from models.model_base import ModelBase
from models.revendedor import Revendedor
from typing import List, Union
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures



class NotaFiscal(ModelBase):
    __tablename__ = 'nota_fiscal'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    valor: float = sa.Column(sa.DECIMAL(decimal_return_scale=2).with_variant(sa.Float(), "sqlite"),
                             nullable=False)

    numero_serie: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(200), nullable=False)

    revendedor_fk: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),
                                   sa.ForeignKey('revendedor.id'), nullable=False)
    revendedor: Revendedor = orm.relationship('Revendedor', lazy='joined')

    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)


    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return (f'<Nota Fiscal (numero_serie={self.numero_serie}, valor={self.valor},'
                f'descricao={self.descricao})>')



    @staticmethod
    async def insertNotaFiscal(valor: float, numero_serie: str, descricao: str, revendedor_fk: int) -> 'NotaFiscal' or None:
        """Insere uma NotaFiscal na tabela nota_fiscal
        :param valor: float: valor da nota fiscal, duas casas decimais
        :param numero_serie: str: número de série da nota fiscal
        :param descricao: str: descrição da nota fiscal
        :param revendedor_fk: int: id do revendedor
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se inserido com sucesso, None caso contrário
        :raises TypeError: Se o valor não for um float, ou se o número de série ou a descrição não forem strings
        :raises ValueError: Se o valor, o número de série ou a descrição não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir a nota fiscal, especificado para o número de série
        ou para o revendedor, caso já existam registros com esses valores. Caso seja por outr motivo, será lançado
        um erro genérico.
        """

        session = None
        try:
            # check if is string
            if not isinstance(valor, float) and not isinstance(valor, int):
                raise TypeError('valor da NotaFiscal deve ser um número!')
            if not isinstance(numero_serie, str):
                raise TypeError('numero_serie da NotaFiscal deve ser uma string!')
            if not isinstance(descricao, str):
                raise TypeError('descricao da NotaFiscal deve ser uma string!')
            if not isinstance(revendedor_fk, int):
                raise TypeError('revendedor_fk da NotaFiscal deve ser um inteiro!')

            numero_serie = numero_serie.strip().upper()
            descricao = descricao.strip().upper()
            valor = round(float(valor), 2)

            if not numero_serie:
                raise ValueError('numero_serie da NotaFiscal não informado!')
            if not descricao:
                raise ValueError('descricao da NotaFiscal não informada!')


            nota_fiscal = NotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao,
                                     revendedor_fk=revendedor_fk)

            # Verificar se já existe um registro com o nome e a fórmula informados
            session = await createSession()
            async with session.begin():
                print(f'Inserindo NotaFiscal: {nota_fiscal}')
                session.add(nota_fiscal)
                await session.commit()

                print(f'Nota fiscal inserida com sucesso!')
                print(f'ID da NotaFiscal inserida: {nota_fiscal.id}')
                print(f'valor da NotaFiscal inserida: {nota_fiscal.valor}')
                print(f'numero_serie da NotaFiscal inserida: {nota_fiscal.numero_serie}')
                print(f'descricao da NotaFiscal inserida: {nota_fiscal.descricao}')
                print(f'revendedor_fk da NotaFiscal inserida: {nota_fiscal.revendedor_fk}')
                print(f'revendedor.nome da NotaFiscal inserida: {nota_fiscal.revendedor.nome}')
                return nota_fiscal
        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'nota_fiscal.numero_serie' in str(intg_error):
                    raise RuntimeError(f"Já existe uma Nota Fiscal com o número de série '{numero_serie}' cadastrado. "
                                       f"O número de série deve ser único.")
            elif 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                                        Verifique se a FK fornecida existe: {revendedor_fk=}"""
                                   )
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Nota Fiscal: {intg_error}')

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
    def selectAllNotasFiscal() -> List['NotaFiscal'] or []:
        """Seleciona todas as Notas Fiscais na tabela nota_fiscal
        :return: List[NotaFiscal] or []: Retorna uma lista de objetos NotaFiscal se encontrados, [] caso contrário
        :raises Exception: Se ocorrer um erro inesperado ao selecionar Notas Fiscais
        """
        try:
            with createSession() as session:
                notas_fiscais = session.query(NotaFiscal).all()
                return notas_fiscais

        except Exception as e:
            raise Exception(f'Erro inesperado ao selecionar todas NotaFiscal: {e}')

    @staticmethod
    def selectNotaFiscalPorId(id: int) -> 'NotaFiscal' or None:
        """Seleciona uma Nota Fiscal na tabela nota_fiscal por id
        :param id: int: id da Nota Fiscal
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
        """
        try:
            # check if is integer
            if not isinstance(id, int):
                raise TypeError('id da Nota Fiscal deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not id:
                raise ValueError('id da Nota Fiscal não informado!')

            with createSession() as session:
                nota_fiscal = session.query(NotaFiscal).filter(NotaFiscal.id == id).one_or_none()
                return nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectNotaFiscalPorNumeroSerie(numero_serie: str) -> 'NotaFiscal' or None:
        """Seleciona uma Nota Fiscal na tabela nota_fiscal por número de série
        :param numero_serie: str: número de série da Nota Fiscal
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
        :raises TypeError: Se o número de série não for uma string
        :raises ValueError: Se o número de série não for informado
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se encontrado, None caso contrário
        """
        try:
            # check if is string
            if not isinstance(numero_serie, str):
                raise TypeError('numero_serie da Nota Fiscal deve ser uma string!')

            # validar se os parâmetros informados são válidos
            numero_series = numero_serie.strip().upper()
            if not numero_serie:
                raise ValueError('numero_serie da Nota Fiscal não informado!')

            with createSession() as session:
                nota_fiscal = session.query(NotaFiscal).filter(NotaFiscal.numero_serie == numero_serie).one_or_none()
                return nota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectNotasFiscaisPorRevendedorFk(revendedor_fk: int) -> List['NotaFiscal'] or []:
        """Seleciona Notas Fiscais na tabela nota_fiscal por revendedor_fk
        :param revendedor_fk: int: id do revendedor
        :return: List[NotaFiscal] or None: Retorna uma lista de objetos NotaFiscal se encontrado, None caso contrário
        :raises TypeError: Se o revendedor_fk não for um inteiro
        :raises ValueError: Se o revendedor_fk não for informado
        :return: List[NotaFiscal] or None: Retorna uma lista de objetos NotaFiscal se encontrado, None caso contrário
        """
        try:
            # check if is integer
            if not isinstance(revendedor_fk, int):
                raise TypeError('revendedor_fk da Nota Fiscal deve ser um inteiro!')

            # validar se os parâmetros informados são válidos
            if not revendedor_fk:
                raise ValueError('revendedor_fk da Nota Fiscal não informado!')

            with createSession() as session:
                notas_fiscais = session.query(NotaFiscal).filter(NotaFiscal.revendedor_fk == revendedor_fk).all()
                return notas_fiscais

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')


    @staticmethod
    def updateNotaFiscal(id_nf: int, valor: Union[float, None], revendedor_fk: Union[int, None],
                         numero_serie: str = '', descricao: str = '') -> 'NotaFiscal':
        """Atualiza uma NotaFiscal na tabela nota_fiscal
        :param id: int: id da NotaFiscal
        :param valor: float: valor da nota fiscal, duas casas decimais
        :param numero_serie: str: número de série da nota fiscal
        :param descricao: str: descrição da nota fiscal
        :param revendedor_fk: int: id do revendedor
        :return: NotaFiscal or None: Retorna o objeto NotaFiscal se atualizado com sucesso, None caso contrário
        :raises TypeError: Se o id não for um inteiro, ou se o valor não for um float, ou se o número de série ou a descrição não forem strings
        :raises ValueError: Se o id, o valor, o número de série ou a descrição não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar a nota fiscal, especificado para o número de série
        ou para o revendedor, caso já existam registros com esses valores. Caso seja por outr motivo, será lançado
        um erro genérico.
        """
        try:
            # check if is integer
            if not isinstance(id_nf, int):
                raise TypeError('id_nf da Nota Fiscal deve ser um inteiro!')
            if not isinstance(valor, float) and not isinstance(valor, int):
                raise TypeError('valor da NotaFiscal deve ser um número ou não deve informado!')
            if not isinstance(numero_serie, str):
                raise TypeError('numero_serie da NotaFiscal deve ser uma string!')
            if not isinstance(descricao, str):
                raise TypeError('descricao da NotaFiscal deve ser uma string!')
            if not isinstance(revendedor_fk, int):
                raise TypeError('revendedor_fk da NotaFiscal deve ser um inteiro ou não deve informado!')

            if len(numero_serie) > 0 and all(caractere.isspace() for caractere in numero_serie):
                raise ValueError('numero_serie da NotaFiscal não pode ser composto só por espaços!')

            if len(descricao) > 0 and all(caractere.isspace() for caractere in descricao):
                raise ValueError('descricao da NotaFiscal não pode ser composto só por espaços!')

            numero_serie = numero_serie.strip().upper()
            descricao = descricao.strip().upper()
            valor = round(float(valor), 2) if valor else None

            with createSession() as session:
                nota_fiscal = session.query(NotaFiscal).filter_by(id=id_nf).first()

                if not nota_fiscal:
                    raise ValueError(f'Nota Fiscal com id={id_nf} não cadastrada na base!')

                if valor:
                    nota_fiscal.valor = valor

                if numero_serie:
                    nota_fiscal.numero_serie = numero_serie
                else:
                    numero_serie = nota_fiscal.numero_serie

                if descricao:
                    nota_fiscal.descricao = descricao

                if revendedor_fk:
                    nota_fiscal.revendedor_fk = revendedor_fk
                else:
                    revendedor_fk = nota_fiscal.revendedor_fk

                session.commit()
                return nota_fiscal

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'nota_fiscal.numero_serie' in str(intg_error):
                    raise RuntimeError(f"Já existe uma Nota Fiscal com o número de série '{numero_serie}' cadastrado. "
                                       f"O número de série deve ser único.")
            elif 'FOREIGN KEY constraint failed' in str(intg_error):
                raise RuntimeError(f"""Erro de integridade ao inserir LoteNotaFiscal. 
                                        Verifique se a FK fornecida existe: {revendedor_fk=}"""
                                   )
            else:
                raise RuntimeError(f'Erro de integridade ao inserir Nota Fiscal: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exp:
            raise Exception(f'Erro inesperado ao atualizar Ingrediente: {exp}')

    @staticmethod
    def deleteNotaFiscalById(id_nota_fiscal: int) -> 'NotaFiscal':
        """Deleta um NotaFiscal cadastrado no banco de dados a partir do id.
        :param id_nota_fiscal: int: identificador do NotaFiscal
        :return: NotaFiscal: Retorna o objeto NotaFiscal deletado
        :raises TypeError: Se o id_nota_fiscal não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o NotaFiscal, especificado para o
        id_nota_fiscal, caso o NotaFiscal esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o NotaFiscal não for encontrado na base
        """
        try:
            if not isinstance(id_nota_fiscal, int):
                raise TypeError('id_nota_fiscal do NotaFiscal deve ser um inteiro!')

            with createSession() as session:
                inota_fiscal: NotaFiscal = session.query(NotaFiscal). \
                    filter_by(id=id_nota_fiscal).first()

                if not inota_fiscal:
                    raise ValueError(f'NotaFiscal com id={id_nota_fiscal} não cadastrado na base!')

                session.delete(inota_fiscal)
                session.commit()
                return inota_fiscal

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=NotaFiscal.__tablename__)
                raise RuntimeError(f'NotaFiscal com id={id_nota_fiscal} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar NotaFiscal: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar NotaFiscal: {exc}')


if __name__ == '__main__':
    # try:
    #     NotaFiscal.insertNotaFiscal(valor=100.00, numero_serie='123456', descricao='Nota fiscal de teste', revendedor_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir Nota Fiscal: {e}')
    #
    # # repetido
    # try:
    #     NotaFiscal.insertNotaFiscal(valor=100.00, numero_serie='123456', descricao='Nota fiscal de teste', revendedor_fk=1)
    # except Exception as e:
    #     print(f'Erro ao inserir Nota Fiscal: {e}')
    #
    # # revendedor_fk não existe
    # try:
    #     NotaFiscal.insertNotaFiscal(valor=100.00, numero_serie='1231457', descricao='Nota fiscal de teste', revendedor_fk=10)
    # except Exception as e:
    #     print(f'Erro ao inserir Nota Fiscal: {e}')

    try:
        nota_fiscal = NotaFiscal.deleteNotaFiscalById(id_nota_fiscal='201')
        print(f'Nota Fiscal deletada: {nota_fiscal}')
    except Exception as e:
        print(f'Erro ao deletar Nota Fiscal: {e}')
