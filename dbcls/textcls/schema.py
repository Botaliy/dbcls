from typing import Self


class Schema:

    def __new__(cls) -> Self:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Schema, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.hierarchy = {}
        self.current_db = None

    def __getitem__(self, key):
        return self.hierarchy[key]

    def __setitem__(self, key, value):
        self.hierarchy[key] = value
    
    def tables_in_current_db(self):
        if not self.hierarchy:
            return []
        return self.hierarchy[self.current_db]
    
    def set_current_db(self, db):
        self.current_db = db

    def columns_in_table(self, table):
        return self.hierarchy[self.current_db][table]
