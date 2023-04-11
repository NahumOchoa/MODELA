import ply.lex as lex
import ply.yacc as yacc
from executors import ExecutorFactory
import pandas as pd
import config


class ModelaLexer:
    # List tokens
    tokens = config.tokens

    # General purpose strings
    NO_NAMES = config.NO_NAMES
    # Token Definitions
    t_SPECIAL_CHARACTERS = config.t_SPECIAL_CHARACTERS
    t_ignore_SPACE = config.t_ignore_SPACE

    t_URL = config.t_URL
    t_EQUALS = config.t_EQUALS
    t_STRING = config.t_STRING
    t_TRANSFORMATION = config.t_TRANSFORMATION
    t_FILE = config.t_FILE
    t_SETTER = config.t_SETTER
    t_FROM = config.t_FROM
    t_DO = config.t_DO
    t_LOAD = config.t_LOAD
    t_DATA = config.t_DATA
    t_TASK = config.t_TASK
    t_ALGORITHM = config.t_ALGORITHM
    t_PREPROCESSING = config.t_PREPROCESSING
    t_TYPE_MODEL = config.t_TYPE_MODEL
    t_LEARNER = config.t_LEARNER
    t_MODEL = config.t_MODEL

    def t_NUMBER(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_NAME(self, t):
        r'(?!(set|SET|from|FROM|do|DO|load|LOAD|data|DATA|MODEL|model|WITH|with|FILE|file|SCALING|ENCODING|IMPUTATION|scaling|encoding|imputation|PREPROCESSING|preprocessing|min_max|gaussian|one_hot|simple_imputer|MIN_MAX|GAUSSIAN|ONE_HOT|SIMPLE_IMPUTER))[a-zA-Z_0-9\-]+'
        t.value = str(t.value)
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs, debug=1)

    def input(self, data: str):
        self.lexer.input(data)

    def tokenize(self, data):
        self.lexer.input(data)
        for token in self.lexer:
            print(token)


class ModelaYacc:
    tokens = config.tokens

    def p_expression_number(self, t):
        'expression : NUMBER'
        print(str(t[1]))
        t[0] = t[1]

    def p_expression_setter(self, t):
        'expression : SETTER assign'
        pass
        #print(str(t[1]) + ' ' + str(t[2]))

    def p_expression_string(self, t):
        'expression : STRING'
        print(str(t[1]))
        t[0] = t[1]

    def p_expression_name(self, t):
        'expression : NAME'
        try:
            t[0] = self.names[t[1]]
            print(f"{t[1]}: {t[0]}")
        except LookupError:
            print("Undefined name '%s'" % t[1])
            t[0] = 0

    def p_statement_assign(self, t):
        '''assign : NAME EQUALS expression
                  | assign NAME EQUALS expression'''

        params = {"set": t}
        factory = ExecutorFactory()
        executor = factory.get_executor("SET", params)
        names_dict = executor.execute()
        self.names["".join(names_dict.keys())] = names_dict["".join(names_dict.keys())]

    def p_statement_preprocessing(self, t):
        '''expression : PREPROCESSING'''
        print(t[1])
        params = {"input_command": t[1], "df": self.data}
        factory = ExecutorFactory()
        executor = factory.get_executor("PREPROCESSING", params)
        self.data = executor.execute()
        print(self.data)

    def p_statement_model(self, t):
        '''expression : MODEL'''
        params = {"input_command": t[1], "df": self.data}
        factory = ExecutorFactory()
        executor = factory.get_executor("MODEL", params)
        self.data = executor.execute()

    def p_statement_load_data(self, t):
        '''expression : LOAD DATA FROM FILE'''
        work_dir = self.names.get("WORKING_DIRECTORY") or ""
        params = {"file_name": t[4], "work_directory": work_dir}
        factory = ExecutorFactory()
        executor = factory.get_executor("LOAD_DATA_FROM_FILE", params)
        self.data = executor.execute()
        print(self.data)

    def __init__(self):
        self.data = pd.DataFrame()
        self.names = {"test": self.data}
        self.parser = None

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data: str):
        self.parser.parse(data)
