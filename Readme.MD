# Modela

Modela is a simple language designed to help data analysts and scientists to automate data preprocessing tasks. 

## Installation

To install Modela, please run the following command:

pip install modela

python
Copy code

## Usage

To use Modela, create a new Python file and import the necessary libraries:

import ply.lex as lex
import ply.yacc as yacc
from executors import ExecutorFactory
import pandas as pd
import config

javascript
Copy code

Then, create an instance of the `ModelaLexer` class and use its `tokenize` method to tokenize your data:

lexer = ModelaLexer()
lexer.tokenize(data)

kotlin
Copy code

After tokenizing your data, create an instance of the `ModelaYacc` class, build the parser, and parse your data:

parser = ModelaYacc()
parser.build()
parser.parse(data)

markdown
Copy code

## Contributing

To contribute to Modela, please follow these steps:

1. Fork this repository
2. Create a new branch (`git checkout -b new-feature`)
3. Make your changes and commit them (`git commit -am 'Added a new feature'`)
4. Push your changes to your fork (`git push origin new-feature`)
5. Create a pull request

## License

Modela is licensed under the MIT License. See `LICENSE` for more information.