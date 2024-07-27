from typing import AsyncGenerator
from time import time

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine.interfaces import DBAPICursor, _DBAPIAnyExecuteParams
from sqlalchemy.engine.interfaces import ExecutionContext

from config import settings
from logger import db_query_logger
from user.models import User


test_db_settings = settings.test_database
db_settings = settings.database
test_settings = settings.test

if test_settings.IS_TESTING:
    engine = create_async_engine(test_db_settings.DATABASE_URL_ASYNC)
else:
    engine = create_async_engine(db_settings.DATABASE_URL_ASYNC)
    
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: _DBAPIAnyExecuteParams,
    context: ExecutionContext | None,
    executemany: bool,
) -> None:
    """
    Event listener that is called before executing a cursor operation.

    This function logs the start time of the query and the SQL statement 
    along with its parameters before the execution of the query starts, 
    allowing for tracing of query performance.

    Args:
        conn (Connection): The database connection being used.
        cursor (DBAPICursor): The cursor associated with the execution.
        statement (str): The SQL statement to be executed.
        parameters (_DBAPIAnyExecuteParams): The parameters that will be passed to the statement.
        context (ExecutionContext | None): The execution context associated with the statement, 
                                            which can be used to store information across 
                                            the execution lifecycle.
        executemany (bool): A flag indicating whether the execution is for multiple statements.
    """
    context._query_start_time = time()
    db_query_logger.debug("Start Query:\n%s" % statement)
    db_query_logger.debug("Parameters:\n%r" % (parameters,))


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: _DBAPIAnyExecuteParams,
    context: ExecutionContext,
    executemany: bool,
) -> None:
    """
    Event listener that is called after executing a cursor operation.

    This function logs the total time taken for the query execution and marks 
    the completion of the query, allowing for performance tracking.

    Args:
        conn (Connection): The database connection being used.
        cursor (DBAPICursor): The cursor associated with the execution.
        statement (str): The SQL statement that was executed.
        parameters (_DBAPIAnyExecuteParams): The parameters that were passed to the statement.
        context (ExecutionContext): The execution context associated with the statement, 
                                    used to retrieve any information stored during execution.
        executemany (bool): A flag indicating whether the execution was for multiple statements.
    """
    total = time() - context._query_start_time
    db_query_logger.debug("Query Complete!\n\n")
    db_query_logger.debug("Total Time: %.02fms" % (total * 1000))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronously creates and yields a database session.

    This function provides an asynchronous session for database operations, 
    ensuring that the session is properly managed and closed after use.

    Yields:
        AsyncGenerator[AsyncSession, None]: An asynchronous session for database interaction.
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Provides a user database instance for the given session.

    This function yields an instance of the SQLAlchemy user database that 
    can be used to perform user-related database operations.

    Args:
        session (AsyncSession): The asynchronous session for interacting with the database.

    Yields:
        SQLAlchemyUserDatabase: An instance of the SQLAlchemy user database.
    """
    yield SQLAlchemyUserDatabase(session, User)
