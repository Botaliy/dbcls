import asyncio
# import sys
import json
# from functools import partial
from time import time
from typing import Callable
from typing import Optional
import logging
import visidata
import argparse

from dbcls.textcls.editor import Editor
from dbcls.clients.base import Result
from dbcls.clients.sqlite3 import Sqlite3Client


client = None

logging.basicConfig(level=logging.WARNING)


def get_sel(editor) -> str:
    pass
    # selection = wnd.screen.selection
    # if not selection.is_selected():
    # if not selection.is_rectangular():
    #     selected_from, selected_to = selection.get_selrange()
    #     return wnd.document.gettext(selected_from, selected_to)
    #     return
    # data = []
    # position_from, position_to, column_from, column_to = selection.get_rect_range()

    # while position_from < position_to:
    #     position_and_col_string = selection.get_col_string(position_from, column_from, column_to)
    #     if position_and_col_string:
    #         *_, col_string = position_and_col_string
    #         data.append(col_string.rstrip('\n'))
    #     else:
    #         data.append('')
    #     position_from = wnd.document.geteol(position_from)

    # return '\n'.join(data)


def get_current_sql_rows_pos(editor) -> list[int]:
    """Analze current editor position to find rows of sql query under the cursor"""
    pass
    # pos = wnd.cursor.pos
    # start_pos = pos
    # rows = set()
    # back_only = False

    # if (
    #     pos < len(wnd.document.buf) and
    #     (
    #         isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos), NonSqlComment) or
    #         (
    #             pos > 0 and
    #             wnd.document.buf[pos] == '\n' and
    #             isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos - 1), NonSqlComment)
    #         )
    #     )
    # ):
    #     return []

    # for pos in range(pos, 0, -1):
    #     if pos >= len(wnd.document.buf):
    #         continue

    #     if (
    #         wnd.document.buf[pos] == ';' and
    #         isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos), DefaultToken) and
    #         wnd.document.gettol(pos) == wnd.document.gettol(start_pos)
    #     ):
    #         rows.add(wnd.document.gettol(pos))
    #         back_only = True

    #     if (
    #         (
    #             (
    #                 (
    #                     wnd.document.buf[pos - 1] == ';' and
    #                     wnd.document.gettol(pos) != wnd.document.gettol(start_pos)
    #                 ) or
    #                 (wnd.document.buf[pos] == '\n' and (pos - 1) <= 0) or
    #                 (wnd.document.buf[pos] == '\n' and wnd.document.buf[pos - 1] == '\n')
    #             ) and
    #             isinstance(
    #                 wnd.document.mode.tokenizer.get_token_at(wnd.document, pos - 1),
    #                 (DefaultToken, CaseInsensitiveKeywords)
    #             )
    #         ) or
    #         isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos), NonSqlComment) or
    #         (
    #             wnd.document.buf[pos] == '\n' and
    #             isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos - 1), NonSqlComment)
    #         )
    #     ):
    #         break

    #     rows.add(wnd.document.gettol(pos))

    # if back_only:
    #     return list(sorted(rows))

    # pos = start_pos

    # for pos in range(pos, len(wnd.document.buf)):
    #     if (
    #         isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos), NonSqlComment) or
    #         (
    #             (
    #                 wnd.document.buf[pos] == ';' or
    #                 (wnd.document.buf[pos] == '\n' and len(wnd.document.buf) <= pos + 1) or
    #                 (wnd.document.buf[pos] == '\n' and wnd.document.buf[pos + 1] == '\n')
    #             ) and
    #             isinstance(wnd.document.mode.tokenizer.get_token_at(wnd.document, pos), DefaultToken)
    #         )
    #     ):
    #         break

    #     rows.add(wnd.document.gettol(pos))

    # return list(sorted(rows))


def get_expression_under_cursor(editor) -> str:
    pass
    # line = ''
    # for row in get_current_sql_rows_pos(wnd):
    #     _, sel = wnd.screen.document.getline(row)
    #     if sel:
    #         line += sel

    # return line


