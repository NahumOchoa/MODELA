tokens = [
        'SPECIAL_CHARACTERS',
        'SETTER',
        'FROM',
        'DO',
        'LOAD',
        'DATA',
        'FILE',
        'NUMBER',
        'NAME',
        'STRING',
        'EQUALS',
        'URL',
        'TRANSFORMATION',
        'PREPROCESSING',
        'ALGORITHM',
        'TASK',
        'USING',
    ]

# General purpose strings
NO_NAMES = 'set|SET|from|FROM|do|DO|load|LOAD|data|DATA|PREPROCESSING|preprocessing|WITH|with|USING|using|'
# Token Definitions
t_SPECIAL_CHARACTERS = r'[\;\:\.]+'
t_ignore_SPACE = '\s+|\,+'

t_URL = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[' \
        r'a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
t_EQUALS = r'='
t_STRING = r'[\'\"]{1}.+[\'\"]{1}'
t_TRANSFORMATION = r'TRANSFORMATION\(type=(numerical|categorical)\,?(\s*)on=\[[\w\d\-\_]+\,?(\s*)[\w\d\-\_?(\,' \
                   r'\s)]+\]?(\,\s*method=(standard|max_min))*\)'
t_FILE = r'FILE\(source=\'[\w\d\-\_]+\.[\w]{1,4}\'?(\s*)\,?(\s*)type=(csv|xlsx|txt)?([\,\s]*params=\[.*\])*\)'
t_SETTER = r'set|SET'
t_FROM = r'from|FROM'
t_DO = r'do|DO'
t_LOAD = r'load|LOAD'
t_DATA = r'data|DATA'
t_TASK = r'SCALING|ENCODING|IMPUTATION|scaling|encoding|imputation'
t_ALGORITHM = r'min_max|gaussian|one_hot|simple_imputer|MIN_MAX|GAUSSIAN|ONE_HOT|SIMPLE_IMPUTER'
t_PREPROCESSING = r'PREPROCESSING|preprocessing'
t_NAME = r'(?!(' + NO_NAMES+'))(?!(' + t_ALGORITHM +'))(?!(' + t_PREPROCESSING +'))[a-zA-Z_0-9\-]+'
t_USING = r'USING\(type=(' + t_TASK + ')\,?(\s*)method=(' + t_ALGORITHM + ')\,?(\s*)cols=\[[\w\d\-\_\']+(\s*\,\s*[\w\d\-\_\']+)*\](\s*)\)'
t_USING_PATTERN = r'USING\(type=(\w+),\s*method=(\w+),\s*cols=\[(.*)\]\)'
