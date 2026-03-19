# Analizador Léxico B-Minor+

## Descripción

Este proyecto implementa un analizador léxico (lexer) completo para el lenguaje B-Minor+. El lexer es responsable de convertir texto sin formato en símbolos reconocidos conocidos como tokens.

## Estructura actual del proyecto

- `lex.py`: analizador léxico con SLY.
- `parser.py`: analizador sintáctico (parser) con SLY que construye un AST en forma de diccionarios/listas.
- `errors.py`: utilidades compartidas para reporte y conteo de errores.
- `samples/`: contiene todos los archivos de ejemplo `good*.bminor` y `bad*.bminor`.

### Ejecutar parser

```bash
python parser.py samples/good7.bminor
```

## Características Implementadas

### Keywords Reservadas
- `constant`: Declara una constante
- `print`: Instrucción de impresión
- `return`: Retorno de función
- `break`: Salir de un bucle
- `continue`: Continuar con la siguiente iteración
- `if`: Condicional
- `else`: Alternativa del condicional
- `while`: Bucle
- `function`: Declaración de función
- `true`: Valor booleano verdadero
- `false`: Valor booleano falso

### Identificadores
- **ID**: Texto que comienza con una letra o '_', seguido de cualquier número de letras, dígitos o guiones bajos
- **Ejemplos**: `abc`, `ABC`, `abc123`, `_abc`, `a_b_c`

### Literales
- **ENTERO**: Números enteros decimales (ej: `123`, `0`, `456`)
- **FLOTANTE**: Números de punto flotante en formato:
  - `1.234` (decimal completo)
  - `.1234` (decimal que empieza con punto)
  - `1234.` (decimal que termina con punto)
- **CHAR**: Caracteres literales que soportan:
  - Caracteres simples: `'a'`
  - Secuencias de escape: `'\n'`, `'\''`
  - Valores hexadecimales: `'\x41'`

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`, `^`
- **Relacionales**: `<`, `<=`, `>`, `>=`, `==`, `!=`
- **Lógicos**: `&&`, `||`, `!`

### Símbolos Varios
- `=` (ASSIGN): Asignación
- `;` (SEMI): Punto y coma
- `(` `)` (LPAREN, RPAREN): Paréntesis
- `{` `}` (LBRACE, RBRACE): Llaves
- `,` (COMA): Coma
- `` ` `` (DEREF): Comilla invertida

### Manejo de Comentarios
- **Línea simple**: `//` - Ignora el resto de la línea
- **Bloque**: `/* ... */` - Ignora un bloque (no permite anidación)

### Manejo de Errores
El lexer reconoce y reporta los siguientes errores:
- **Carácter ilegal**: `lineno: Carácter 'c' ilegal`
- **Constante de carácter sin terminación**: `lineno: Constante de carácter sin terminación`
- **Comentario sin terminación**: `lineno: Comentario sin terminación`

## Implementación Técnica

### Tecnologías Utilizadas
- **Python**: Lenguaje de implementación
- **SLY (Sly Lex-Yacc)**: Biblioteca para análisis léxico y sintáctico
- **Rich**: Biblioteca para output colorizado en terminal

### Estructura del Código
1. **Clase Lexer**: Hereda de `sly.Lexer` y define todos los tokens
2. **Expresiones Regulares**: Patrones para reconocer cada tipo de token
3. **Manejo de Precedencia**: Los operadores de múltiples caracteres se definen antes que los de un carácter
4. **Funciones de Token**: Procesamiento especial para literales y keywords
5. **Manejo de Errores**: Funciones específicas para diferentes tipos de errores

### Orden de Precedencia en Tokens
Es crucial mantener el orden correcto en las definiciones:
1. Operadores de múltiples caracteres (`<=`, `>=`, `==`, `!=`, `&&`, `||`)
2. Operadores de un carácter (`<`, `>`, `!`)
3. Literales flotantes (más específicos primero)
4. Literales enteros
5. Identificadores y keywords

## Sistema de Pruebas

### Tests Unitarios (Automatizados)

Se implementaron **26 pruebas unitarias** usando el framework **unittest** de Python organizadas en tres categorias:

#### Tabla 1: Pruebas Funcionales (TestLexer) - 18 Tests

