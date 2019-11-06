
import string
import symengine
from kmp import build_kmp_automata, run_kmp, get_inverted_map

def build_mat(inverted_map):
    return (None, None, None)


if __name__ == '__main__':

    pat = "tobeornottobe"
    txt = "tobeornoto"

    LETTERS = list(string.ascii_lowercase)

    map_next = build_kmp_automata(LETTERS, pat)
    inverted_map = get_inverted_map(LETTERS, map_next)

    z, s_syms, mat = build_mat(inverted_map)
