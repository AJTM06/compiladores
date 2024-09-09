def t_error(t):
    print ("Caracter desconocido '%s'"%t.value[0])
    t.lexer.skip(1)
