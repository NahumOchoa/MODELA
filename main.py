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
    parser.tokenize("LOAD DATA FROM FILE(source='prueba.csv', type=csv)")
    yacc.parser.parse("LOAD DATA FROM FILE(source='prueba.csv', type=csv)")
    parser.tokenize("preprocessing USING(type=encoding, method=one_hot, cols=[test3,test4])")
    yacc.parser.parse("preprocessing USING(type=encoding, method=one_hot, cols=[test3,test4])")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
