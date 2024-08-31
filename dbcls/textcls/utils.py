

def get_current_sql_expression(document):
    start = document.cursor_position
    text = document.text
    while start > 0 and text[start-1] not in (';', '\n'):
        start -= 1
    end = document.cursor_position
    while end < len(text) and text[end] not in (';', '\n'):
        end += 1
    
    return text[start:end].strip()