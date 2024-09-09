def t_NUMDECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
