from typing import Iterable
from prompt_toolkit.completion import Completer, merge_completers
from prompt_toolkit.completion.base import CompleteEvent, Completion
from prompt_toolkit.document import Document
import re
from .sql_keywords import SQL_WORDS
from textcls.schema import schema
from prompt_toolkit.filters import Condition, Always
from textcls.utils import get_current_sql_expression

# class CustomCondition(Completion):
#     def __init__(
#         self,
#         text,
#         start_position=0,
#         display=None,
#         display_meta=None,
#         style="",
#         selected_style="",
#         action=None,
#     ):
#         super().__init__(
#             text,
#             start_position=start_position,
#             display=display,
#             display_meta=display_meta,
#             style=style,
#             selected_style=selected_style,
#         )
#         self.action = action

#     def apply(self, document):
#         new_document = super().apply(document)
#         if self.action:
#             print(f"\nВыполняется действие: {self.action}")
#         return new_document

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

class SqlTablesAndColumnsCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor()
        words = set()
        if is_after_from(document, word_before_cursor):
            for table in schema.tables_in_current_db():
                if table.upper().startswith((word_before_cursor.upper())):
                    words.add(table)

        start, end = get_current_sql_expression(document)
        current_sql = document.text[start:end]
        if is_after_word(current_sql, 'WHERE'):
            for table in schema.tables_in_current_db():
                if table.upper().startswith((word_before_cursor.upper())):
                    words.add(table)
        for w in sorted(words):
            start_position = -len(word_before_cursor)
            yield Completion(w, start_position=start_position)


completer = merge_completers([SQLKeywordsCompleter(), SqlTablesAndColumnsCompleter()])
