def analizar_archivo(archivos):
    try:
        with open(archivos, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
        lexer.input(data)
        #Aqui se almacenara los tokens
        diccionario=[]
        while True:
            tok = lexer.token()
            if not tok: 
                break
          
            diccionario.append({
                'Tipo de token ':tok.type,
                'Valor ':tok.value,
                'Esta en la linea ':tok.lineno,
                'En la posición ':tok.lexpos
            })
        for token in diccionario:
            print(token)

    except FileNotFoundError:
        print("Archivo no encontrado intente nuevamente")
   
#Inicializar el lexer
lexer = lex.lex()

analizar_archivo('archivos/holamundo.txt')