def t_NUMENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t