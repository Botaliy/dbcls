from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_completions


def create_key_bindings(editor):
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
        b = editor.editor_layout.layout.current_buffer
        print(b)

    return kb
