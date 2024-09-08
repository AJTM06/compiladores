import ply.lex as lex
import ply.yacc as yacc
import os

tokens = [
    'VARIABLE',
    'NUMENTERO',
    'NUMDECIMAL',
    'PALABRA',
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
    'imprimir':'IMPRIMIR',
    'entero':'ENTERO',
    'decimal':'DECIMAL',
    'cadena':'CADENA',
    'boolean':'BOOLEANO'
}

tokens = tokens+list(palabras_reservadas.values())

t_ignore = ' \t'

#tokens operadores
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
