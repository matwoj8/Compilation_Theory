from sly import Parser
from my_scanner import Scanner
from AST import *


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ("right", 'IFX'),
        ("right", 'ELSE'),
        ("right", '='),
        ("right", 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVASSIGN'),
        ("nonassoc", 'GT', 'LT', 'GE', 'LE', 'EQ', 'NEQ'),
        ("left", '+', '-','DOTPLUS', 'DOTMINUS'),
        ("left", '*', '/', 'DOTTIMES', 'DOTDIV'),
        ("right", 'UMINUS'),
        ("left", 'TRANSPOSE')
    )

    @_('instructions_or_empty')
    def program(self, p):
        return InstructionsOrEmpty(p[0])
    
    @_('instructions')
    def instructions_or_empty(self, p):
        return Instructions(p[0], lineno=p.lineno)

    @_('')
    def instructions_or_empty(self, p):
        return Instructions([], lineno=p.lineno)
    
    @_('instruction')
    def instructions(self, p):
        return [p[0]]

    @_('instructions instruction')
    def instructions(self, p):
        return p[0] + [p[1]]


    @_('return_i',
    'while_l',
    'for_l',
        'if_i',
    'assign ";"')
    def instruction(self, p):
        return p[0]
    
    @_('BREAK ";"')
    def instruction(self, p):
        return BreakStatement(lineno=p.lineno)
    
    @_("CONTINUE ';'")
    def instruction(self, p):
        return ContinueStatement(lineno=p.lineno)
    
    @_('PRINT expr ";"')
    def instruction(self, p):
        return PrintStatement(p[1], lineno=p.lineno)
    
    @_('PRINT expr "," expr ";"')
    def instruction(self, p):
        return PrintStatement([p[1], p[3]], lineno=p.lineno)
        

    @_('"{" instructions "}"') # musi tu zwracac blok instrukcji, teraz zwracal liste i  sie jebie
    def instruction(self, p):
        return Block(p[1], lineno=p.lineno)



    @_('expr "+" expr',
    'expr "-" expr',
    'expr "*" expr',
    'expr "/" expr',
    'expr DOTPLUS expr',
    'expr DOTMINUS expr',
    'expr DOTTIMES expr',
    'expr DOTDIV expr',
    'expr GT expr',
    'expr LT expr',
    'expr GE expr',
    'expr LE expr',
    'expr EQ expr',
    'expr NEQ expr',
        'expr TRANSPOSE',)
    def expr(self, p):
        if len(p) == 3:
            return BinaryExpression(p[0], p[1], p[2], lineno=p.lineno)
        else:
            return UnaryExpression('TRANSPOSE', p[0], lineno=p.lineno)   
    

    @_('ID "[" expr "]"',
    'ID "[" expr "," expr "]"')
    def tab(self, p):
        return IdTab(p[0], p[2], p[4] if len(p) == 6 else None, lineno=p.lineno)


    @_('INTNUM')
    def expr(self, p):
        return IntNum(p[0], lineno=p.lineno)
    
    @_('STRING')
    def expr(self, p):
        return StringNum(p[0], lineno = p.lineno)
    
    @_('ID')
    def expr(self, p):
        return IDNum(p[0], lineno = p.lineno)
    
    @_('FLOATNUM')
    def expr(self, p):
        return FloatNum(p[0], lineno=p.lineno)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p[1]
    
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return UnaryExpression('UMINUS', p[1], lineno=p.lineno)
    
    @_('matrix')
    def expr(self, p):
        return p[0]
        

    @_(' "[" lists "]" ')
    def matrix(self, p):
        return Matrix(p[1], lineno = p.lineno)

    @_('list ";" lists',
    'list')
    def lists(self, p):
        if len(p) == 1:
            return [p[0]]        
        else:
            return [p[0]] + p[2]

    @_('expr "," list',
    'expr')
    def list(self, p):
        if len(p) == 1:
            return [p[0]]        
        else:
            return [p[0]] + p[2]

    @_('mat_fun "(" INTNUM ")"')
    def matrix(self, p):
        return MatFun(p[0] , IDNum(p[2], lineno = p.lineno), lineno=p.lineno)

    
    @_('ZEROS',
    'EYE',
    'ONES')
    def mat_fun(self, p):
        return p[0]

    
    @_('IF "(" expr ")" instruction %prec IFX',
    'IF "(" expr ")" instruction ELSE instruction')
    def if_i(self, p):
        if len(p) == 5:
            return IfStatement(p[2], p[4], None, lineno=p.lineno)
        else:
            return IfStatement(p[2], p[4], p[6], lineno=p.lineno)
            
    @_('RETURN ";"',
    'RETURN expr ";"')
    def return_i(self, p):
        return ReturnStatement(p[1] if len(p) == 3 else None, lineno = p.lineno)
    
    @_('WHILE "(" expr ")" instruction')
    def while_l(self, p):
        return WhileLoop(p[2], p[4], lineno=p.lineno)
    
    @_('FOR ID "=" expr ":" expr instruction')
    def for_l(self, p):
        return ForLoop(IDNum(p[1], lineno=p.lineno), p[3], p[5], p[6], lineno=p.lineno)
    
    @_('ID')
    def value(self, p):
        return IDNum(p[0], lineno=p.lineno)

    @_('tab',
    'matrix')
    def value(self, p):
        return p[0]

    @_('value "=" expr' ,
    'value PLUSASSIGN expr',
    'value MINUSASSIGN expr',
    'value TIMESASSIGN expr',
    'value DIVASSIGN expr')
    def assign(self, p):
        return Assignment(p[0], p[1], p[2], lineno=p.lineno)

    def error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")



