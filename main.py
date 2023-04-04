"""
MODELA language project
"""

__author__ = ""
__version__ = "0.1.0"
__license__ = "MIT"

from modela_compiler import ModelaLexer
from modela_compiler import ModelaYacc


def main():
    parser = ModelaLexer()
    yacc = ModelaYacc()
    yacc.build()
    parser.build()
    while True:
        try:
            s = input('modela > ')
            if s == 'exit' or s == 'quit':
                break
        except EOFError:
            break
        if not s:
            continue
        parser.input(s)
        yacc.parser.parse(s)
    parser.tokenize("LOAD DATA FROM FILE(source='Allstate-cost-cleaned.csv', type=csv)")
    yacc.parser.parse("LOAD DATA FROM FILE(source='prueba.csv', type=csv)")
    parser.tokenize("PREPROCESSING(type=encoding, method=one_hot, cols=[test3,test4])")
    yacc.parser.parse("preprocessing USING(type=encoding, method=one_hot, cols=[test3,test4])")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
