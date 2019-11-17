
from typing import Tuple, List, Dict

import sympy
from sympy import Symbol, Expr

from kmp import Alphabet, SourceStatesMap, build_kmp_automata, build_inverted_map
from parser.input import parser as input_parser, InputTransformer

from solver.native      import solve_system as solve_system_native
from solver.mathematica import solve_system as solve_system_mathematica


def build_equations(
        alphabet: Alphabet,
        inverted_map: SourceStatesMap,
        weighted = True,
    ) -> Tuple[Symbol, List[Symbol], Dict[str, Expr]]:
    
    # Número de estados
    M = len(inverted_map)

    z = Symbol('z')

    # Símbolos que representam as funções geradoras associadas a cada estado
    st_syms: List[Symbol] = [Symbol(f's{i}') for i in range(M)]

    eq_map = {}
    for st in range(M):
        stsym = st_syms[st]
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

        # eq = Eq(stsym, rhs)
        # eqs.append(eq)

        eq_map[stsym] = rhs

    return z, st_syms, eq_map



if __name__ == '__main__':
    # INPUT_FILE = 'exemplos/aabaaa.txt'
    # INPUT_FILE = 'exemplos/macaco.txt'  # TODO
    INPUT_FILE = 'exemplos/macaco_probs.txt'

    # SOLVER = solve_system_native
    SOLVER = solve_system_mathematica

    with open(INPUT_FILE) as f:
        input_txt = f.read()

    input_ast = input_parser.parse(input_txt)
    problems = InputTransformer().transform(input_ast)

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
