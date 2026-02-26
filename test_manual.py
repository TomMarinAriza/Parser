from rich import print
from rich.table import Table
from rich.console import Console
from lex import Lexer

def test_manual_keywords():
    """Test manual de keywords B-Minor"""
    console = Console()
    lexer = Lexer()
    
    print("\n[bold blue]TEST MANUAL: Keywords Reservadas B-Minor[/bold blue]")
    print("-" * 50)
    
    source = "constant print return break continue if else while function true false"
    tokens = list(lexer.tokenize(source))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Token", style="cyan")
    table.add_column("Tipo", style="green")
    table.add_column("Valor", style="yellow")
    table.add_column("Linea", style="red")
    
    for token in tokens:
        table.add_row(str(token.index + 1), token.type, str(token.value), str(token.lineno))
    
    console.print(table)
    return len(tokens)

def test_manual_operators():
    """Test manual de operadores"""
    console = Console()
    lexer = Lexer()
    
    print("\n[bold blue]TEST MANUAL: Operadores B-Minor[/bold blue]")
    print("-" * 40)
    
    source = "+ - * / ^ < <= > >= == != && || ! = ;"
    tokens = list(lexer.tokenize(source))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Operador", style="cyan")
    table.add_column("Token", style="green")
    table.add_column("Descripcion", style="yellow")
    
    descriptions = {
        'PLUS': 'Suma',
        'MINUS': 'Resta',
        'TIMES': 'Multiplicacion',
        'DIVIDE': 'Division',
        'GROW': 'Exponenciacion',
        'LT': 'Menor que',
        'LE': 'Menor o igual',
        'GT': 'Mayor que', 
        'GE': 'Mayor o igual',
        'EQ': 'Igual',
        'NE': 'No igual',
        'LAND': 'Y logico',
        'LOR': 'O logico',
        'LNOT': 'No logico',
        'ASSIGN': 'Asignacion',
        'SEMI': 'Punto y coma'
    }
    
    for token in tokens:
        desc = descriptions.get(token.type, 'Desconocido')
        table.add_row(str(token.value), token.type, desc)
    
    console.print(table)
    return len(tokens)

def test_manual_literals():
    """Test manual de literales"""
    console = Console()
    lexer = Lexer()
    
    print("\n[bold blue]TEST MANUAL: Literales B-Minor[/bold blue]")
    print("-" * 40)
    
    source = "123 3.14 .5 99. 'a' '\\n' '\\x41'"
    tokens = list(lexer.tokenize(source))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Literal", style="cyan")
    table.add_column("Tipo", style="green") 
    table.add_column("Valor Procesado", style="yellow")
    table.add_column("Descripcion", style="red")
    
    for i, token in enumerate(tokens):
        if token.type == 'ENTERO':
            desc = 'Numero entero decimal'
        elif token.type == 'FLOTANTE':
            desc = 'Numero de punto flotante'
        elif token.type == 'CHAR':
            desc = 'Caracter literal'
        else:
            desc = 'Otro tipo'
            
        table.add_row(
            str(source.split()[i]),
            token.type, 
            str(token.value),
            desc
        )
    
    console.print(table)
    return len(tokens)

def test_manual_programa_completo():
    """Test manual de programa B-Minor completo"""
    console = Console()
    lexer = Lexer()
    
    print("\n[bold blue]TEST MANUAL: Programa B-Minor Completo[/bold blue]")
    print("-" * 50)
    
    source = """
    function factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    """
    
    tokens = list(lexer.tokenize(source))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("No.", style="dim")
    table.add_column("Token", style="cyan", width=12)
    table.add_column("Valor", style="green")
    table.add_column("Linea", style="yellow")
    table.add_column("Posicion", style="red")
    
    for i, token in enumerate(tokens, 1):
        table.add_row(
            str(i),
            token.type,
            str(token.value),
            str(token.lineno),
            f"{token.index}-{token.end}"
        )
    
    console.print(table)
    return len(tokens)

def test_manual_errores():
    """Test manual de deteccion de errores"""
    console = Console()
    lexer = Lexer()
    
    print("\n[bold red]TEST MANUAL: Deteccion de Errores[/bold red]")
    print("-" * 45)
    
    print("\n[yellow]1. Caracter ilegal (@):[/yellow]")
    try:
        tokens = list(lexer.tokenize("valid @ token"))
        print(f"Tokens encontrados: {len(tokens)}")
    except Exception as e:
        print(f"Error capturado: {e}")
    
    print("\n[yellow]2. Constante de caracter sin terminar:[/yellow]")
    try:
        tokens = list(lexer.tokenize("'sin_cerrar"))
        print(f"Tokens encontrados: {len(tokens)}")
    except Exception as e:
        print(f"Error capturado: {e}")
    
    print("\n[yellow]3. Comentario sin terminar:[/yellow]")
    try:
        tokens = list(lexer.tokenize("/* comentario sin cerrar"))
        print(f"Tokens encontrados: {len(tokens)}")
    except Exception as e:
        print(f"Error capturado: {e}")

def run_all_manual_tests():
    """Ejecutar todos los tests manuales"""
    print("[bold green]SUITE DE TESTS MANUALES - LEXER B-MINOR[/bold green]")
    print("=" * 60)
    
    total_tokens = 0
    
    total_tokens += test_manual_keywords()
    total_tokens += test_manual_operators()  
    total_tokens += test_manual_literals()
    total_tokens += test_manual_programa_completo()
    
    test_manual_errores()
    
    print(f"\n[bold cyan]TOTAL DE TOKENS PROCESADOS: {total_tokens}[/bold cyan]")
    print("\n[green]Todos los tests manuales completados exitosamente![/green]")

if __name__ == '__main__':
    run_all_manual_tests()