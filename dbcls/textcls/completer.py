from typing import Iterable
from prompt_toolkit.completion import Completer, merge_completers
from prompt_toolkit.completion.base import CompleteEvent, Completion
from prompt_toolkit.document import Document
import re
from .sql_keywords import SQL_WORDS
from textcls.utils import get_current_sql_expression
from textcls.schema import Schema

schema = Schema()

class SQLKeywordsCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor()
        words = set()
        if len(word_before_cursor) < 2:
            return
        for w in re.split(r"\W", word_before_cursor):
            for sw in SQL_WORDS:
                if sw.startswith(w.upper()) and sw != w.upper():
                    words.add(sw)
        for w in sorted(words):
            start_position = -len(word_before_cursor)
            yield Completion(w, start_position=start_position)


def is_after_from(document, word):
    if (
        len(word) > 0
        and len(document.current_line.upper().split(" ")) > 1
        and document.current_line.upper().split(" ")[-2] == 'FROM'
    ):
        return True

def is_after_word(current_sql, word):
    if (
        len(current_sql) > 0
        and len(current_sql.upper().split(" ")) > 1
        and word in current_sql.upper().split(" ")
    ):
        return True

def find_tables_in_current_sql_expression(sql_exp, tables):
    tables_in_sql = set()
    for table in tables:
        if table.upper() in sql_exp.upper():
            tables_in_sql.add(table)
    return tables_in_sql

class SqlTablesAndColumnsCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor()
        words = set()
        tables = schema.tables_in_current_db()
        if is_after_from(document, word_before_cursor) and not is_after_word(document.text, 'WHERE'):
            for table in tables:
                if table.upper().startswith((word_before_cursor.upper())):
                    words.add(table)

        start, end = get_current_sql_expression(document)
        current_sql = document.text[start:end]
        if is_after_word(current_sql, 'WHERE'):
            row_tables = find_tables_in_current_sql_expression(current_sql, tables)
            if row_tables and is_after_word(current_sql, 'WHERE'):
                for table in row_tables:
                    columns = schema[schema.current_db][table]
                    for column in columns:
                        if column.upper().startswith((word_before_cursor.upper())):
                            words.add(column)
        
        for w in sorted(words):
            start_position = -len(word_before_cursor)
            yield Completion(w, start_position=start_position)


completer = merge_completers([SQLKeywordsCompleter(), SqlTablesAndColumnsCompleter()])
