from pathlib import Path
from typing import Optional

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy import text
from sqlalchemy.pool import QueuePool

from models.model_base import ModelBase

from ScriptsAuxiliares.Auxiliar import Auxiliar

# Descrive all this module does
# This module is responsible for creating the connection to the database
# and creating the tables in the database.
# It also creates a session with the database to perform CRUD operations.
# the createEngine function is responsible for creating the connection to the database
# the createSession function is responsible for creating a session with the database
# the createTables function is responsible for creating the tables in the database
# the __engine variable is responsible for storing the connection to the database
# the __session variable is responsible for storing the session with the database
# This module is used in other modules to perform CRUD operations on the database
# This module is used in other modules to create the tables in the database
# This module is used in other modules to create a session with the database
# This module is used in other modules to create the connection to the database
# If the database already exists, the tables will be deleted and recreated


# This class will be used to create a session with the database and to
# define the connection to the database itself.

__async_engine: Optional[AsyncEngine] = None


def createEngine(sqlite: bool = True, echo: bool = False, timeout: int = 30) -> AsyncEngine:
    """Cria/Configura a engine Async para conexão com o banco de dados
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    :param echo: bool: se True, mostra as queries executadas, se False, não mostra
    :param timeout: int: tempo limite para conexão, padrão 30 segundos
    :return: Engine
    """
    global __async_engine

    if __async_engine:
        return __async_engine

    if sqlite:
        root_path = Auxiliar.getProjectRootDir()
        db_path = Path(f'{root_path}//db/picoles.sqlite')
        folder = Path(db_path).parent
        folder.mkdir(parents=True, exist_ok=True)
        conn_str = f'sqlite+aiosqlite:///{db_path}'
        __async_engine = create_async_engine(
            url=conn_str,  # caminho do banco de dados
            echo=echo,  # se True, mostra as queries executadas
            # fk on

            connect_args={
                "check_same_thread": False,  # para permitir multi-thread
                "timeout": timeout,  # tempo limite para conexão
            }
        )
    else:
        # postgres

        # opção para usar o postgres
        db_user_name = 'postgres'
        db_password = 'postgres'
        local = 'localhost'
        port = '5432'
        db_name = 'picoles'
        conn_str = f'postgresql:+asyncpg//{db_user_name}:{db_password}@{local}:{port}/{db_name}'
        __engine = create_async_engine(
            url=conn_str,  # caminho do banco de dados
            echo=echo  # se True, mostra as queries executadas
        )
    return __async_engine


async def createSession(sqlite: bool = True, echo: bool = False, timeout: int = 30) -> AsyncSession:
    """Cria uma sessão Async com o banco de dados para realizar operações de CRUD
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    :param echo: bool: se True, mostra as queries executadas, se False, não mostra
    :param timeout: int: tempo limite para conexão, padrão 30 segundos
    :return: Session
    """

    global __async_engine
    if __async_engine is None:
        __async_engine = createEngine(sqlite=sqlite, echo=echo, timeout=timeout)

    async_session = sessionmaker(
        bind=__async_engine,  # engine de conexão
        expire_on_commit=False,  # não expira a sessão após o commit
        class_=AsyncSession  # tipo de sessão
    )

    session: AsyncSession = async_session()

    if sqlite:
        # ativa as chaves estrangeiras no sqlite, pois por padrão vem desativado,
        # caso contrário o sqlite não irá verificar se as chaves estrangeiras inseridas já existem e irá inserir
        # o registro mesmo que a chave estrangeira não exista
        # await session.execute(text('PRAGMA foreign_keys=ON;'))
        # close the session
        # await session.close()

        async with session.begin():
            await session.execute(text('PRAGMA foreign_keys=ON;'))
    return session


async def createTables(sqlite: bool = True) -> None:
    """Cria as tabelas no banco de dados
    :param sqlite: bool: se True, usa o sqlite, se False, usa o postgres
    """

    global __async_engine
    if __async_engine is None:
        __async_engine = createEngine(sqlite=sqlite)

    import models.__all_models

    # abre uma conexão com o banco de dados, cria as tabelas e fecha a conexão
    async with __async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)

