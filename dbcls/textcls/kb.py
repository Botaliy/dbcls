from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_completions
import asyncio


def create_key_bindings(editor: 'Editor'):
    kb = KeyBindings()

    @kb.add("c-q")
    def exit_(event):
        event.app.exit()

    @kb.add("enter")
    def insert_completion(event,
                          filter=has_completions):
        b = editor.editor_layout.layout.current_buffer
        if b.complete_state:
            b.complete_state = None
            b.insert_text(" ")
        else:
            b.insert_text("\n")

    @kb.add("c-r")
    async def run_sql_command(event):
        comm = editor.get_sql_command()
        result = await editor.sql_client.execute(comm)
        editor.run_visidata(result)
        await editor.redraw()

    
    @kb.add("c-s")
    def save_file(event):
        editor.save_buffer()

    return kb