def print_center(editor, text: str):
    pass
    # num_rows, num_cols = window.getmaxyx()
    # x = num_cols // 2 - len(text) // 2
    # y = num_rows // 2
    # window.addstr(y, x, text)
    # window.refresh()


async def await_and_print_time(
        editor,
        coro: asyncio.coroutines
) -> Result:
    pass
    # start = time()
    # task = asyncio.create_task(coro)

    # posy, _ = editor.get_cursor_loc()

    # # win = curses.newwin(3, 50, max(posy - 3, 0), 5)

    # try:

    #     while not task.done():
    #         wnd.mainframe._cwnd.timeout(0)
    #         key = wnd.mainframe._cwnd.getch()

    #         if key == 27:
    #             task.cancel()
    #             raise asyncio.CancelledError()

    #         await asyncio.sleep(0.1)

    #         print_center(win, f'Running (press ESC to cancel): {round(time() - start, 2)}s ')
    # finally:
    #     del win
    # return await task


# def fix_visidata_curses():
#     if visidata.color.colors.color_pairs:
#         for (fg, bg), (pairnum, _) in visidata.color.colors.color_pairs.items():
#             curses.init_pair(pairnum, fg, bg)


# def fix_kaa_curses(wnd: TextEditorWindow):
#     curses.endwin()
#     kaa.app.show_cursor(1)

#     for pairnum, (fg, bg) in enumerate(kaa.app.colors.pairs.keys()):
#         curses.init_pair(pairnum, fg, bg)

#     wnd.draw_screen(force=True)


def run_corutine_and_show_result(editor, coro: asyncio.coroutines):
    start = time()
    end = None
    message = ''

    try:
        try:
            result = asyncio.run(await_and_print_time(
                editor,
                coro
            ))
        except asyncio.CancelledError:
            end = time()
            message = 'Cancelled'
            return

        end = time()
        message = str(result)

        if not result or not result.data:
            return

        # fix_visidata_curses()

        visidata.vd.run()
        visidata.vd.view(result.data)
    except Exception as exc:
        end = time()
        message = str(exc)
    finally:
        editor.document.set_title(client.get_title())
        # kaa.app.messagebar.set_message(f'{round(end - start, 2)}s {message}')
        # fix_kaa_curses(wnd)


# @command('db.query')
def db_query(editor):
    sel = get_sel(editor)

    if not sel:
        sel = get_expression_under_cursor(editor)

    if not sel or not sel.strip():
        # kaa.app.messagebar.set_message("Nothing to execute")
        return

    selection = sel.strip()
    run_corutine_and_show_result(editor, client.execute(selection))


# @command('db.show_tables')
# def db_show_tables(wnd: TextEditorWindow):
#     run_corutine_and_show_result(wnd, client.get_tables())


# @command('db.show_databases')
# def db_show_databases(wnd: ):
#     run_corutine_and_show_result(wnd, client.get_databases())


def on_keypressed(
        self,
        original_fn: Callable,
        editor,
        event,
        key: Optional[str],
        commands: list[str],
        candidate: list[tuple]
):
    pass
    # pos = wnd.cursor.pos
    # tol = wnd.document.gettol(pos)
    # wnd.document.marks['current_script'] = (0, tol)
    # wnd.document.style_updated()
    # wnd.document.set_title(client.get_title())
    # return original_fn(wnd, event, key, commands, candidate)


def on_cursor_located(
        self,
        original_fn: Callable,
        wnd,
        *args, **kwargs
):
    wnd.document.highlights = []
    for id, row_pos in enumerate(get_current_sql_rows_pos(wnd)):
        wnd.document.highlights.append(
            row_pos
        )
    return original_fn(wnd, *args, **kwargs)


def get_line_overlays(self, original_fn: Callable) -> dict[int, str]:
    highlights = {}
    highlights.update(original_fn())

    for pos in self.document.highlights:
        highlights[pos] = 'cursor-row'

    return highlights


