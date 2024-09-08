import ply.lex as lex
import ply.yacc as yacc
import os

#Errores
#errores_lexicos = []
#errores_desconocidos = []

tokens = [
    'VARIABLE',
    'NUMENTERO',
    'NUMDECIMAL',
    'PALABRA',
    #'FUNCION',
    #'SI',
    #'SINO',
   # 'IMPRIMIR',
    #'DEVOLVER',
    #'MIENTRAS',
    #'ROMPER',
    'OP_MAS',
    'OP_MENOS',
    'OP_MULTI',
    'OP_DIV',
    'OP_IGUAL',
    'SIGMENOR',
    'SIGMAYOR', 
    'SIGMAYORIGUAL',
    'SIGMENORIGUAL',
    'SIGDOBLEIGUAL',
    'DIFERENTE', 
    'PUNTO',
    'COMA', 
    'PUNTOCOMA', 
    'DOSPUNTOS', 
    'COMILLASIMPLE',
    'COMILLADOBLE',
    'PARIN', 
    'PARFIN',
    'LLAIN', 
    'LLAFIN',
    'CORIN',
    'CORFIN'

]

palabras_reservadas = {
    'si':'SI',
    'sino':'SINO',
    'mientras':'MIENTRAS',
    'para':'PARA',
    'funcion':'FUNCION',
    'retorna':'RETORNAR',
    'verdadero':'VERDADERO',
    'falso':'FALSO',
    'o':'O',#OPERADOR LOGICO OR
    'y':'Y',#OPERADOR LOGICO AND
    #'':'',
    'imprimir':'IMPRIMIR',
    'entero':'ENTERO',
    'decimal':'DECIMAL',
    'cadena':'CADENA',
    'bolean':'BOLEAN'
}

tokens = tokens+list(palabras_reservadas.values())

#precedencias para poder definir funciones 
precedence = (
    ('left', 'O'),
    ('left', 'Y'),
    ('left', 'OP_MAS', 'OP_MENOS'),
    ('left', 'OP_MULTI', 'OP_DIV'),
)

t_ignore = ' \t'


#tokens simples
t_OP_MAS = r'\+'
t_OP_MENOS = r'\-'
t_OP_MULTI = r'\*'
t_OP_DIV = r'/'
t_OP_IGUAL = r'='
t_SIGMENOR = r'<'
t_SIGMAYOR = r'>'
t_SIGMAYORIGUAL = r'>='
t_SIGMENORIGUAL = r'<='
t_SIGDOBLEIGUAL = r'=='
t_DIFERENTE = r'!='
t_PUNTO = r'\.'
t_COMA = r'\,'
t_PUNTOCOMA = r'\;'
t_DOSPUNTOS = r'\:'
t_COMILLASIMPLE = r'\''
t_COMILLADOBLE = r'\"'
t_PARIN = r'\('
t_PARFIN = r'\)'
t_LLAIN = r'\{'
t_LLAFIN = r'\}'
t_CORIN = r'\['
t_CORFIN = r'\]'


def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in palabras_reservadas:
        t.type = palabras_reservadas[t.value.lower()]
    return t

def t_NUMENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NUMDECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_PALABRA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMENTARIO(t):
    r'\#.*'
    pass

def t_COMENTARIO_BLOQUE(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    pass

def t_error(t):
    print ("Caracter desconocido '%s'"%t.value[0])
    t.lexer.skip(1)

# Definir reglas de la gramática
def p_programa(p):
    '''programa : lista_instrucciones'''
    p[0] = p[1]

def p_lista_instrucciones(p):
    '''lista_instrucciones : lista_instrucciones instruccion
                           | instruccion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Definir reglas para asignaciones
def p_instruccion_asignacion(p):
    '''instruccion : VARIABLE OP_IGUAL expresion PUNTOCOMA'''
    p[0] = ('asignacion', p[1], p[3])

# Definir reglas para expresiones
def p_expresion(p):
    '''expresion : expresion OP_MAS termino
                 | expresion OP_MENOS termino
                 | termino'''
    if len(p) == 4:
        p[0] = ('operacion', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_termino(p):
    '''termino : NUMENTERO
               | NUMDECIMAL
               | VARIABLE
               | PALABRA'''
    p[0] = p[1]

# Definir la estructura de control "si"
def p_instruccion_si(p):
    '''instruccion : SI PARIN condicion PARFIN LLAIN lista_instrucciones LLAFIN
                   | SI PARIN condicion PARFIN LLAIN lista_instrucciones LLAFIN SINO LLAIN lista_instrucciones LLAFIN'''
    if len(p) == 8:
        p[0] = ('si', p[3], p[6])
    else:
        p[0] = ('si_sino', p[3], p[6], p[10])

# Definir la estructura de control "mientras"
def p_instruccion_mientras(p):
    '''instruccion : MIENTRAS PARIN condicion PARFIN LLAIN lista_instrucciones LLAFIN'''
    p[0] = ('mientras', p[3], p[6])

# Definir una condición (operadores lógicos y relacionales)
def p_condicion(p):
    '''condicion : expresion SIGDOBLEIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion SIGMENOR expresion
                 | expresion SIGMAYOR expresion
                 | expresion SIGMENORIGUAL expresion
                 | expresion SIGMAYORIGUAL expresion
                 | expresion O expresion
                 | expresion Y expresion'''
    p[0] = ('condicion', p[2], p[1], p[3])

# Manejo de errores
def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")

# Crear el parser
parser = yacc.yacc()

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
            #print(tok)
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



'''def analizar_archivo(archivo):
    with open(archivo, 'r', encoding='utf-8') as archivotxt:
        data = archivotxt.read()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)'''
   
#Inicializar el lexer
lexer = lex.lex()

#archivo = 'hola_mundo.txt'
analizar_archivo('archivos/holamundo.txt')
#analizar_archivo('C:/Users/JOSE LUIS/Documents/1. Universidad/ULS/Compiladores/Proyecto_Compiladores/Analizador Lexico/hola_mundo.txt')



#data = "Hola 67 12 0.3"

#lexer.input(data)
