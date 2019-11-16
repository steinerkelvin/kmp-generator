
import string
from sympy import Symbol, Eq, collect, pprint, diff, solve, simplify, latex
from macacos_kmp import build_kmp_automata, get_inverted_map

def build_equations(inverted_map):
    M = len(inverted_map)
    z = Symbol('z')
    s_syms = [Symbol(f's{i}') for i in range(M)]

    eqs = []
    for s in range(M):
        sym = s_syms[s]

        rhs_list = []
        invmap = inverted_map[s]
        for (src_st, chars) in invmap.items():
            # Ignora transições a partir do último estado
            if src_st == M - 1:
                continue
            n = len(chars)
            rhs_list.append(
                z * n * s_syms[src_st],
            )

        if s == 0:
            rhs_list.append(1)

        rhs = sum(rhs_list)
        rhs = collect(rhs, z)

        eq = Eq(sym, rhs)
        eqs.append(eq)

    return z, s_syms, eqs


if __name__ == '__main__':

    pat = "tobeornottobe"
    txt = "tobeornoto"

    LETTERS = list(string.ascii_lowercase)

    map_next = build_kmp_automata(LETTERS, pat)
    inverted_map = get_inverted_map(LETTERS, map_next)

    # def pprint(*args):
    #     print(latex(*args))

    # pprint(inverted_map)

    z, s_syms, eqs = build_equations(inverted_map)

    print(s_syms)

    for eq in eqs:
        pprint(eq)

    sols = solve(eqs, s_syms)

    for (sym, sol) in sols.items():
        print(f'\n{sym}:')
        pprint(sol)

    n = len(LETTERS)
    last_sfunc = sols[s_syms[-1]]

    g = last_sfunc.subs(z, z/n)

    print("\bg(z/n)")
    pprint(g)

    gd = diff(g, z)

    print("\ng'(z/n)")
    pprint(gd)

    # result = gd.evalf(subs={z: 1})
    result = gd.subs({z: 1})

    print('\n')
    print('result: {}'.format(result))
    print('result: {}'.format(result.evalf()))
