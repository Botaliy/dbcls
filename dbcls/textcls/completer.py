from typing import Iterable
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion.base import CompleteEvent, Completion
from prompt_toolkit.document import Document
import re
from .sql_keywords import SQL_WORDS
from textcls.schema import schema



class SqlCompleter(Completer):


    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        word_before_cursor = document.get_word_before_cursor()
        if word_before_cursor.upper() == 'FROM' and schema.current_db:
            for table in schema[schema.current_db]:
                 yield Completion(table, start_position=-len(word_before_cursor))
        words = set()
        if len(word_before_cursor) == 0 or len(word_before_cursor) < 2:
            return
        for w in re.split(r"\W", word_before_cursor):
            for sw in SQL_WORDS:
                if sw.startswith(w.upper()) and sw != w.upper():
                    words.add(sw)
        for w in sorted(words):
            start_position = -len(word_before_cursor)
            yield Completion(w, start_position=start_position)


completer = SqlCompleter()
