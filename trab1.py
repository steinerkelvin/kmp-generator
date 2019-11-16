
from typing import Tuple, List
import string
from pprint import pprint

import sympy
from sympy import Symbol, Eq

from kmp import Alphabet, SourceStatesMap, build_kmp_automata, build_inverted_map
from parser.input import parser as input_parser, InputTransformer

def build_equations(
        alphabet: Alphabet,
        inverted_map: SourceStatesMap,
        weighted = True,
    ) -> Tuple[Symbol, List[Symbol], List[Eq]]:
    
    # Número de estados
    M = len(inverted_map)

    z: Symbol = Symbol('z')

    # Símbolos que representam as funções geradoras associadas a cada estado
    st_syms: List[Symbol] = [Symbol(f's{i}') for i in range(M)]

    eqs = []
    for st in range(M):
        st_sym = st_syms[st]
        st_invmap = inverted_map[st]

        rhs_list = []
        for (c, src_sts) in st_invmap.items():
            n = len(src_sts)

            prob = alphabet[c]

            src_syms = map(lambda st: st_syms[st], src_sts)
            rhs_item = z * prob * sum(src_syms)
            rhs_list.append(rhs_item)

        rhs = sum(rhs_list)
        rhs = sympy.collect(rhs, z)

        if st == 0:
            rhs += 1

        eq = Eq(st_sym, rhs)
        eqs.append(eq)

    return z, st_syms, eqs


if __name__ == '__main__':
    # INPUT_FILE = 'exemplos/aabaaa.txt'
    # INPUT_FILE = 'exemplos/macaco.txt'
    INPUT_FILE = 'exemplos/macaco_probs.txt'

    with open(INPUT_FILE) as f:
        input_txt = f.read()

    input_ast = input_parser.parse(input_txt)
    problems = InputTransformer().transform(input_ast)

    for problem in problems:
        alphabet, pattern = problem

        kmp_map = build_kmp_automata(alphabet, pattern)
        inv_map = build_inverted_map(alphabet, kmp_map)

        z, s_syms, eqs = build_equations(alphabet, inv_map)

        for eq in eqs:
            sympy.pprint(eq)

    
        sols = sympy.solve(eqs, s_syms)

        for (sym, sol) in sols.items():
            print(f'\n{sym}:')
            pprint(sol)

        last_sfunc = sols[s_syms[-1]]

        # n = len(alphabet)
        # g = last_sfunc.subs(z, z/n)

        g = last_sfunc
        print("\bg(z)")
        pprint(g)

        gd = sympy.diff(g, z)
        print("\ng'(z)")
        pprint(gd)

        # result = gd.evalf(subs={z: 1})
        result = gd.subs({z: 1})

        print('\n')
        print('result: {}'.format(result))
        print('result: {}'.format(result.evalf()))
