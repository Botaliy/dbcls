from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    VSplit,
    Window,
    HSplit,
    FloatContainer,
    Float,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.containers import WindowAlign
from dbcls.textcls.lexer import SqlLexer
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
import os
from prompt_toolkit.keys import Keys

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
    }
)


def handle_text(buffer):
    buffer.completer.get_completions(buffer.document, buffer.cursor_position)


def handle_line_prefix(buffer, wrap_count):
    return FormattedText([("class:line-numbers", f" {buffer + 1} ")])

def read_file(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return f.read()
    else:
        return ''

class EditorLayout:
    def __init__(self, editor, input) -> None:
        self.editor = editor
        
        try:
            self.start_text = read_file(input)
        except Exception as e:
            raise Exception(f'File not found: {e}')
        editor.main_buffer.insert_text(self.start_text)
        self._fc = FloatContainer(
            content=VSplit(
                [
                    Window(
                        BufferControl(
                            buffer=editor.main_buffer,
                            lexer=SqlLexer(editor)
                        ),
                        wrap_lines=True,
                        get_line_prefix=handle_line_prefix,
                    ),
                ]
            ),
            floats=[
                Float(
                    content=CompletionsMenu(max_height=16),
                    allow_cover_cursor=True,
                    xcursor=True,
                    ycursor=True,
                ),
                Float(
                    content=TimerWindow(editor=editor),
                    height=10,
                    transparent=True,
                    xcursor=True,
                    ycursor=True,
                )
            ],
        )
        self.layout = Layout(container=HSplit([
            self._fc,
            BottomToolbar(self.editor),
            ]))


class BottomToolbar(ConditionalContainer):
    def __init__(self, editor):
        self.editor = editor
        super().__init__(
            content=Window(
                BufferControl(
                    buffer=editor.confirm_save_buffer,
                    key_bindings=self.get_kb(),
                ),
                align=WindowAlign.LEFT,
                height=2,
                style="bg:#cacaca",
            ),
            filter=has_focus(editor.confirm_save_buffer),
        )
    
    def get_kb(self):
        kb = KeyBindings()

        @kb.add('y')
        @kb.add('Y')
        def save_file(event):
            self.editor.save_buffer()
            self.editor.app.exit()

        @kb.add('n')
        @kb.add('N')
        def exit(event):
            self.editor.app.exit()
        
        return kb
    
class TimerWindow(ConditionalContainer):
    def __init__(self, editor):
        self.editor = editor
        super().__init__(
            content=Window(
                BufferControl(
                    buffer=editor.timer_window,
                    key_bindings=self.get_kb(),
                ),
                style="bg:#ffffff",
                width=50,
                height=8,
            ),
            filter=has_focus(editor.timer_window),
        )
    
    def get_kb(self):
        kb = KeyBindings()

        @kb.add(Keys.Escape)
        async def cancel_async_task(event):
            self.editor.cancel_current_task()
        
        return kb
