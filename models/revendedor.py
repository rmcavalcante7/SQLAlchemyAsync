import sqlalchemy as sa
from datetime import datetime
from models.model_base import ModelBase
from conf.db_session import createSession
from sqlalchemy.exc import IntegrityError
from ScriptsAuxiliares.DataBaseFeatures import DataBaseFeatures


class Revendedor(ModelBase):
    __tablename__ = 'revendedor'

    id: int = sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"),  # para funcionar o autoincrement no sqlite
                        primary_key=True, autoincrement=True)
    nome: str = sa.Column(sa.String(100), nullable=False)
    cnpj: str = sa.Column(sa.String(14), unique=True, nullable=False)
    razao_social: str = sa.Column(sa.String(100), nullable=False)
    contato: str = sa.Column(sa.String(100), nullable=False)
    data_criacao: datetime = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    data_atualizacao: datetime = sa.Column(sa.DateTime, default=datetime.now,
                                           nullable=False, onupdate=datetime.now)

    def __repr__(self):
        """Retorna uma representação do objeto em forma de 'string'."""
        return f'<Revendedor (nome={self.nome}, cnpj={self.cnpj}, razao_social={self.razao_social})>'

    @staticmethod
    async def insertRevendedor(nome: str, cnpj: str, razao_social: str, contato: str) -> 'Revendedor' or None:
        """Insere um Revendedor na tabela revendedor
        :param nome: str: nome do revendedor
        :param cnpj: str: CNPJ do revendedor
        :param razao_social: str: razão social do revendedor
        :param contato: str: contato do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se inserido com sucesso, None caso contrário
        :raises TypeError: Se o nome, cnpj, razao_social ou contato não forem strings
        :raises ValueError: Se o nome, cnpj, razao_social ou contato não forem informados
        :raises RuntimeError: Se ocorrer um erro de integridade ao inserir o revendedor, especificado para o cnpj. Caso
        seja por outro motivo, será lançado um erro genérico.
        """

        session = None
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Revendedor deve ser uma string!')
            if not isinstance(cnpj, str):
                raise TypeError('cnpj do Revendedor deve ser uma string!')
            if not isinstance(razao_social, str):
                raise TypeError('razao_social do Revendedor deve ser uma string!')
            if not isinstance(contato, str):
                raise TypeError('contato do Revendedor deve ser uma string!')

            nome = nome.strip().upper()
            cnpj = cnpj.strip().upper()
            razao_social = razao_social.strip().upper()
            contato = contato.strip().upper()

            # validar se os parâmetros informados são válidos
            if not nome:
                raise ValueError('nome do Revendedor não informado!')
            if not cnpj:
                raise ValueError('cnpj do Revendedor não informado!')
            if len(cnpj) != 14:
                raise ValueError('cnpj do Revendedor deve ter 14 caracteres!')
            if not razao_social:
                raise ValueError('razao_social do Revendedor não informada!')
            if not contato:
                raise ValueError('contato do Revendedor não informado!')

            revendedor = Revendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
            session = await createSession()
            async with session.begin():
                print(f'Inserindo Revendedor: {revendedor}')
                session.add(revendedor)
                await session.commit()

                print(f'Revendedor inserido com sucesso!')
                print(f'ID do Revendedor inserido: {revendedor.id}')
                print(f'Nome do Revendedor inserido: {revendedor.nome}')
                print(f'CPNJ do Revendedor inserido: {revendedor.cnpj}')
                print(f'Razão Social do Revendedor inserido: {revendedor.razao_social}')
                print(f'Contato do Revendedor inserido: {revendedor.contato}')
                print(f'Data de criação do Revendedor inserido: {revendedor.data_criacao}')
            return revendedor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'revendedor.cnpj' in str(intg_error):
                    raise RuntimeError(f"Já existe um Revendedor com o CNPJ '{cnpj}' cadastrado. "
                                       f"O CNPJ deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir Revendedor: {intg_error}')

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
    def selectAllRevendedores() -> list['Revendedor'] or []:
        """Seleciona todos os Revendedores na tabela revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises Exception: Informa erro inesperado ao selecionar Revendedores
        """
        try:
            with createSession() as session:
                revendedores = session.query(Revendedor).all()
                return revendedores

        except Exception as exc:
            raise Exception(f'Erro inesperado ao selecionar todos Revendedor: {exc}')

    @staticmethod
    def selectRevendedorPorId(id: int) -> 'Revendedor' or None:
        """Seleciona um Revendedor na tabela revendedor por id
        :param id: int: id do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se encontrado, None caso contrário
        :raises TypeError: Se o id não for um inteiro
        :raises ValueError: Se o id não for informado
        """
        try:
            if not isinstance(id, int):
                raise TypeError('id do Revendedor deve ser um inteiro!')

            if not id:
                raise ValueError('id do Revendedor não informado!')

            with createSession() as session:
                revendedor = session.query(Revendedor).filter(Revendedor.id == id).first()
                return revendedor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRevendedorPorCnpj(cnpj: str) -> 'Revendedor' or None:
        """Seleciona um Revendedor na tabela revendedor por cnpj
        :param cnpj: str: CNPJ do revendedor
        :return: Revendedor or None: Retorna o objeto Revendedor se encontrado, None caso contrário
        :raises TypeError: Se o cnpj não for uma string
        :raises ValueError: Se o cnpj não for informado
        """
        try:
            if not isinstance(cnpj, str):
                raise TypeError('cnpj do Revendedor deve ser uma string!')

            cnpj = cnpj.strip().upper()

            if not cnpj:
                raise ValueError('cnpj do Revendedor não informado!')

            with createSession() as session:
                revendedor = session.query(Revendedor).filter(Revendedor.cnpj == cnpj).first()
                return revendedor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRevendedoresPorNome(nome: str) -> list['Revendedor'] or []:
        """Seleciona os Revendedore na tabela revendedor por nome
        :param nome: str: nome do revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises TypeError: Se o nome não for uma string
        :raises ValueError: Se o nome não for informado
        """
        try:
            if not isinstance(nome, str):
                raise TypeError('nome do Revendedor deve ser uma string!')

            nome = nome.strip().upper()
            if not nome:
                raise ValueError('nome do Revendedor não informado!')

            with createSession() as session:
                revendedores = session.query(Revendedor).filter(Revendedor.nome == nome).first()
                return revendedores

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    @staticmethod
    def selectRendedoresPorRaizSocial(razao_social: str) -> list['Revendedor'] or []:
        """Seleciona os Revendedore na tabela revendedor por razao_social
        :param razao_social: str: razao_social do revendedor
        :return: list[Revendedor] or []: Retorna a lista de objetos Revendedor se encontrado, [] caso contrário
        :raises TypeError: Se o razao_social não for uma string
        :raises ValueError: Se o razao_social não for informado
        """
        try:
            if not isinstance(razao_social, str):
                raise TypeError('razao_social do Revendedor deve ser uma string!')

            razao_social = razao_social.strip().upper()
            if not razao_social:
                raise ValueError('razao_social do Revendedor não informado!')

            with createSession() as session:
                revendedores = session.query(Revendedor).filter(Revendedor.razao_social == razao_social).first()
                return revendedores

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exc:
            print(f'Erro inesperado: {exc}')

    
    @staticmethod
    def updateRevendedor(id_revendedor: int, nome: str, cnpj: str, razao_social: str, contato: str) -> 'Revendedor':
        """Atualiza um Revendedor na tabela revendedor
        :param id_revendedor: int: id do revendedor
        :param nome: str: nome do revendedor
        :param cnpj: str: CNPJ do revendedor
        :param razao_social: str: razão social do revendedor
        :param contato: str: contato do revendedor
        :return: Revendedor: Retorna o objeto Revendedor atualizado
        :raises TypeError: Se o id_revendedor não for um inteiro
        :raises TypeError: Se o nome, cnpj, razao_social ou contato não forem strings
        :raises ValueError: Se o nome, cnpj, razao_social ou contato forem composto só por espaços
        :raises ValueError: Se o id_revendedor não existir na base
        :raises RuntimeError: Se ocorrer um erro de integridade ao atualizar o revendedor, especificado para o cnpj. Caso
        seja por outro motivo, será lançado um erro genérico.
        """
        try:
            if not isinstance(id_revendedor, int):
                raise TypeError('id do Revendedor deve ser um inteiro!')
            if not isinstance(nome, str):
                raise TypeError('nome do Revendedor deve ser uma string!')
            if not isinstance(cnpj, str):
                raise TypeError('cnpj do Revendedor deve ser uma string!')
            if not isinstance(razao_social, str):
                raise TypeError('razao_social do Revendedor deve ser uma string!')
            if not isinstance(contato, str):
                raise TypeError('contato do Revendedor deve ser uma string!')
            
            
            if len(nome) > 0 and all(caractere.isspace() for caractere in nome):
                raise ValueError('nome do Revendedor não pode ser composto só por espaços!')
            if len(cnpj) > 0 and all(caractere.isspace() for caractere in cnpj):
                raise ValueError('cnpj do Revendedor não pode ser composto só por espaços!')
            if len(razao_social) > 0 and all(caractere.isspace() for caractere in razao_social):
                raise ValueError('razao_social do Revendedor não pode ser composto só por espaços!')
            if len(contato) > 0 and all(caractere.isspace() for caractere in contato):
                raise ValueError('contato do Revendedor não pode ser composto só por espaços!')
            
            nome = nome.strip().upper()
            cnpj = cnpj.strip().upper()
            razao_social = razao_social.strip().upper()
            contato = contato.strip().upper()

            with createSession() as session:
                revendedor = session.query(Revendedor).filter_by(id=id_revendedor).first()

                if not revendedor:
                    raise ValueError(f'Revendedor com id={id_revendedor} não cadastrado na base!')

                if nome:
                    revendedor.nome = nome

                if cnpj:
                    revendedor.cnpj = cnpj
                else:
                    cnpj = revendedor.cnpj

                if razao_social:
                    revendedor.razao_social = razao_social

                if contato:
                    revendedor.contato = contato

                revendedor.data_atualizacao = datetime.now()
                session.commit()
                return revendedor

        except IntegrityError as intg_error:
            if 'UNIQUE constraint failed' in str(intg_error):
                if 'revendedor.cnpj' in str(intg_error):
                    raise RuntimeError(f"Já existe um Revendedor com o CNPJ '{cnpj}' cadastrado. "
                                       f"O CNPJ deve ser único.")
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao inserir Revendedor: {intg_error}')

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except Exception as exp:
            raise Exception(f'Erro inesperado ao atualizar Ingrediente: {exp}')

    @staticmethod
    def deleteRevendedorById(id_revendedor: int) -> 'Revendedor':
        """Deleta um Revendedor cadastrado no banco de dados a partir do id.
        :param id_revendedor: int: identificador do Revendedor
        :return: Revendedor: Retorna o objeto Revendedor deletado
        :raises TypeError: Se o id_revendedor não for um inteiro
        :raises RuntimeError: Se ocorrer um erro de integridade ao deletar o Revendedor, especificado para o
        id_revendedor, caso o Revendedor esteja associado a um ou mais alimentos em outras tabelas. Caso seja por outro
        motivo, será lançado um erro genérico.
        :raises ValueError: Se o Revendedor não for encontrado na base
        """
        try:
            if not isinstance(id_revendedor, int):
                raise TypeError('id_revendedor do Revendedor deve ser um inteiro!')

            with createSession() as session:
                revendedor: Revendedor = session.query(Revendedor). \
                    filter_by(id=id_revendedor).first()

                if not revendedor:
                    raise ValueError(f'Revendedor com id={id_revendedor} não cadastrado na base!')

                session.delete(revendedor)
                session.commit()
                return revendedor

        except TypeError as te:
            raise TypeError(te)

        except ValueError as ve:
            raise ValueError(ve)

        except IntegrityError as intg_error:
            if 'FOREIGN KEY constraint failed' in str(intg_error):
                tabelas = DataBaseFeatures.findTabelsWithFkTo(table_name=Revendedor.__tablename__)
                raise RuntimeError(f'Revendedor com id={id_revendedor} não pode ser deletado, '
                                   f'pois pode está associado a um ou mais elementos na(s) tabela(s): {tabelas}')
            else:
                # Tratar outros erros de integridade do SQLAlchemy
                raise RuntimeError(f'Erro de integridade ao deletar Revendedor: {intg_error}')

        except Exception as exc:
            raise Exception(f'Erro inesperado ao deletar Revendedor: {exc}')
        
        
if __name__ == '__main__':
    # try:
    #     Revendedor.insertRevendedor(nome='Sorbato de Potássio', cnpj='12345678901234',
    #                                 razao_social='Sorbato de Potássio LTDA',
    #                                 contato='Sorbato de Potássio')
    # except Exception as e:
    #     print(f'Erro ao inserir Revendedor: {e}')
    #
    # try:
    #     Revendedor.insertRevendedor(nome='Benzoato de Sódio', cnpj='12345678901234',
    #                                 razao_social='Benzoato de Sódio LTDA',
    #                                 contato='Benzoato de Sódio')
    # except Exception as e:
    #     print(f'Erro ao inserir Revendedor: {e}')
    #
    # print('fim')


    try:
        revendedor = Revendedor.deleteRevendedorById(id_revendedor=55)
        print(revendedor)
    except Exception as e:
        print(f'Erro ao deletar Revendedor: {e}')
