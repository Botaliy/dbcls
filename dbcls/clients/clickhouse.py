import aiochclient
from aiohttp import ClientSession
from aiohttp import ClientTimeout

from .base import (
    ClientClass,
    Result,
)


class ClickhouseClient(ClientClass):
    ENGINE = 'Clickhouse'

    def __init__(self, host, username, password, dbname, port='8123'):
        super().__init__(host, username, password, dbname, port)
        if not dbname:
            self.dbname = 'default'
        
        if not port:
            self.port = '8123'

    async def get_tables(self) -> Result:
        return await self.execute('SHOW TABLES')

    async def get_databases(self) -> Result:
        return await self.execute('SHOW DATABASES')
    

    async def load_columns(self, table) -> Result:
        return await self.execute(f'describe table {table}')
    
    async def get_current_database(self) -> Result:
        return await self.execute('SELECT currentDatabase()')
    
    async def load_scheme(self) -> None:
        result = await self.get_current_database()
        db_name = next(i for i in result.data[0].values())
        self.schema.current_db = db_name
        self.schema[db_name] = {}
        tables: Result = await self.get_tables()
        for table in tables.data:
            table_name = table['name']
            columns = await self.load_columns(table_name)
            self.schema[db_name][table_name] = [i['name'] for i in columns.data]
        self.cache_schema()

    async def execute(self, sql) -> Result:
        db = self.dbname

        if sql.strip().upper().startswith('USE '):
            db = sql.strip().split(' ')[1].rstrip(';')
            return await self.change_database(db)

        timeout = ClientTimeout(connect=60)

        async with ClientSession(timeout=timeout) as sess:
            client = aiochclient.ChClient(
                sess,
                url=f"http://{self.host}:{self.port}",
                database=db,
                user=self.username,
                password = self.password,
            )

            data = [dict(x) for x in await client.fetch(sql.rstrip(';'), decode=True)]

            return Result(data=data, rowcount=len(data))
