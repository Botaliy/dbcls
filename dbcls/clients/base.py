import abc
from contextlib import suppress
from dataclasses import (
    dataclass,
    field,
)
import pickle
from dbcls.textcls.schema import Schema


@dataclass
class Result:
    data: list[dict] = field(default_factory=list)
    rowcount: int = 0
    message: str = ''

    def __str__(self) -> str:
        if self.message:
            return self.message

        if self.data:
            return f'{self.rowcount} rows returned'

        if self.rowcount:
            return f'{self.rowcount} rows affected'

        return 'Empty set'


class ClientClass(abc.ABC):
    ENGINE = ''

    def __init__(self, host: str, username: str, password: str, dbname: str, port: str):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.schema = Schema()
        self.schema.set_current_db(dbname)

    @abc.abstractmethod
    def get_databases(self) -> Result:
        pass

    @abc.abstractmethod
    def get_tables(self) -> Result:
        pass

    async def change_database(self, database: str):
        old_db = self.dbname
        self.dbname = database
        try:
            await self.execute('SELECT 1')
            return Result(message=f'You are now connected to database "{database}"')
        except Exception:
            self.dbname = old_db
            raise

    def get_title(self) -> str:
        return f'{self.ENGINE} {self.host}:{self.port} {self.dbname}'

    @abc.abstractmethod
    async def execute(self, sql) -> Result:
        pass

    
    def cache_schema(self):
        with suppress(Exception):
            with open('schema.pkl', 'wb') as f:
                pickle.dump(schema, f)
        
    def load_cached_schema(self):
        with suppress(Exception):
            with open('schema.pkl', 'rb') as f:
                self.schema = pickle.load(f)
