def unpad(text):
    """Remove leading spaces from mutline string.

    >>> unpad('\\n  abc\\n    def\\n')
    'abc\\n  def'
    """
    rows = text.split('\n')
    # Find first non-empty row and remember number of leading spaces.
    for row in rows:
        n_leading_spaces = len(row) - len(row.lstrip())
        if n_leading_spaces > 0:
            break
    unpadded_rows = [row[n_leading_spaces:] for row in rows]
    return '\n'.join(unpadded_rows).strip()

