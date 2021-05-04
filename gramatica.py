#Importamos las librerías necesarias
import ply.yacc as yacc
import ply.lex as lex
import re

#Definimos los nombres de los tokens
tokens = (

    'ID',
    'IGUAL',
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'DECIMAL',
    'ENTERO',
)

#para definir los patrones de los tokens podemos agregar el prefijo 't_'
#PARA ESPECIFICAR UNA EXPRESION REGULAR DEBEMOS HACER USO DE 'r'
t_IGUAL = r'='
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'

#Otra forma de definir patrones es con funciones:

#Función para variables
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     return t

#Función para números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

#Función para números enteros
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

#Caracteres ignorados
t_ignore = " \t"

#Función para saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Se construye el analizador léxico
lexer = lex.lex()

#Asociación de operadores y precedencia
precedence = (
    ('left','MAS','MENOS'),
    ('left','POR','DIV'),
    ('right','UMENOS'),
    ('left','PARIZQ', 'PARDER'),
    )

#Definicion de la gramática

#Función para nuevas variables temporales
contTemp=1
contEtq=1
def newTemp():
    global contTemp
    cad = 'T'+str(contTemp)
    contTemp+=1
    return cad

#Función para nuevas etiquetas
def newEtq():
    global contEtq
    cad = 'L' + str(contEtq)
    contEtq+=1
    return cad

#Función para expresiones
def p_expresion_r_7(t):
    'r  :   e'

    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, str(t[1][1])]

#Función para expresiones binarias
def p_expresion_binaria(t):
    '''e  :     e   MAS     e
            |   e   MENOS   e
            |   e   POR     e
            |   e   DIV     e '''

    temp=newTemp()
    cad=str(t[1][1])+str(t[3][1])+temp+' = '+str(t[1][0])+' '+t[2]+' '+str(t[3][0])+'\r\n'
    t[0]=[temp, cad]

#Función para expresiones unarias
def p_expresion_unaria(t):
    '''e  :     MENOS   e   %prec   UMENOS'''
    temp=newTemp()
    t[0]=[temp, t[2][1]+temp+' = 0 - '+t[2][0]+'\r\n']

#Función para expresiones de agrupación (con paréntesis)
def p_expresion_agrupacion(t):
    'e : PARIZQ e PARDER'
    t[0]=t[2] #copio los list

#Función para las expresiones numéricas y variables
def p_expresion_number(t):
    '''e    : ENTERO
            | DECIMAL
            | ID'''
    t[0]=[t[1], ''] #creo un LIST de 2 elementos
    #print(t[0])

#Función para errores
def p_error(t):
    print("")

#Se construye el analizador
parser = yacc.yacc()
 
#Se lee el archivo .txt para las entradas
filename = "Entrada.txt"
textFile = open(filename, "r")
input = textFile.read()
cad=parser.parse(input)

#Se obtienen las cadenas en donde se guardaron las variables temporales generadas
salida=str(cad[2])
contador = str(contTemp-1)

#Se obtiene el nombre de la variable principal
filename = "Entrada.txt"
textFile = open(filename, "r")
for elemento in textFile:
    variable = re.findall("[a-zA-Z]*\s*=\s*", elemento)
    characters = "'[]"
    for x in range(len(characters)):
        variable = str(variable).replace(characters[x],"")

#Ahora escribimos la salida en codigo 3 direcciones
f = open ('salida.txt','w')
f.write(salida)
f.close()

#Se imprime la generación de código intermedio
print("\n-----GENERACIÓN DE CÓDIGO INTERMEDIO-----")
print("\nLa expresión es: "+input+"\n")
print("La representación intermedia en triplos es:\n")
archivo = open("salida.txt")
print(archivo.read().strip())
print("\n"+variable+"T"+contador+"\n")

#Se imprime los integrantes del equipo :)
print("Programa elaborado por:"+"\n"
        +"<<Mis Oy Cristina de Jesus>>"+"\n"
        +"<<Poot Can Gener Emmanuel>>"+"\n"
        +"<<Tun Tun José Natividad>>"+"\n"
        +"<<Uicab Balam Nanci Arai>>")