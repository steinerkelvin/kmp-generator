#!/bin/python

import ast
import re
from lark import Lark, Token

fracs = []

# parser = Lark("""
# start: FRAC*
# FRAC: INT+ "/" INT+
# %import common.INT
# %ignore " "
# """, parser="lalr")
# parser.parse('3/12')

parser = Lark(r"""

    inputs:  input (","? input)*
    input: alphabet ","? pattern
    alphabet: "{" (WORD | letter_list | pair_list) "}"
    pattern:  "{" (WORD | letter_list ) "}"

    letter_list: letter (","? letter)*
    pair_list: pair (","? pair)*
    pair: "(" letter "," prob ")"
    letter: LETTER | "'" LETTER "'"

    prob: INT | DECIMAL | FRAC
    FRAC: INT "/" INT

    %import common.INT
    %import common.DECIMAL
    %import common.LETTER
    %import common.WORD
    %ignore " "
    %ignore "\n"

""", start='inputs')


if __name__ == '__main__':

    # Exemplo de entrada
    # {('C', 0.25), ('G', 0.25), ('A', 0.3), ('T', 0.2)}, {'CCUGATATA'}

    with open("exemplo_entrada.txt", "r") as f:
        txt = f.read()
        ast = parser.parse(txt)
        # print(ast)
        print(ast.pretty())
