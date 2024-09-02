from prompt_toolkit.styles import Style
from pygments.token import Keyword, Name, Comment, String, Number


class CustomSQLStyle(Style):
    """
    Кастомный стиль для SQL ключевых слов.
    """
    default_style = ""

    styles = {
        Keyword: 'bold #ff00ff',  # Измените цвет ключевых слов SQL (например, розовый и жирный)
        Name: '#00ff00',          # Измените цвет имен
        Comment: 'italic #888888', # Комментарии курсивом и серым цветом
        String: '#ff0000',        # Цвет строк (например, красный)
        Number: '#0000ff',        # Цвет чисел (например, синий)
    }