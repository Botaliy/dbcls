from typing import Iterable
from prompt_toolkit.completion import Completer, merge_completers, ConditionalCompleter
from prompt_toolkit.completion.base import CompleteEvent, Completion
from prompt_toolkit.document import Document
import re
from .sql_keywords import SQL_WORDS
from textcls.schema import schema
from prompt_toolkit.filters import 


def is_after_keyword(document, keyword):
    return keyword.lower() in document.text.lower().split()


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


class SqlCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor()
        words = set()
        if (
            len(word_before_cursor) > 0
            and len(document.current_line.upper().split(" ")) > 1
            and document.current_line.upper().split(" ")[-2] == "FROM"
        ):
            for table in schema[schema.current_db]:
                if table.startswith(word_before_cursor):
                    words.add(table)
        if len(word_before_cursor) == 0 or len(word_before_cursor) < 2:
            return
        for w in re.split(r"\W", word_before_cursor):
            for sw in SQL_WORDS:
                if sw.startswith(w.upper()) and sw != w.upper():
                    words.add(sw)
        for w in sorted(words):
            start_position = -len(word_before_cursor)
            yield Completion(w, start_position=start_position)


completer = merge_completers(
    [
        ConditionalCompleter(SQLKeywordsCompleter(), filter=True),
        ConditionalCompleter(
            SqlCompleter(),
            condition=lambda document: is_after_keyword(document, "SELECT"),
        ),
    ]
)
