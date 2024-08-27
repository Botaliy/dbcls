from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    VSplit,
    Window,
    HSplit,
    FloatContainer,
    Float,
)
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.buffer import Buffer
from textcls.lexer import SqlLexer
from textcls.completer import completer
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

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
    with open(file, "r") as f:
        return f.read()

class EditorLayout:
    def __init__(self, editor, input) -> None:
        self.editor = editor
        main_buffer = Buffer(
            completer=completer,
            document=Document("", 0),
            multiline=False,
            on_text_changed=handle_text,
            complete_while_typing=True,
            name="dummy-buffer",
        )
        try:
            main_buffer.insert_text(read_file(input))
        except Exception as e:
            raise Exception(f'File not found: {e}')
        self._fc = FloatContainer(
            content=VSplit(
                [
                    # LineToolbar(self.editor),
                    Window(
                        BufferControl(
                            buffer=main_buffer,
                            lexer=SqlLexer(),
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
                )
            ],
        )
        self.layout = Layout(container=HSplit([self._fc]))


class TestContainer(ConditionalContainer):
    def __init__(self):
        super().__init__(
            content=Window(
                FormattedTextControl("Hello"),
                width=5,
                align=WindowAlign.CENTER,
                style="bg:#ff0000",
            ),
            filter=Condition(lambda: True),
        )


class LineNumbersControl(FormattedTextControl):
    def __init__(self, editor):
        def get_line_numbers():
            return "\n".join(
                str(i)
                for i in range(
                    1,
                    editor.editor_layout.layout.current_buffer.document.line_count + 1,
                )
            )

        super().__init__(get_line_numbers)


class LineToolbar(ConditionalContainer):
    def __init__(self, editor):
        super().__init__(
            content=Window(
                LineNumbersControl(editor),
                width=5,
                align=WindowAlign.CENTER,
                style="class:line-numbers",
            ),
            filter=Condition(lambda: True),
        )
        self.editor = editor
        self.show_line_numbers = True
