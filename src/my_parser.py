from sly import Parser
from my_scanner import Scanner


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

    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction')
    def instructions(self, p):
        pass

    @_('instruction')
    def instructions(self, p):
        pass

    @_('BREAK ";"',
       'CONTINUE ";"',
       'return_i',
       'while_l',
       'for_l',
        'if_i', 
       'PRINT "(" expr ")" ";"',
       'PRINT expr ";"',
       'PRINT expr "," expr ";"',
       'assign ";"')
    def instruction(self, p):
        pass

    @_('"{" instructions_opt "}"')
    def instruction(self, p):
        pass



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
        pass

    @_('ID "[" expr "]"',
       'ID "[" expr "," expr "]"')
    def tab(self, p):
        pass

    @_('INTNUM',
       'FLOATNUM',
       'STRING',
       'ID',
       '"(" expr ")"',
       '"-" expr %prec UMINUS',
        'matrix'
       )
    def expr(self, p):
        pass

    @_(' "[" lists "]" ')
    def matrix(self, p):
        pass

    @_('list ";" lists',
       'list')
    def lists(self, p):
        pass

    @_('expr "," list',
       'expr')
    def list(self, p):
        pass

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix(self, p):
        pass

    
    @_('IF "(" expr ")" instruction %prec IFX',
       'IF "(" expr ")" instruction ELSE instruction')
    def if_i(self, p):
        pass
    
    @_('RETURN ";"',
       'RETURN expr ";"')
    def return_i(self, p):
        pass
    
    @_('WHILE "(" expr ")" instruction')
    def while_l(self, p):
        pass
    
    @_('FOR ID "=" expr ":" expr instruction')
    def for_l(self, p):
        pass

    

    @_('ID "=" expr' ,
       'ID PLUSASSIGN expr',
       'ID MINUSASSIGN expr',
       'ID TIMESASSIGN expr',
       'ID DIVASSIGN expr',
       'tab "=" expr',
       'tab PLUSASSIGN expr',
       'tab MINUSASSIGN expr',
       'tab TIMESASSIGN expr',
       'tab DIVASSIGN expr',
       'matrix "=" expr',
       'matrix PLUSASSIGN expr',
       'matrix MINUSASSIGN expr',
       'matrix TIMESASSIGN expr',
       'matrix DIVASSIGN expr')
    def assign(self, p):
        pass

    def error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")



