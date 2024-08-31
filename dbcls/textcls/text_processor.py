from prompt_toolkit import PromptSession
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.processors import Processor, Transformation
from pygments.token import Token
from textcls.utils import get_current_sql_expression

class CurrentCommandHighlighter(Processor):
    def __init__(self, cursor_position_callback):
        self.cursor_position_callback = cursor_position_callback

    def apply_transformation(self, document, lineno, source_to_display, tokens):
        cursor_position = self.cursor_position_callback()
        text = document.text

        current_command = get_current_sql_expression(text, cursor_position)

        def highlight_command(line):
            if current_command in line:
                start_idx = line.find(current_command)
                end_idx = start_idx + len(current_command)
                return [
                    (Token.Text, line[:start_idx]),
                    (Token.CurrentCommand, line[start_idx:end_idx]),
                    (Token.Text, line[end_idx:])
                ]
            return [(Token.Text, line)]

        new_tokens = highlight_command(document.lines[lineno])
        return Transformation(new_tokens)