| No. | Metodo de Test | Descripcion | Tokens Probados | Estado |
|-----|----------------|-------------|-----------------|--------|
| 1 | test_keywords_reservadas | Keywords reservadas de B-Minor | CONSTANT, PRINT, RETURN, etc. | PASS |
| 2 | test_identificadores_validos | Identificadores correctos | ID | PASS |
| 3 | test_literales_enteros | Numeros enteros (123, 0, 456) | ENTERO | PASS |
| 4 | test_literales_flotantes | Numeros flotantes (1.234, .5, 99.) | FLOTANTE | PASS |
| 5 | test_literales_caracteres | Caracteres ('a', '\\n', '\\x41') | CHAR | PASS |
| 6 | test_operadores_relacionales | <, <=, >, >=, ==, !=, &&, ||, ! | LT, LE, GT, GE, EQ, NE, LAND, LOR, LNOT | PASS |
| 7 | test_operadores_aritmeticos | +, -, *, /, ^ | PLUS, MINUS, TIMES, DIVIDE, GROW | PASS |
| 8 | test_simbolos_varios | =, ;, (, ), {, }, ,, ` | ASSIGN, SEMI, LPAREN, RPAREN, etc. | PASS |
| 9 | test_comentarios_ignorados | //, /* */ | (ignorados) | PASS |
| 10 | test_declaracion_funcion | function suma(a, b) { return a + b; } | FUNCTION, ID, LPAREN, etc. | PASS |
| 11 | test_condicionales_con_operadores | if (x <= 10 && y >= 5) { print x; } | IF, LPAREN, ID, LE, etc. | PASS |
| 12 | test_bucles_control_flujo | while (true) { if break; else continue; } | WHILE, TRUE, IF, BREAK, CONTINUE | PASS |
| 13 | test_variables_constantes | constant PI = 3.14159; x = 'A'; | CONSTANT, ID, ASSIGN, FLOTANTE | PASS |
| 14 | test_expresiones_complejas | result = (a * b) + (c / d) ^ 2; | ID, LPAREN, TIMES, PLUS, GROW | PASS |
| 15 | test_comparaciones_logica | if (x != y || a == b) { result = !false; } | IF, NE, LOR, EQ, LNOT, FALSE | PASS |
| 16 | test_valores_literales | Verificacion de valores procesados | 123 → 123, 3.14 → 3.14 | PASS |
| 17 | test_precedencia_operadores | <=, >=, ==, != reconocidos correctamente | LE, GE, EQ, NE | PASS |
| 18 | test_espacios_en_blanco | Manejo de espacios, tabs, returns | (ignorados correctamente) | PASS |

#### Tabla 2: Pruebas de Manejo de Errores (TestLexerErrorHandling) - 3 Tests

| No. | Metodo de Test | Input de Prueba | Error Esperado | Resultado |
|-----|----------------|-----------------|----------------|-----------|
| 19 | test_caracter_ilegal | "valid @ more" | Caracter '@' ilegal | ERROR DETECTADO |
| 20 | test_constante_caracter_sin_terminar | "'a" | Constante de caracter sin terminacion | ERROR DETECTADO |
| 21 | test_comentario_sin_terminar | "/* comentario sin cerrar" | Comentario sin terminacion | ERROR DETECTADO |

#### Tabla 3: Pruebas de Deteccion de Errores (TestLexerIntentionalFailures) - 5 Tests

| No. | Metodo de Test | Input Erroneo | Tokens Esperados (Incorrectos) | Resultado Esperado |
|-----|----------------|---------------|--------------------------------|-------------------|
| 22 | test_keyword_inexistente_DEBERIA_FALLAR | "for class import" | FOR, CLASS, IMPORT | FAIL (keywords no existen en B-Minor) |
| 23 | test_operador_inexistente_DEBERIA_FALLAR | "x ++ y" | ID, INCREMENT, ID | FAIL (++ no existe en B-Minor) |
| 24 | test_literal_invalido_DEBERIA_FALLAR | "'abc'" | CHAR | FAIL (char literal debe ser un caracter) |
| 25 | test_numero_flotante_mal_formado_DEBERIA_FALLAR | "12..34" | FLOTANTE | FAIL (dos puntos consecutivos) |
| 26 | test_orden_tokens_incorrecto_DEBERIA_FALLAR | "if (x > 5) print x;" | PRINT, IF, LPAREN, ID | FAIL (orden incorrecto intencionalmente) |

### Tests Manuales (Visuales)

#### Tabla 4: Tests Manuales Disponibles

| Funcion | Descripcion | Que Prueba | Salida |
|---------|-------------|------------|---------|
| test_manual_keywords() | Keywords reservadas con tabla visual | 11 keywords de B-Minor | Tabla colorizada |
| test_manual_operators() | Operadores con descripciones | 16 operadores con significado | Tabla con descripciones |
| test_manual_literals() | Literales con valores procesados | Enteros, flotantes, caracteres | Tabla con valores |
| test_manual_programa_completo() | Programa factorial completo | Tokenizacion de programa real | Tabla detallada |
| test_manual_errores() | Demostracion de errores | 3 tipos de errores | Mensajes de error |


## Proceso de Desarrollo

### 1. Análisis de Requisitos
- Estudio detallado de las especificaciones de B-Minor+
- Identificación de todos los tokens requeridos
- Definición de patrones de expresiones regulares

### 2. Implementación Base
- Configuración de la clase Lexer con SLY
- Definición de tokens básicos
- Implementación de reconocimiento de keywords

### 3. Manejo de Literales
- Implementación de reconocimiento de enteros
- Soporte para flotantes en múltiples formatos
- Manejo de caracteres con secuencias de escape

### 4. Operadores y Símbolos
- Implementación de operadores aritméticos
- Soporte para operadores relacionales y lógicos
- Definición de símbolos especiales

### 5. Manejo de Comentarios
- Implementación de comentarios de línea
- Soporte para comentarios de bloque
- Manejo correcto de conteo de líneas

### 6. Manejo de Errores
- Detección de caracteres ilegales
- Manejo de literales sin terminar
- Detección de comentarios sin cerrar

### 7. Pruebas Unitarias
- Desarrollo de suite de pruebas comprehensiva
- Verificación de todos los casos edge
- Validación de expresiones regulares

### 8. Optimización y Refinamiento
- Ajuste del orden de precedencia
- Optimización de expresiones regulares
- Mejora en mensajes de error

## Consideraciones Técnicas

### Expresiones Regulares Clave
- **Flotantes**: `r'\d+\.\d*|\.\d+|\d+\.'` - Cubre todos los formatos
- **Caracteres**: `r"'(\\x[0-9a-fA-F]{2}|\\[nt'\\]|[^'\\])'"` - Incluye escapes
- **Comentarios**: `r'/\*(.|\n)*?\*/'` - Non-greedy para evitar problemas

### Manejo de Estados
- El lexer mantiene estado de línea actual para reportes de error
- Ignora automáticamente whitespace y newlines
- Procesa comentarios sin incluirlos en el stream de tokens
