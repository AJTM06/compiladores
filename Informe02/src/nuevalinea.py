def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
