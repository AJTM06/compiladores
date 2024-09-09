def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in palabras_reservadas:
        t.type = palabras_reservadas[t.value.lower()]
    return t