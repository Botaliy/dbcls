from prompt_toolkit.lexers import Lexer, PygmentsLexer
from pygments.lexers.sql import MySqlLexer

class SqlLexer(Lexer):
    def lex_document(self, document):
        return PygmentsLexer(MySqlLexer).lex_document(document)