# @setup('kaa.filetype.default.defaultmode.DefaultMode')
# def editor(mode):
#     # register command to the mode
#     mode.add_command(db_query)
#     mode.add_command(db_show_tables)
#     mode.add_command(db_show_databases)
#     mode.on_keypressed = partial(on_keypressed, mode, mode.on_keypressed)
#     # To determine sql expression under current cursor after each key press
#     mode.on_cursor_located = partial(on_cursor_located, mode, mode.on_cursor_located)
#     # To highligt lines determined in on_cursor_located
#     mode.get_line_overlays = partial(get_line_overlays, mode, mode.get_line_overlays)


    # add key bind th execute 'run.query'
    # mode.add_keybinds(keys={
    #     (alt, 'r'): 'db.query',
    #     (alt, 't'): 'db.show_tables',
    #     (alt, 'e'): 'db.show_databases',
    #     (ctrl, 's'): 'file.save',
    #     (ctrl, 'f'): 'search.showsearch',
    #     (ctrl, 'r'): 'search.showreplace',
    #     (ctrl, 'q'): 'file.quit',
    #     (alt, backspace): 'edit.backspace.word'
    # })

    # mode.SHOW_LINENO = True
    # # Syntax highlight
    # mode.tokenizer = make_tokenizer()
    # mode.themes.append(sql_editor_themes)

def build_parser():
    pass

async def main():
    global client

    parser = argparse.ArgumentParser(description='Пример парсинга аргументов.')

    parser.description = 'DB connection tool'
    parser.add_argument('--config', '-c', dest='config', help='specify config path', default='')
    parser.add_argument('--host', '-H', dest='host', help='specify host name', default='')
    parser.add_argument('--user', '-u', dest='user', help='specify user name', required=False)
    parser.add_argument('--password', '-p', dest='password', default='', help='specify raw password')
    parser.add_argument('--port', '-P', dest='port', default='', help='specify port')
    parser.add_argument('--engine', '-E', dest='engine', help='specify db engine', required=False,
        choices=['clickhouse', 'mysql', 'postgres', 'sqlite3'])
    parser.add_argument('--dbname', '-d', dest='dbname', help='specify db name', required=False)
    parser.add_argument('--filepath', '-f', dest='filepath', help='specify db filepath', required=False)
    args, argv = parser.parse_known_args()
    if len(argv) != 1:
        parser.error(f"Only one filename: {', '.join(argv)}")

    host = args.host
    username = args.user
    password = ''

    if args.password:
        password = args.password

    port = args.port
    engine = args.engine
    dbname = args.dbname
    filepath = args.filepath

    if args.config:
        with open(args.config) as f:
            config = json.load(f)

        if not host or host == '127.0.0.1':
            host = config.get('host', '')
        if not port:
            port = config.get('port', '')
        if not username:
            username = config.get('username', '')
        if not password:
            password = config.get('password', '')
        if not dbname:
            dbname = config.get('dbname', '')
        if not engine:
            engine = config.get('engine', '')
        if not filepath:
            filepath = config.get('filepath', '')
    editor = Editor(argv[0])
    # imported here to make db libs dependencies optional
    if engine == 'clickhouse':
        from dbcls.clients.clickhouse import ClickhouseClient
        client = ClickhouseClient(host, username, password, dbname, port=port)
    if engine == 'mysql':
        from dbcls.clients.mysql import MysqlClient
        client = MysqlClient(host, username, password, dbname, port=port)
    if engine == 'postgres':
        from dbcls.clients.postgres import PostgresClient
        client = PostgresClient(host, username, password, dbname, port=port)
    if engine == 'sqlite3':
        client = Sqlite3Client(filepath)

    
    editor.set_client(client)
    editor.load_cached_schema()
    editor.sql_client.schema.hierarchy['ulog'] = [1,2,3,4,5]
    await editor.run()

# if __name__ == '__main__':
asyncio.run(main())
