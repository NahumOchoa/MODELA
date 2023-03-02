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
        'TRANSFORMATION'
    ]

# General purpose strings
NO_NAMES = 'set|SET|from|FROM|do|DO|load|LOAD|data|DATA'
# Token Definitions
t_SPECIAL_CHARACTERS = r'[\;\:\.]+'
t_ignore_SPACE = '\s+|\,+'
t_NAME = r'(?!(' + NO_NAMES + '))[a-zA-Z_0-9\-]+'
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

