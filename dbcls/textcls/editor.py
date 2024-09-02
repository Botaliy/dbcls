import asyncio
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
import visidata
from textcls.kb import create_key_bindings
from prompt_toolkit.enums import EditingMode
from textcls.layout import EditorLayout
from textcls.completer import completer
from textcls.utils import get_current_sql_command_lines
from prompt_toolkit.styles import Style
from textcls.schema import Schema

style = Style.from_dict({
    'pygments.keyword': 'bold #fc3232',
})

class Editor:
    def __init__(self, input):
        self.input = input
        
        def handle_action(buf):
            buf.completer.get_completions(buf.document, buf.cursor_position)
        self.timer_window = Buffer()
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
        self.editor = self
        self.sql_client = None
        self.async_task = None

    async def run(self):
        await self.app.run_async()
    
    async def redraw(self):
        self.app.renderer.erase()

    def _create_app(self):
        application = Application(
            editing_mode=EditingMode.EMACS,
            layout=self.editor_layout.layout,
            key_bindings=self.key_bindings,
            full_screen=True,
            style=style
        )
        return application
    
    def set_client(self, client):
        self.sql_client = client

    def get_sql_command(self):
        document = self.editor.main_buffer.document
        cursor_position_row = document.cursor_position_row
        start_line, end_line = get_current_sql_command_lines(document.lines, cursor_position_row)
        current_command = self.main_buffer.document.text.lines[start_line:end_line].strip()
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

    async def load_scheme(self):
        await self.sql_client.load_scheme()

    async def async_timer_text(self, window):
        current_time = 0
        while True:
            window.text = f"Running task: {current_time} "
            await asyncio.sleep(0.1)
            current_time = round(current_time + 0.1, 1)
        

    async def async_run_command(self, command, *args):
        self.editor_layout.layout.focus(self.timer_window)
        result = None
        timer_task = asyncio.create_task(self.async_timer_text(self.timer_window))
        self.async_task = asyncio.create_task(command(*args))
        try:
            result = await self.async_task
        except asyncio.CancelledError:
            pass
        finally:
            self.async_task = None
            timer_task.cancel()
            self.editor_layout.layout.focus(self.main_buffer)
        return result

    def cancel_current_task(self):
        if self.async_task:
            self.async_task.cancel()
            self.async_task = None
        self.editor_layout.layout.focus(self.main_buffer)
    
    def load_cached_schema(self):
        self.sql_client.load_cached_schema()