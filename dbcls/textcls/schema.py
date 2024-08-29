

class Schema:
    def __init__(self):
        self.hierarchy = {}
        self.current_db = None

    def __getitem__(self, key):
        return self.hierarchy[key]

    def __setitem__(self, key, value):
        self.hierarchy[key] = value
    
    def tables_in_current_db(self):
        return self.hierarchy[self.current_db]
    
    def set_current_db(self, db):
        self.current_db = db

    def columns_in_table(self, table):
        return self.hierarchy[self.current_db][table]


schema = Schema()


class SQLContext:
    def __init__(self):
        self.tables = {}
        self.current_tables = set()
        self.schema = schema

    def add_table(self, table_name, columns):
        self.tables[table_name] = columns

    def set_current_tables(self, tables):
        self.current_tables = set(tables)

    def reset_current_tables(self):
        self.current_tables.clear()

    def get_columns_for_current_tables(self):
        columns = set()
        for table in self.current_tables:
            if table in self.tables:
                columns.update(self.tables[table])
        return list(columns)
    

sql_context = SQLContext()