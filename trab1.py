#!/usr/bin/env python
# coding: UTF-8

from sys import stderr
import argparse
import sympy

import parser
import solver
from kmp import build_kmp_automata, build_inverted_map, build_equations

def pterr(*args, **kargs):
    print(*args, **kargs, file=stderr)

def fill_probs(alphabet):
    prob_sum = sum(
        filter(lambda x: x != None, alphabet.values()),
    )
    none_count = len(list(
        filter(lambda x: x == None, alphabet.values())
    ))

    fill_prob = (sympy.sympify(1) - prob_sum) / none_count

    new_alphabet = {}
    for c, p in alphabet.items():
        if p == None:
            new_alphabet[c] = fill_prob
        else:
            new_alphabet[c] = p

    return new_alphabet


argparser = argparse.ArgumentParser(description=(
    "Gera automato KMP e calcula o tempo médio para uma entrada aleatória ser aceita."))
argparser.add_argument('input_file')

if __name__ == '__main__':
    args = argparser.parse_args()
    input_file = args.input_file

    # SOLVER = solver.native
    SOLVER = solver.mathematica

    with open(input_file) as f:
        input_txt = f.read()

    input_ast = parser.input_parser.parse(input_txt)
    problems = parser.InputTransformer().transform(input_ast)

    for problem in problems:
        alphabet, pattern = problem

        alphabet = fill_probs(alphabet)

        kmp_map = build_kmp_automata(alphabet, pattern)
        inv_map = build_inverted_map(alphabet, kmp_map)

        # Constrói o sistema de equações para o autômato
        z, st_syms, eq_map = build_equations(alphabet, inv_map)

        # Resolver o sistema com o solucionador selecionado
        z, sols = SOLVER(z, st_syms, eq_map)

        # Pega função geradora do último estado
        last_sym = st_syms[-1]
        last_sfunc = sols[last_sym]

        # n = len(alphabet)
        # g = last_sfunc.subs(z, z/n)

        g = last_sfunc

        # Deriva função geradora de probabilidades
        gd = sympy.diff(g, z)

        # result = gd.evalf(subs={z: 1})
        result = gd.subs({z: 1})


        # Saída

        print("\n")
        print("g(z):")
        sympy.pprint(g, wrap_line=False)

        print("\n\n")
        print("g'(z):")
        sympy.pprint(gd, wrap_line=False)

        # Imprime todas funções geradoras
        print("\n")
        for (sym, sol) in sols.items():
            print("\n")
            print(f"{sym}:")
            sympy.pprint(sol, wrap_line=False)

        # # Imprime função geradora do estado final
        # pterr("\n\n")
        # pterr(f"{last_sym}:")
        # sympy.pprint(last_sfunc, wrap_line=False)

        print('\n\n')
        print('Tempo médio = {}'.format(result))
        print('            = {}'.format(result.evalf()))
