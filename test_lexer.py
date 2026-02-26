import unittest
from rich import print
from lex import Lexer


class TestLexer(unittest.TestCase):
    """Clase de pruebas unitarias para el lexer de B-Minor"""

    def setUp(self):
        """Configuracion inicial para cada test"""
        self.lexer = Lexer()

    def get_token_types(self, source):
        """Funcion auxiliar para obtener los tipos de tokens"""
        return [t.type for t in self.lexer.tokenize(source)]

    def test_keywords_reservadas(self):
        """Test 1: Verificar keywords reservadas"""
        source = "constant print return break continue if else while function true false"
        expected = ['CONSTANT', 'PRINT', 'RETURN', 'BREAK', 'CONTINUE', 'IF', 'ELSE', 'WHILE', 'FUNCTION', 'TRUE', 'FALSE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Keywords reservadas no coinciden")

    def test_identificadores_validos(self):
        """Test 2: Verificar identificadores validos"""
        source = "abc ABC abc123 _abc a_b_c"
        expected = ['ID', 'ID', 'ID', 'ID', 'ID']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Identificadores validos no coinciden")

    def test_literales_enteros(self):
        """Test 3: Verificar literales enteros"""
        source = "123 0 456 999"
        expected = ['ENTERO', 'ENTERO', 'ENTERO', 'ENTERO']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Literales enteros no coinciden")

    def test_literales_flotantes(self):
        """Test 4: Verificar literales flotantes"""
        source = "1.234 .1234 1234. 0.0 99.99"
        expected = ['FLOTANTE', 'FLOTANTE', 'FLOTANTE', 'FLOTANTE', 'FLOTANTE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Literales flotantes no coinciden")

    def test_literales_caracteres(self):
        """Test 5: Verificar literales de caracteres"""
        source = "'a' '\\n' '\\x41' '\\''"
        expected = ['CHAR', 'CHAR', 'CHAR', 'CHAR']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Literales de caracteres no coinciden")

    def test_operadores_relacionales(self):
        """Test 6: Verificar operadores relacionales"""
        source = "< <= > >= == != && || !"
        expected = ['LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'LAND', 'LOR', 'LNOT']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Operadores relacionales no coinciden")

    def test_operadores_aritmeticos(self):
        """Test 7: Verificar operadores aritmeticos"""
        source = "+ - * / ^"
        expected = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'GROW']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Operadores aritmeticos no coinciden")

    def test_simbolos_varios(self):
        """Test 8: Verificar simbolos varios"""
        source = "= ; ( ) { } , `"
        expected = ['ASSIGN', 'SEMI', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMA', 'DEREF']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Simbolos varios no coinciden")

    def test_comentarios_ignorados(self):
        """Test 9: Verificar que los comentarios son ignorados"""
        source = "codigo // este es un comentario\nmas_codigo /* multi-linea \n comentario */ fin"
        expected = ['ID', 'ID', 'ID']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Los comentarios no se ignoran correctamente")

    def test_declaracion_funcion(self):
        """Test 10: Verificar declaracion de funcion completa"""
        source = "function suma(a, b) { return a + b; }"
        expected = ['FUNCTION', 'ID', 'LPAREN', 'ID', 'COMA', 'ID', 'RPAREN', 'LBRACE', 'RETURN', 'ID', 'PLUS', 'ID', 'SEMI', 'RBRACE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Declaracion de funcion no coincide")

    def test_condicionales_con_operadores(self):
        """Test 11: Verificar condicionales con operadores"""
        source = "if (x <= 10 && y >= 5) { print x; }"
        expected = ['IF', 'LPAREN', 'ID', 'LE', 'ENTERO', 'LAND', 'ID', 'GE', 'ENTERO', 'RPAREN', 'LBRACE', 'PRINT', 'ID', 'SEMI', 'RBRACE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Condicionales con operadores no coinciden")

    def test_bucles_control_flujo(self):
        """Test 12: Verificar bucles y control de flujo"""
        source = "while (true) { if (condition) break; else continue; }"
        expected = ['WHILE', 'LPAREN', 'TRUE', 'RPAREN', 'LBRACE', 'IF', 'LPAREN', 'ID', 'RPAREN', 'BREAK', 'SEMI', 'ELSE', 'CONTINUE', 'SEMI', 'RBRACE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Bucles y control de flujo no coinciden")

    def test_variables_constantes(self):
        """Test 13: Verificar variables y constantes"""
        source = "constant PI = 3.14159; x = 'A';"
        expected = ['CONSTANT', 'ID', 'ASSIGN', 'FLOTANTE', 'SEMI', 'ID', 'ASSIGN', 'CHAR', 'SEMI']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Variables y constantes no coinciden")

    def test_expresiones_complejas(self):
        """Test 14: Verificar expresiones complejas"""
        source = "result = (a * b) + (c / d) ^ 2;"
        expected = ['ID', 'ASSIGN', 'LPAREN', 'ID', 'TIMES', 'ID', 'RPAREN', 'PLUS', 'LPAREN', 'ID', 'DIVIDE', 'ID', 'RPAREN', 'GROW', 'ENTERO', 'SEMI']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Expresiones complejas no coinciden")

    def test_comparaciones_logica(self):
        """Test 15: Verificar comparaciones y logica"""
        source = "if (x != y || a == b) { result = !false; }"
        expected = ['IF', 'LPAREN', 'ID', 'NE', 'ID', 'LOR', 'ID', 'EQ', 'ID', 'RPAREN', 'LBRACE', 'ID', 'ASSIGN', 'LNOT', 'FALSE', 'SEMI', 'RBRACE']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Comparaciones y logica no coinciden")

    def test_valores_literales(self):
        """Test 16: Verificar valores de literales"""
        tokens = list(self.lexer.tokenize("123 3.14 'A'"))
        
        # Verificar que los valores sean correctos
        self.assertEqual(tokens[0].value, 123, "Valor del entero incorrecto")
        self.assertEqual(tokens[1].value, 3.14, "Valor del flotante incorrecto")
        self.assertEqual(tokens[2].value, "A", "Valor del caracter incorrecto")

    def test_precedencia_operadores(self):
        """Test 17: Verificar precedencia de operadores"""
        # Los operadores de dos caracteres deben tener precedencia sobre los de uno
        source = "<= >= == != && ||"
        expected = ['LE', 'GE', 'EQ', 'NE', 'LAND', 'LOR']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Precedencia de operadores incorrecta")

    def test_espacios_en_blanco(self):
        """Test 18: Verificar manejo de espacios en blanco"""
        source = "  \t\r  if   \t  (  \r  x  \n  )  "
        expected = ['IF', 'LPAREN', 'ID', 'RPAREN']
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Manejo de espacios en blanco incorrecto")


class TestLexerErrorHandling(unittest.TestCase):
    """Clase de pruebas para manejo de errores del lexer"""

    def setUp(self):
        """Configuracion inicial para cada test"""
        self.lexer = Lexer()

    def test_caracter_ilegal(self):
        """Test 19: Manejo de caracteres ilegales"""
        # El lexer debe manejar caracteres ilegales llamando a error()
        # En lugar de hacer crash, debe continuar procesando
        source = "valid @ more"
        tokens = list(self.lexer.tokenize(source))
        # Debe encontrar al menos el primer token valido
        self.assertTrue(len(tokens) >= 1, "El lexer debe seguir funcionando despues de un error")
        self.assertEqual(tokens[0].type, 'ID', "Primer token debe ser valido")

    def test_constante_caracter_sin_terminar(self):
        """Test 20: Constante de caracter sin terminacion"""
        # Esto debe activar la funcion errorCharLiteral
        source = "'a"
        tokens = list(self.lexer.tokenize(source))
        # El lexer debe manejar el error y continuar
        self.assertIsInstance(tokens, list, "El lexer debe retornar una lista incluso con errores")

    def test_comentario_sin_terminar(self):
        """Test 21: Comentario sin terminacion"""  
        source = "/* comentario sin cerrar"
        tokens = list(self.lexer.tokenize(source))
        # El lexer debe manejar el error
        self.assertIsInstance(tokens, list, "El lexer debe manejar comentarios sin terminar")


class TestLexerIntentionalFailures(unittest.TestCase):
    """Clase para demostrar deteccion de errores - Tests que DEBEN FALLAR"""

    def setUp(self):
        """Configuracion inicial para cada test"""
        self.lexer = Lexer()

    def get_token_types(self, source):
        """Funcion auxiliar para obtener los tipos de tokens"""
        return [t.type for t in self.lexer.tokenize(source)]

    def test_keyword_inexistente_DEBERIA_FALLAR(self):
        """Test que DEBE fallar: Keyword inexistente en B-Minor"""
        source = "for class import"  # 'for', 'class', 'import' no existen en B-Minor
        # Este test DEBE fallar porque esperamos tokens que no existen
        expected = ['FOR', 'CLASS', 'IMPORT']  # Tokens que B-Minor NO reconoce
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Este test DEBE fallar - keywords no existen en B-Minor")

    def test_operador_inexistente_DEBERIA_FALLAR(self):
        """Test que DEBE fallar: Operador inexistente"""
        source = "x ++ y"  # ++ no existe en B-Minor
        # Este test DEBE fallar porque ++ no es un operador en B-Minor
        expected = ['ID', 'INCREMENT', 'ID']  # INCREMENT no existe en B-Minor
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Este test DEBE fallar - operador ++ no existe")

    def test_literal_invalido_DEBERIA_FALLAR(self):
        """Test que DEBE fallar: Literal mal formado"""
        source = "'abc'"  # Caracter literal con mas de un caracter
        # Este test DEBE fallar porque los char literales deben tener un solo caracter
        expected = ['CHAR']  # Esto no deberia ser reconocido como CHAR valido
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Este test DEBE fallar - literal char invalido")

    def test_numero_flotante_mal_formado_DEBERIA_FALLAR(self):
        """Test que DEBE fallar: Numero flotante mal formado"""
        source = "12..34"  # Dos puntos seguidos
        # Este test DEBE fallar porque el numero esta mal formado
        expected = ['FLOTANTE']  # No deberia reconocerse como flotante valido
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Este test DEBE fallar - numero mal formado")

    def test_orden_tokens_incorrecto_DEBERIA_FALLAR(self):
        """Test que DEBE fallar: Orden incorrecto de tokens esperados"""
        source = "if (x > 5) print x;"
        # Esperamos un orden INCORRECTO intencionalmente
        expected = ['PRINT', 'IF', 'LPAREN', 'ID']  # Orden totalmente incorrecto
        result = self.get_token_types(source)
        self.assertEqual(result, expected, "Este test DEBE fallar - orden incorrecto")


def run_all_tests():
    """Ejecuta todas las pruebas organizadas por categoria"""
    
    print("\n[bold cyan]SISTEMA DE PRUEBAS DEL LEXER B-MINOR[/bold cyan]")
    print("=" * 60)
    
    # Crear suite de pruebas exitosas
    loader = unittest.TestLoader()
    success_suite = unittest.TestSuite()
    
    # Anadir pruebas que deben pasar
    success_suite.addTests(loader.loadTestsFromTestCase(TestLexer))
    success_suite.addTests(loader.loadTestsFromTestCase(TestLexerErrorHandling))
    
    print("\n[green]PRUEBAS FUNCIONALES (Deben pasar):[/green]")
    print("-" * 40)
    success_runner = unittest.TextTestRunner(verbosity=1)
    success_result = success_runner.run(success_suite)
    
    # Ejecutar pruebas que deben fallar
    print(f"\n[red]PRUEBAS DE DETECCION DE ERRORES (Deben fallar):[/red]")
    print("-" * 50)
    
    failure_suite = loader.loadTestsFromTestCase(TestLexerIntentionalFailures)
    failure_runner = unittest.TextTestRunner(verbosity=2)
    failure_result = failure_runner.run(failure_suite)
    
    print(f"\n[yellow]RESUMEN DE EJECUCION:[/yellow]")
    print("-" * 30)
    print(f"Pruebas exitosas: {success_result.testsRun - len(success_result.failures) - len(success_result.errors)}")
    print(f"Errores detectados correctamente: {len(failure_result.failures) + len(failure_result.errors)}")
    print(f"Total de pruebas ejecutadas: {success_result.testsRun + failure_result.testsRun}")


if __name__ == '__main__':
    # Si se ejecuta con argumento 'all', ejecuta todas las pruebas organizadas
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        run_all_tests()
    else:
        # Ejecutar solo las pruebas que deben pasar (comportamiento normal)
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTests(loader.loadTestsFromTestCase(TestLexer))
        suite.addTests(loader.loadTestsFromTestCase(TestLexerErrorHandling))
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)