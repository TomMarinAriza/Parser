from rich import print
import sly


class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas B-Minor+
        CONSTANT, PRINT, RETURN, BREAK, CONTINUE, IF, ELSE, WHILE, 
        FUNCTION, TRUE, FALSE, CLASS,

        # Operadores de Relacion
        LT, LE, GT, GE, EQ, NE, LAND, LOR, LNOT,

        # Operadores Aritmeticos
        PLUS, MINUS, TIMES, DIVIDE, GROW,

        # Simbolos varios
        ASSIGN, SEMI, LPAREN, RPAREN, LBRACE, RBRACE, COMA, DEREF, LBRACKET, RBRACKET, COLON,

        # Identificador
        ID,

        # Literales
        INTEGER_LITERAL, FLOAT_LITERAL, CHAR_LITERAL, STRING_LITERAL,
    }

    # Patrones a Ignorar
    ignore = ' \t\r'        

    @_(r'//[^\n]*\n?')
    def ignore_cppcomment(self, t):
        self.lineno += 1
   
    @_(r'/\*(.|\n)*?\*/')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Operadores de Relación de dos caracteres 
    LE = r'<='
    GE = r'>='
    EQ = r'=='
    NE = r'!='
    LAND = r'&&'
    LOR = r'\|\|'

    # Operadores de Relacion un caracter
    LT = r'<'
    GT = r'>'
    LNOT = r'!'

    # Operadores Aritméticos
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    GROW = r'\^'

    # Símbolos varios
    ASSIGN = r'='
    SEMI = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    COMA = r','
    DEREF = r'`'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    COLON = r':'

    # Literales 
    @_(r'\d+\.\d*|\.\d+|\d+\.')
    def FLOAT_LITERAL(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTEGER_LITERAL(self, t):
        t.value = int(t.value)
        return t

    @_(r"'(\\x[0-9a-fA-F]{2}|\\[abefnrtv\\'\"\\]|[^'\\])'")
    def CHAR_LITERAL(self, t):
        # Maneja caracteres literales incluyendo secuencias de escape
        t.value = t.value[1:-1]  # Quita las comillas
        return t
    
    @_(r'"([^"\\]|\\.)*"')
    def STRING_LITERAL(self, t):
        # Maneja literales de cadena incluyendo secuencias de escape
        t.value = t.value[1:-1]  
        return t
    # Manejo de errores para literales de cadena sin terminar
    @_(r'\"([^\"\\\\]|\\\\.)*')
    def errorStringLiteral(self, t):
        print(f"[red]{self.lineno}: Literal de cadena sin terminación[/red]")
        self.lineno += t.value.count('\n')
    # Error específico: literal de carácter con más de 1 elemento
    @_(r"'([^'\\]|\\.){2,}'")
    def errorCharTooLong(self, t):
        print(f"[red]{self.lineno}: Literal de carácter con más de un elemento[/red]")

    # Manejo de errores para literales de caracteres sin terminar
    @_(r"'([^'\\]|\\.)*")
    def errorCharLiteral(self, t):
        print(f"[red]{self.lineno}: Constante de carácter sin terminación[/red]")

    # Definición de Tokens - Identificadores y palabras reservadas
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*') 
    def ID(self, t):
        keywords = {
            # Keywords B-Minor+
            'constant': 'CONSTANT',
            'print': 'PRINT',
            'return': 'RETURN',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'function': 'FUNCTION',
            'true': 'TRUE',
            'false': 'FALSE',
            'class': 'CLASS',
        }
        t.type = keywords.get(t.value, 'ID') 
        return t

    # Manejo de errores para comentarios sin terminar
    @_(r'/\*(.|\n)*')
    def errorComment(self, t):
        print(f"[red]{self.lineno}: Comentario sin terminación[/red]")
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"[red]{self.lineno}: Carácter '{t.value[0]}' ilegal[/red]")
        self.index += 1


# Pruebas unitarias
def tokenize(source):
    """Tokeniza el código fuente y muestra los tokens encontrados"""
    lexer = Lexer()
    for tok in lexer.tokenize(source):
        print(tok)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        try:
            txt = open(sys.argv[1], encoding='utf-8').read()
            tokenize(txt)
        except FileNotFoundError:
            print(f"[red]Error: Archivo '{sys.argv[1]}' no encontrado.[/red]")
            raise SystemExit(1)
    else: 
        print('Uso: python lex.py <archivo.txt>')
        print('Para ejecutar pruebas: python test_lexer.py')
        raise SystemExit(1)