import logging

import sly
from rich import print

from errors import clear_errors, error, errors_detected
from lex import Lexer


def node(kind, **kwargs):
    return {"kind": kind, **kwargs}


class Parser(sly.Parser):
    log = logging.getLogger(__name__)
    log.setLevel(logging.ERROR)

    tokens = Lexer.tokens

    precedence = (
        ("right", "ASSIGN"),
        ("left", "LOR"),
        ("left", "LAND"),
        ("left", "EQ", "NE"),
        ("left", "LT", "LE", "GT", "GE"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "GROW"),
        ("right", "LNOT", "UMINUS", "UPLUS"),
    )

    @_('items')
    def prog(self, p):
        return node("Program", declarations=p.items)

    @_('empty')
    def prog(self, p):
        return node("Program", declarations=[])

    @_('items item')
    def items(self, p):
        return p.items + [p.item]

    @_('item')
    def items(self, p):
        return [p.item]

    @_('decl')
    @_('func_decl')
    @_('class_decl')
    @_('stmt')
    def item(self, p):
        return p[0]

    @_('CLASS ID LBRACE class_members RBRACE')
    def class_decl(self, p):
        return node("ClassDecl", name=p.ID, members=p.class_members, lineno=p.lineno)

    @_('CLASS ID LBRACE class_members RBRACE SEMI')
    def class_decl(self, p):
        return node("ClassDecl", name=p.ID, members=p.class_members, lineno=p.lineno)

    @_('class_members class_member')
    def class_members(self, p):
        return p.class_members + [p.class_member]

    @_('class_member')
    def class_members(self, p):
        return [p.class_member]

    @_('empty')
    def class_members(self, p):
        return []

    @_('decl')
    @_('func_decl')
    def class_member(self, p):
        return p[0]

    @_('ID COLON type SEMI')
    def decl(self, p):
        return node("VarDecl", name=p.ID, type=p.type, value=None, lineno=p.lineno)

    @_('ID COLON type ASSIGN expr SEMI')
    def decl(self, p):
        return node("VarDecl", name=p.ID, type=p.type, value=p.expr, lineno=p.lineno)

    @_('CONSTANT ID ASSIGN expr SEMI')
    def decl(self, p):
        return node("ConstDecl", name=p.ID, type=None, value=p.expr, lineno=p.lineno)

    @_('CONSTANT ID COLON type ASSIGN expr SEMI')
    def decl(self, p):
        return node("ConstDecl", name=p.ID, type=p.type, value=p.expr, lineno=p.lineno)

    @_('FUNCTION type ID LPAREN opt_func_params RPAREN block')
    def func_decl(self, p):
        return node(
            "FuncDecl",
            name=p.ID,
            return_type=p.type,
            params=p.opt_func_params,
            body=p.block,
            lineno=p.lineno,
        )

    @_('FUNCTION ID LPAREN opt_func_params RPAREN block')
    def func_decl(self, p):
        return node(
            "FuncDecl",
            name=p.ID,
            return_type=node("Type", name="void"),
            params=p.opt_func_params,
            body=p.block,
            lineno=p.lineno,
        )

    @_('func_params')
    def opt_func_params(self, p):
        return p.func_params

    @_('empty')
    def opt_func_params(self, p):
        return []

    @_('func_params COMA func_param')
    def func_params(self, p):
        return p.func_params + [p.func_param]

    @_('func_param')
    def func_params(self, p):
        return [p.func_param]

    @_('ID COLON type')
    def func_param(self, p):
        return node("Param", name=p.ID, type=p.type)

    @_('ID ID')
    def func_param(self, p):
        return node("Param", name=p.ID1, type=node("Type", name=p.ID0))

    @_('ID')
    def type(self, p):
        return node("Type", name=p.ID)

    @_('ID LBRACKET expr RBRACKET type')
    def type(self, p):
        return node("ArrayType", base=p.type, size=p.expr, tag=p.ID)

    @_('ID LBRACKET expr RBRACKET')
    def type(self, p):
        return node("ArrayType", base=None, size=p.expr, tag=p.ID)

    @_('block')
    @_('if_stmt')
    @_('while_stmt')
    @_('return_stmt')
    @_('break_stmt')
    @_('continue_stmt')
    @_('print_stmt')
    @_('decl')
    @_('expr_stmt')
    def stmt(self, p):
        return p[0]

    @_('LBRACE stmt_list RBRACE')
    def block(self, p):
        return node("Block", statements=p.stmt_list, lineno=p.lineno)

    @_('LBRACE RBRACE')
    def block(self, p):
        return node("Block", statements=[], lineno=p.lineno)

    @_('stmt_list stmt')
    def stmt_list(self, p):
        return p.stmt_list + [p.stmt]

    @_('stmt')
    def stmt_list(self, p):
        return [p.stmt]

    @_('IF LPAREN opt_expr RPAREN stmt ELSE stmt')
    def if_stmt(self, p):
        return node(
            "IfStmt",
            test=p.opt_expr,
            then_branch=p.stmt0,
            else_branch=p.stmt1,
            lineno=p.lineno,
        )

    @_('IF LPAREN opt_expr RPAREN stmt')
    def if_stmt(self, p):
        return node("IfStmt", test=p.opt_expr, then_branch=p.stmt, else_branch=None, lineno=p.lineno)

    @_('WHILE LPAREN opt_expr RPAREN stmt')
    def while_stmt(self, p):
        return node("WhileStmt", test=p.opt_expr, body=p.stmt, lineno=p.lineno)

    @_('PRINT opt_expr_list SEMI')
    def print_stmt(self, p):
        return node("PrintStmt", values=p.opt_expr_list, lineno=p.lineno)

    @_('RETURN opt_expr SEMI')
    def return_stmt(self, p):
        return node("ReturnStmt", value=p.opt_expr, lineno=p.lineno)

    @_('BREAK SEMI')
    def break_stmt(self, p):
        return node("BreakStmt", lineno=p.lineno)

    @_('CONTINUE SEMI')
    def continue_stmt(self, p):
        return node("ContinueStmt", lineno=p.lineno)

    @_('expr SEMI')
    def expr_stmt(self, p):
        return node("ExprStmt", expr=p.expr, lineno=p.lineno)

    @_('SEMI')
    def expr_stmt(self, p):
        return node("EmptyStmt", lineno=p.lineno)

    @_('expr_list')
    def opt_expr_list(self, p):
        return p.expr_list

    @_('empty')
    def opt_expr_list(self, p):
        return []

    @_('expr_list COMA expr')
    def expr_list(self, p):
        return p.expr_list + [p.expr]

    @_('expr')
    def expr_list(self, p):
        return [p.expr]

    @_('expr')
    def opt_expr(self, p):
        return p.expr

    @_('empty')
    def opt_expr(self, p):
        return None

    @_('lval ASSIGN expr')
    def expr(self, p):
        return node("AssignExpr", target=p.lval, value=p.expr, lineno=p.lineno)

    @_('expr LOR expr')
    @_('expr LAND expr')
    @_('expr EQ expr')
    @_('expr NE expr')
    @_('expr LT expr')
    @_('expr LE expr')
    @_('expr GT expr')
    @_('expr GE expr')
    @_('expr PLUS expr')
    @_('expr MINUS expr')
    @_('expr TIMES expr')
    @_('expr DIVIDE expr')
    @_('expr GROW expr')
    def expr(self, p):
        return node("BinaryExpr", op=p[1], left=p.expr0, right=p.expr1, lineno=p.lineno)

    @_('LNOT expr')
    @_('PLUS expr %prec UPLUS')
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return node("UnaryExpr", op=p[0], value=p.expr, lineno=p.lineno)

    @_('ID LPAREN opt_expr_list RPAREN')
    def expr(self, p):
        return node("CallExpr", callee=p.ID, args=p.opt_expr_list, lineno=p.lineno)

    @_('LBRACE opt_expr_list RBRACE')
    def expr(self, p):
        return node("ArrayLiteral", elements=p.opt_expr_list, lineno=p.lineno)

    @_('ID LBRACKET expr RBRACKET')
    def expr(self, p):
        return node("IndexExpr", array=node("Name", id=p.ID, lineno=p.lineno), index=p.expr, lineno=p.lineno)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('lval')
    def expr(self, p):
        return p.lval

    @_('INTEGER_LITERAL')
    @_('FLOAT_LITERAL')
    @_('CHAR_LITERAL')
    @_('STRING_LITERAL')
    def expr(self, p):
        return node("Literal", value=p[0], lineno=p.lineno)

    @_('TRUE')
    def expr(self, p):
        return node("Literal", value=True, lineno=p.lineno)

    @_('FALSE')
    def expr(self, p):
        return node("Literal", value=False, lineno=p.lineno)

    @_('ID')
    def lval(self, p):
        return node("Name", id=p.ID, lineno=p.lineno)

    @_('ID LBRACKET expr RBRACKET')
    def lval(self, p):
        return node("IndexExpr", array=node("Name", id=p.ID, lineno=p.lineno), index=p.expr, lineno=p.lineno)

    @_('')
    def empty(self, p):
        return None

    def error(self, p):
        if p:
            error(f"Syntax error at {p.type} ({p.value!r})", p.lineno)
        else:
            error("Syntax error at EOF")


def parse(source):
    clear_errors()
    lexer = Lexer()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(source))
    return ast


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Uso: python parser.py <archivo.bminor>")

    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        source = f.read()

    ast = parse(source)
    if errors_detected():
        raise SystemExit(1)

    print(json.dumps(ast, indent=2, ensure_ascii=False))