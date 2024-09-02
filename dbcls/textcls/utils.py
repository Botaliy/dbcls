

def get_current_sql_expression(document):
    start = document.cursor_position
    text = document.text
    while start > 0 and text[start-1] not in (';', '\n'):
        start -= 1
    end = document.cursor_position
    while end < len(text) and text[end] not in (';', '\n'):
        end += 1
    
    return start, end


def get_current_sql_command_lines(lines, current_line_idx):
    start_idx = current_line_idx
    while start_idx > 0:
        line = lines[start_idx].strip()
        if line == "" or line.endswith(";"):
            start_idx += 1
            break
        start_idx -= 1
    if start_idx < current_line_idx and lines[start_idx].strip().endswith(";"):
        start_idx += 1

    end_idx = current_line_idx
    while end_idx < len(lines) - 1:
        line = lines[end_idx].strip()
        if line in ["", ' '] or line.endswith(";"):
            break
        end_idx += 1
    
    if not lines[end_idx].strip().endswith(";"):
        end_idx += 1

    return start_idx, end_idx