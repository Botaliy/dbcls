from prompt_toolkit.lexers import Lexer, PygmentsLexer
from pygments.lexers.sql import MySqlLexer
from textcls.utils import get_current_sql_command_lines

class SqlLexer(Lexer):

    def __init__(self, editor) -> None:
        super().__init__()
        self.editor = editor
    
    def highlight_current_line(self, line):
        new_list = []
        for token in line:
            new_list.append((f'{token[0]} bg:#d5d3d3', token[1]))
        return new_list


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
                origin_result = self.highlight_current_line(origin_result)
            return origin_result

        return get_lines
