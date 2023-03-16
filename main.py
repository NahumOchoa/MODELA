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
    parser.tokenize("preprocessing WITH SCALING USING min_max")
    yacc.parser.parse("preprocessing WITH scaling USING min_max")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
