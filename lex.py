from rich import print
import sly


class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        ARRAY, BOOLEAN, CHAR, CONSTANT, BREAK, CONTINUE, ELSE, FLOAT, FOR,
        FUNCTION, IF, INTEGER, PRINT, RETURN, WHILE, STRING, VOID,

        # Operadores de Relacion
        LT, LE, GT, GE, EQ, NE, LAND, LOR, LNOT, INC, DEC,

        # Operadores de Asignacion
        ADDEQ , SUBEQ, MULEQ, DIVEQ, MODEQ,

        #Operadores Aritmeticos
        PLUS, MINUS, TIMES, DIVIDE, MOD, GROW,

        #Simbolos varios
        ASSIGN, SEMI, LPAREN ,RPAREN, LBRACE, RBRACE, COMA, DEREF,

        # Identidicador
        ID,

        # Literales
        INTEGER_LITERAL, FLOAT_LITERAL, CHAR_LITERAL,
        STRING_LITERAL, TRUE, FALSE,
    }

    # Operadores Aritméticos
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    GROW = r'\^'

    # Operadores de Relación
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    EQ = r'=='
    NE = r'!='
    LAND = r'&&'
    LOR = r'\|\|'
    LNOT = r'!'
    INC = r'\+\+'
    DEC = r'--'

    # Operadores de Asignación
    ADDEQ = r'\+='
    SUBEQ = r'-='
    MULEQ = r'\*='
    DIVEQ = r'/='
    MODEQ = r'%='

    # Símbolos varios
    ASSIGN = r'='
    SEMI = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COMA = r','
    DEREF = r'`'
    
    # literals = '+-*/%^=,.:()[]{}'  # Comentado porque ahora usamos tokens específicos

    # Patrones a Ignorar
    ignore = ' \t\r'        # Whitespace

    @_(r'//.*\n')
    def ignore_cppcomment(self, t):
        self.lineno += 1
    
    @_(r'/\*(.|\n)*\*/')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Definición de Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Literales
    @_(r'\d+\.\d+')
    def FLOAT_LITERAL(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTEGER_LITERAL(self, t):
        t.value = int(t.value)
        return t

    @_(r"'([^'\\]|\\.)'")
    def CHAR_LITERAL(self, t):
        # Maneja caracteres literales incluyendo secuencias de escape
        t.value = t.value[1:-1]  # Quita las comillas
        return t

    @_(r'"([^"\\]|\\.)*"')
    def STRING_LITERAL(self, t):
        # Maneja cadenas literales incluyendo secuencias de escape
        t.value = t.value[1:-1]  # Quita las comillas
        return t

    # keywords
    ID['array']   = ARRAY
    ID['boolean'] = BOOLEAN
    ID['char']    = CHAR
    ID['else']    = ELSE
    ID['false']   = FALSE
    ID['float']   = FLOAT
    ID['for']     = FOR
    ID['function']= FUNCTION
    ID['if']      = IF
    ID['integer'] = INTEGER
    ID['print']   = PRINT
    ID['return']  = RETURN
    ID['string']  = STRING
    ID['void']    = VOID
    ID['while']   = WHILE
    ID['true']    = TRUE
    ID['break']   = BREAK
    ID['continue'] = CONTINUE
    ID['constant']   = CONSTANT

    def errorCharacter(self, t):
        # Manejo de errores
        print(f"{self.lineno}: Carácter '{t.value[0]}' ilegal")
        self.index += 1
    
    @_(r'/\*([^*]|\*(?!/))*$')
    def errorComments(self, t):
        print(f"{self.lineno}: Comentario sin cerrar")

def tokenize(source):
    lex = Lexer()

    for tok in lex.tokenize(source):
        print(tok)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python lexer.py filename')
        raise SystemExit
    
    txt = open(sys.argv[1], encoding='utf-8').read()
    tokenize(txt)
