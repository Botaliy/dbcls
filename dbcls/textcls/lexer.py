from prompt_toolkit.lexers import Lexer, PygmentsLexer
from pygments.lexers.sql import MySqlLexer
from textcls.utils import get_current_sql_command_lines

class SqlLexer(Lexer):
    # def lex_document(self, document):
    #     result = PygmentsLexer(MySqlLexer).lex_document(document)
    #     return result

    def __init__(self, editor) -> None:
        super().__init__()
        self.editor = editor

    def lex_document(self, document):
        instance = self
        def is_current_line_highlighted(line):
            nonlocal instance
            cursor_position_row = instance.editor.main_buffer.document.cursor_position_row
            start_line, end_line = get_current_sql_command_lines(document.lines, cursor_position_row)
            return start_line <= line <= end_line


        def get_lines(num):
            origin_get_line = PygmentsLexer(MySqlLexer).lex_document(document)
            origin_result = origin_get_line(num)
            need_highlight = is_current_line_highlighted(num)
            if need_highlight:
                new_list = []
                for _token in origin_result:
                    new_list.append((f'{_token[0]} bg:#adacac', _token[1]))
                origin_result = new_list
            return origin_result

        return get_lines
