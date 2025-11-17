import sys
from sly import Lexer


class Scanner(Lexer):

    literals = { '(', ')', '{', '}', ';', '[', ']', ',', ':', '=', '.', '+', '-', '*', '/' }
    tokens = {
        'DOTPLUS', 'DOTMINUS', 'DOTTIMES', 'DOTDIV',
    'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVASSIGN',


    # relacyjne
    'EQ', 'NEQ', 'GT', 'LT', 'GE', 'LE',

    # słowa kluczowe
    'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN',
    'EYE', 'ZEROS', 'ONES', 'PRINT',

    # inne
    'TRANSPOSE', 'ID', 'FLOATNUM', 'INTNUM', 'STRING'
    }
    
    ignore = ' \t'
    ignore_comment = r'\#.*'
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = 'IF'
    ID['else'] = 'ELSE'
    ID['for'] = 'FOR'
    ID['while'] = 'WHILE'
    ID['break'] = 'BREAK'
    ID['continue'] = 'CONTINUE'
    ID['return'] = 'RETURN'
    ID['eye'] = 'EYE'
    ID['zeros'] = 'ZEROS'
    ID['ones'] = 'ONES'
    ID['print'] = 'PRINT'

    FLOATNUM = r'(\d+\.\d*|\.\d+)([eE][+-]?\d+)?'
    INTNUM = r'\d+'
    
    STRING = r'\".*?\"'

    # ASSIGN  = r'='
    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    TIMESASSIGN = r'\*='
    DIVASSIGN = r'/='

    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.-'
    DOTTIMES = r'\.\*'
    DOTDIV = r'\./'

    EQ = r'=='
    NEQ = r'!='
    GE = r'>='
    LE = r'<='
    GT = r'>'
    LT = r'<'


    TRANSPOSE = r'\''

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')



if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")


  