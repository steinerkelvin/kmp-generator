
from typing import TypeVar, Optional, List, Dict
from sympy import Number

T = TypeVar('T')
Letter = str
Alphabet = Dict[str, Optional[Number]]
NextStateMap = List[Dict[Letter, int]]

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
    ):

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


if __name__ == '__main__':
    from sympy import sympify

    half = sympify('1/2')
    alphabet = {'a': half, 'b': half}
    pattern = list("aabaaa")

    kmp = build_kmp_automata(alphabet, pattern)
    print(kmp)
