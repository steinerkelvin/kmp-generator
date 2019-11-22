#!/usr/bin/env python
# coding: UTF-8

import sympy

import parser
import solver
from kmp import build_kmp_automata, build_inverted_map, build_equations


if __name__ == '__main__':
    # INPUT_FILE = 'exemplos/aabaaa.txt'
    # INPUT_FILE = 'exemplos/cccc.txt'
    # INPUT_FILE = 'exemplos/macaco.txt'  # TODO
    INPUT_FILE = 'exemplos/macaco_probs.txt'

    # SOLVER = solver.native
    SOLVER = solver.mathematica

    with open(INPUT_FILE) as f:
        input_txt = f.read()

    input_ast = parser.input_parser.parse(input_txt)
    problems = parser.InputTransformer().transform(input_ast)

    for problem in problems:
        alphabet, pattern = problem

        kmp_map = build_kmp_automata(alphabet, pattern)
        inv_map = build_inverted_map(alphabet, kmp_map)

        # Constrói o sistema de equações para o autômato
        z, st_syms, eq_map = build_equations(alphabet, inv_map)

        # Resolver o sistema com o solucionador selecionado
        z, sols = SOLVER(z, st_syms, eq_map)

        # Pega função geradora do último estado
        last_sym = st_syms[-1]
        last_sfunc = sols[last_sym]

        # # Imprime todas funções geradoras
        # for (sym, sol) in sols.items():
        #     print(f"\n\n{sym}:")
        #     sympy.pprint(sol)

        # Imprime função geradora do estado final
        print("\n\n\n", f"{last_sym}:")
        sympy.pprint(last_sfunc)

        # TODO testar se deve adicionar os pesos
        # n = len(alphabet)
        # g = last_sfunc.subs(z, z/n)

        g = last_sfunc
        # print("\n\n\n", "g(z):"); sympy.pprint(g)

        # Deriva função geradora de probabilidades
        gd = sympy.diff(g, z)
        # print("\n\n\n", "g'(z):"); sympy.pprint(gd)

        # result = gd.evalf(subs={z: 1})
        result = gd.subs({z: 1})

        print('\n')
        print('result: {}'.format(result))
        print('result: {}'.format(result.evalf()))
