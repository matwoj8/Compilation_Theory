
import sys
import ply.yacc as yacc
from my_parser import Mparser
from my_scanner import Scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser()
    scanner = Scanner()
    text = file.read()

    ast = parser.parse(scanner.tokenize(text))

    # Below code shows how to use visitor
    # typeChecker = TypeChecker()   
    # typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    print("Interpreter: ")
    interpreter = Interpreter()
    interpreter.visit(ast)
    print("\n")
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
    