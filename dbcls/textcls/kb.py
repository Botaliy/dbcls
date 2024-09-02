from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_completions
from prompt_toolkit.keys import Keys


def create_key_bindings(editor: 'Editor'):
    kb = KeyBindings()

    @kb.add(Keys.ControlQ)
    def exit_(event):
        if not editor.equal_buffer():
            editor.confirm_save()
            return
        event.app.exit()

    @kb.add(Keys.Enter)
    def insert_completion(event,
                          filter=has_completions):
        b = editor.editor_layout.layout.current_buffer
        if b.complete_state:
            b.complete_state = None
            b.insert_text(" ")
        else:
            b.insert_text("\n")

    @kb.add(Keys.ControlR)
    @kb.add('®')
    @kb.add('escape','r')
    async def run_sql_command(event):
        comm = editor.get_sql_command()
        result = await editor.async_run_command(editor.sql_client.execute, comm)
        editor.run_visidata(result)
        await editor.redraw()

    @kb.add(Keys.ControlT)
    async def renew_schema(event):
        await editor.async_run_command(editor.load_scheme)

    @kb.add(Keys.Escape)
    async def cancel_async_task(event):
        editor.cancel_current_task()
    
    @kb.add(Keys.ControlS)
    def save_file(event):
        editor.save_buffer()
    

    return kb
