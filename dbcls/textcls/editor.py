from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window, HSplit, VSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import Frame
from prompt_toolkit.document import Document
from pygments.lexers.python import PythonLexer
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.formatted_text import FormattedText
import visidata
from textcls.kb import create_key_bindings
from prompt_toolkit.enums import EditingMode
from textcls.layout import EditorLayout
from textcls.completer import completer


background_color = "#2C3E50"
text_color = "#ECF0F1"
highlight_color = "#96aeff"
line_numbers = "#dbbfbf"
special = "#FF0000 bold"

style = Style.from_dict(
    {
        "window": f"bg:{background_color} {text_color}",
        "line-numbers": f"bg:{background_color} #000000",
        "current-line": f"bg:{highlight_color}",
        "sql-keyword": f"{special}",  # Red and bold for special words
    }
)


class Editor:
    def __init__(self, input):
        self.input = input
        
        def handle_action_comm(buff):
            # if 'Y' in buff.text:
            #     self.save_buffer()
            #     self.app.exit() 
            #     return
            # if 'N' in buff.text:
            #     self.app.exit()
            #     return
            print(1)

        def handle_action(buf):
            buf.completer.get_completions(buf.document, buf.cursor_position)

        self.main_buffer = Buffer(
            completer=completer,
            document=Document("", 0),
            multiline=False,
            on_text_changed=handle_action,
            complete_while_typing=True,
            name="dummy-buffer"
        )
        self.confirm_save_buffer = Buffer(
            multiline=False)
        self.editor_layout = EditorLayout(self, input)
        self.key_bindings = create_key_bindings(self)
        self.app = self._create_app()
        self.sql_client = None

    async def run(self):
        await self.app.run_async()
    

    async def redraw(self):
        self.app.renderer.erase()

    def _create_app(self):
        application = Application(
            editing_mode=EditingMode.EMACS,
            layout=self.editor_layout.layout,
            key_bindings=self.key_bindings,
            style=style,
            full_screen=True,
        )
        return application
    
    def set_client(self, client):
        self.sql_client = client

    def get_sql_command(self):
        buff = self.editor_layout.layout.current_buffer
        cursor_position = buff.cursor_position
        delimiter = ';'
        text = buff.text
        # start_pos = text.rfind(delimiter, 0, cursor_position) + 1

        # end_pos = text.find(delimiter, 0, cursor_position)
        # if end_pos == -1:  # Если не найден, берем до конца буфера
        #     end_pos = len(text)
        
        # sql_command = text[start_pos:end_pos].strip()
        
        start = text.rfind(';', 0, cursor_position) + 1
        end = text.find(';', cursor_position)
        # Если конец не найден, берем до конца текста
        if end == -1:
            end = len(text)
        current_command = text[start:end].strip()
        # Если курсор находится после всех команд и current_command пустой,
        # попробуем найти последнюю команду до курсора.
        if not current_command:
            last_semicolon = text.rfind(';')
        
            if last_semicolon != -1 and cursor_position > last_semicolon:
                # Находим начало последней команды до последнего `;`
                start = text.rfind(';', 0, last_semicolon) + 1
                current_command = text[start:last_semicolon].strip()

        return current_command

    def run_visidata(self, result):
        visidata.vd.run()
        visidata.vd.view(result.data)

    def save_buffer(self):
        buff: Buffer = self.main_buffer
        with open(self.input, "w") as f:
            f.write(buff.text)
    
    def equal_buffer(self):
        buff: Buffer = self.editor_layout.layout.current_buffer
        return buff.text == self.editor_layout.start_text

    def confirm_save(self):
        self.confirm_save_buffer.text = "Save changes? Y or N"
        self.editor_layout.layout.focus(self.confirm_save_buffer)
