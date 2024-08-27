

class Schema:
    def __init__(self):
        self.hierarchy = {}
        self.current_db = None

    def __getitem__(self, key):
        return self.hierarchy[key]

    def __setitem__(self, key, value):
        self.hierarchy[key] = value

schema = Schema()
