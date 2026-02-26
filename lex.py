from rich import print
import sly


class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas B-Minor+
        CONSTANT, PRINT, RETURN, BREAK, CONTINUE, IF, ELSE, WHILE, 
        FUNCTION, TRUE, FALSE,

        # Operadores de Relacion
        LT, LE, GT, GE, EQ, NE, LAND, LOR, LNOT,

        # Operadores Aritmeticos
        PLUS, MINUS, TIMES, DIVIDE, GROW,

        # Simbolos varios
        ASSIGN, SEMI, LPAREN, RPAREN, LBRACE, RBRACE, COMA, DEREF,

        # Identificador
        ID,

        # Literales
        ENTERO, FLOTANTE, CHAR,
    }

    # Patrones a Ignorar
    ignore = ' \t\r'        # Whitespace

    @_(r'//[^\n]*\n?')
    def ignore_cppcomment(self, t):
        self.lineno += 1
   
    @_(r'/\*(.|\n)*?\*/')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Operadores de Relación de dos caracteres (deben ir antes que los de un carácter)
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

    # Literales - Los patrones más específicos deben ir primero
    @_(r'\d+\.\d*|\.\d+|\d+\.')
    def FLOTANTE(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def ENTERO(self, t):
        t.value = int(t.value)
        return t

    @_(r"'(\\x[0-9a-fA-F]{2}|\\[nt'\\]|[^'\\])'")
    def CHAR(self, t):
        # Maneja caracteres literales incluyendo secuencias de escape
        t.value = t.value[1:-1]  # Quita las comillas
        return t

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
        }
        t.type = keywords.get(t.value, 'ID')  # Verifica si es una palabra reservada
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