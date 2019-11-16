
import string

from symengine import Symbol, zeros, sympify
# from sympy import Symbol, sympify, zeros, SparseMatrix

# from sympy import pprint

from kmp import build_kmp_automata, run_kmp, get_inverted_map

# TODO numpy

def build_mat(inverted_map):
    M = len(inverted_map)
    z = Symbol('z')
    s_syms = [Symbol(f's{i}') for i in range(M)]

    mat = zeros(M, M)
    # mat = SparseMatrix.zeros(M, M)

    for st in range(M):
        sym = s_syms[st]
        mat[st, st] = sympify(-1)
        # mat[st, st] = -1

        invmap = inverted_map[st]
        for (src_st, chars) in invmap.items():
            n = len(chars)
            if src_st == M - 1:
                continue
            mat[st, src_st] += n * z

    return (z, s_syms, mat)


if __name__ == '__main__':

    pat = "tobeornottobe"
    txt = "tobeornoto"

    LETTERS = list(string.ascii_lowercase)

    map_next = build_kmp_automata(LETTERS, pat)
    inverted_map = get_inverted_map(LETTERS, map_next)

    z, s_syms, mat = build_mat(inverted_map)

    M = len(s_syms)
    b = zeros(M, 1)
    b[0] = -1

    # for i in range(M):
    #     print("[", end='')
    #     for j in range(M):
    #         print("{!s:8}".format(mat[i,j]), end=', ')
    #     print("],")

    print(mat)
    print(b)

    # res = mat.LUsolve(b)
    res = mat.solve(b)
    # pprint(res)
    print(res)
