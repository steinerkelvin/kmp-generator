#!/bin/python

from typing import Any
from dataclasses import dataclass
from collections import namedtuple
from itertools import repeat

import sympy
from lark import Lark, Transformer, v_args

grammar = r"""

    inputs:  input (","? input)*
    input: alphabet ","? pattern

    ?alphabet: "{" alphabet_body "}"
    alphabet_body: WORD     -> alphabet_word
            | _letter_list  -> alphabet_letters
            | _pair_list    -> alphabet_pairs

    ?pattern: "{" pattern_body "}"
    pattern_body: WORD -> pattern_word
        | _letter_list -> pattern_letters

    _pair_list: pair (","? pair)*
    pair: "(" letter "," prob ")"

    _letter_list: letter (","? letter)*
    letter: LETTER | "'" LETTER "'"

    prob: INT | DECIMAL | FRAC
    FRAC: INT "/" INT

    %import common.INT
    %import common.DECIMAL
    %import common.LETTER
    %import common.WORD
    %ignore " "
    %ignore "\n"

"""

parser = Lark(grammar, start='inputs')


Input = namedtuple('Input', ['alphabet', 'pattern'])

@v_args(inline=True)
class InputTransformer(Transformer):

    def inputs(self, *inputs):
        return list(inputs)

    def input(self, alphabet, pattern):
        return Input(alphabet, pattern)

    def alphabet_word(self, word):
        letter_map = dict(zip(list(word), repeat(None)))
        return letter_map

    def alphabet_letters(self, *letters):
        letter_map = dict(zip(letters, repeat(None)))
        return letter_map

    def alphabet_pairs(self, *pairs):
        letter_map = dict(pairs)
        return letter_map

    def pair(self, letter_tk, prob_tk):
        return (str(letter_tk), prob_tk)

    def letter(self, letter_tk):
        return str(letter_tk)

    def prob(self, prob_tk):
        return sympy.sympify(prob_tk)
    
    def pattern_word(self, word):
        return list(word)

    def pattern_letters(self, *letters):
        return list(letters)



if __name__ == '__main__':

    # Exemplo de entrada
    # {('C', 0.25), ('G', 0.25), ('A', 0.3), ('T', 0.2)}, {'CCUGATATA'}

    with open("exemplo_entrada.txt", "r") as f:
        txt = f.read()
        ast = parser.parse(txt)
        print(ast.pretty())

        transf = InputTransformer()
        result = transf.transform(ast)

        for r in result:
            alphabet, pattern = r
            print(alphabet)
            print(pattern)
            print()
