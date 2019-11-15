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

#pega a posicao da segunda ocorrencia de um caracter
def acha_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

def junta_padrao(listaPadrao):
    probFracoes = []
    for index, tuplaFracao in enumerate(listaPadrao):
        fracao = tuplaFracao[0] + '/' + tuplaFracao[1]
        probFracoes.insert(index, fracao)
    return probFracoes

def refaz_tuplas(probFracoes, probabilidades):
    for j in probabilidades:
        print(j)

# Exemplo de entrada
# {('C', 0.25), ('G', 0.25), ('A', 0.3), ('T', 0.2)},{'CCUGATATA'}

# entradaEx = f.readline()
# entradaEx = f.readline()
entradaEx = f.readline()
entradaEx = entradaEx.replace('\n', '') # Tira o \n da string
while entradaEx:
    entradaEx = entradaEx.replace('\n', '') # Tira o \n da string
    print(entradaEx)
    print(frac_parser.parse(entradaEx).pretty())
    entradaEx = f.readline()

print(entradaEx)

# Acha a primeira ocorrencia das chaves, e cria uma string que vai desde essa primeira ocorrencia, ate a ultima
# Ou seja, separa a parte que representa as probabilidasdes das letras ocorrerem no padrao em uma outra string 
probabilidades = entradaEx[entradaEx.find("{")+1:entradaEx.find("}")]
print(probabilidades)
# print(frac_parter.parse(probabilidades))
# a =
# x = re.findall('(-?\d+)\/(\d+)', probabilidades)
# print(x)
# aa = junta_padrao(x)
# print(aa)
# print(refaz_tuplas(aa, probabilidades))


# # Mesmo raciocinio para a separacao do padrao, exceto dessa vez, procuramos a segunda ocorrencia das chaves
# padrao = list(entradaEx[acha_2nd(entradaEx, '{')+1:acha_2nd(entradaEx, '}')])
# print(padrao)

# # Transforma a string de probabilidades em uma lista de tuplas
# probLista = list(ast.literal_eval(probabilidades))
# print(probLista)

# # Kelvin pediu para q as probabilidades sejam lidas como string
# for index, tuplaProb in enumerate(probLista):
#     itemTProb = list(tuplaProb)
#     for i, elem in enumerate(itemTProb):
#         itemTProb[i] = str(elem)
#     tuplaProb = tuple(itemTProb)
#     probLista[index] = tuplaProb

# print(probLista)
# print(padrao)