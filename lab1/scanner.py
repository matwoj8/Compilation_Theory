import sys
from sly import Lexer


class Scanner(Lexer):

    tokens = { 'ID', 'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN', 'EYE',
               'ZEROS', 'ONES', 'PRINT', 'DOTADD', 'DOTSUB', 'DOTDIV', 'DOTMUL', 'ADDASSIGN',
               'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'SMALLASSIGN', 'LARGEASSIGN', 'ASSIGNASSIGN',
               'NOTASSIGN','STRING', 'INT', 'FLOAT'}

    literals = ['=', '+', '-', '*', '/', '<', '>', '(', ')', '[', ']', '{', '}', ':', "'", ';', ',', '.']

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

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

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTDIV = r'\./'
    DOTMUL = r'\.\*'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'\-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'\/='

    SMALLASSIGN = r'\<='
    LARGEASSIGN = r'\>='
    ASSIGNASSIGN = r'\=='
    NOTASSIGN = r'\!='

    STRING = r'\".*?\"'
    FLOAT = r'\d+\.\d+'
    INT = r'\d+'

    pass


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")
