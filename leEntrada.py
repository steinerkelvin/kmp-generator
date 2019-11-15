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

frac_parser = Lark(r"""
    value: dictlist
    dict: "{" letralist "}" | "{" pairlist "}" | "{" WORD "}"
    dictlist: [dict ("," dict)*]
    
    letra: "'" LETTER "'" | LETTER
    letralist: [letra ("," letra)*]
    prob: DECIMAL | INT | FRAC
    pair: "(" letra "," prob ")"
    pairlist: [pair ("," pair)*]
    
    FRAC: INT+ "/" ("1".."9")+
    
    %import common.INT
    %import common.LETTER
    %import common.WORD
    %import common.DECIMAL
    %ignore " "
""", start='value')

# print(fracs)

# print(parser.parse('3/12'))
f = open("teste.txt", "r")

# Exemplo de entrada
# {('C', 0.25), ('G', 0.25), ('A', 0.3), ('T', 0.2)},{'CCUGATATA'}

# entradaEx = f.readline()
# entradaEx = f.readline()
entradaEx = f.readline()
while entradaEx:
    entradaEx = entradaEx.replace('\n', '') # Tira o \n da string
    print(entradaEx)
    print(frac_parser.parse(entradaEx).pretty())
    entradaEx = f.readline()

print(entradaEx)