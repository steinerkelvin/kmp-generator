
from typing import TypeVar, Optional, Tuple, List, Dict
import sympy
from sympy import Number, Symbol, Expr

T = TypeVar('T')
Letter = str
Alphabet = Dict[str, Optional[Number]]
NextStateMap = List[Dict[Letter, int]]
SourceStatesMap = List[Dict[Letter, List[int]]]

def run_kmp(
        map_next: NextStateMap,
        pat: List[Letter],
    ) -> int:
    last = len(map_next) - 1
    s = 0
    for c in pat:
        # Considera transições inexistentes como indo ao estado 0
        s = map_next[s].get(c, 0)  
        if s == last:
            break
    return s

def build_kmp_automata(
        alphabet: Alphabet,
        pat: List[Letter],
    ) -> NextStateMap:

    # Tamanho do padrão
    N = len(pat)
    # Número de estados
    M = N + 1

    # Mapa de próximos estados para cada estado para cada letra
    map_next: NextStateMap = [ dict() for _ in range(M) ]

    for (i, ic) in enumerate(pat):
        map_next[i][ic] = i+1

    for i in range(1, N):
        c_i = pat[i]
        for c in alphabet:
            if c != c_i:
                sub_pat = pat[1:i] + [c]
                nxt = run_kmp(map_next, sub_pat)
                if nxt != 0:  # Ignora transições que "resetam" o automato
                    map_next[i][c] = nxt

    return map_next

def build_inverted_map(
        alphabet: Alphabet,
        map_next: NextStateMap,
    ):
    # Quantidade de estados
    M = len(map_next)
    inverted_map: SourceStatesMap = [ dict() for _ in range(M) ]

    # Ignora o último estado, já que não devem existir transições a partir dele
    for st in range(M-1):  
        st_mp = map_next[st]
        for c in alphabet:
            nxt_st: int = st_mp.get(c, 0)
            src_st_list = inverted_map[nxt_st].setdefault(c, [])
            src_st_list.append(st)

    return inverted_map

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
    import string
    from itertools import repeat
    from pprint import pprint
    from sympy import sympify, pprint as sympt

    half = sympify('1/2')

    # alphabet = {'a': half, 'b': half}
    # pattern = list("aabaaa")

    prob = sympify(1) / 26
    alphabet = dict(zip(list(string.ascii_lowercase), repeat(prob)))
    pattern = list("tobeornottobe")

    print(f"alphabet={alphabet}", "\n")

    map_next = build_kmp_automata(alphabet, pattern)
    print(f"map_next={map_next}", "\n")

    inv = build_inverted_map(alphabet, map_next)

    print("inverted map:")
    for (s, mp) in enumerate(inv):
        print(f"{s}: ")
        pprint(mp)
        print()
