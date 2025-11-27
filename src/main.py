import sys
from my_scanner import Scanner
from my_parser import Mparser
import AST
from TreePrinter import TreePrinter


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()


    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    ast.printTree()
