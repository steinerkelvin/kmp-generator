
from typing import TypeVar, Dict, List
import string

T = TypeVar('T')

LETTERS = list(string.ascii_lowercase)

def run(map_next: List[Dict[str, int]], txt: str) -> int:
    last = len(map_next) - 1
    s = 0
    for c in txt:
        # Considera transições inexistentes como indo ao estado 0
        s = map_next[s].get(c, 0)  
        if s == last:
            break
    return s

def build_kmp_automata(alphabet, pat):

    # Tamanho do padrão
    N = len(pat)
    # Número de estados
    M = N + 1

    # Mapa de próximos estados para cada estado para cada letra
    map_next = [ dict() for _ in range(M) ]

    for (i, ic) in enumerate(pat):
        map_next[i][ic] = i+1

    for i in range(1, N):
        c_i = pat[i]
        for c in alphabet:
            if c != c_i:
                sub_pat = pat[1:i] + c
                nxt = run(map_next, sub_pat)
                if nxt != 0:  # Ignora transições que "resetam" o automato
                    map_next[i][c] = nxt

    return map_next



if __name__ == '__main__':

    pat = "tobeornottobe"
    txt = "tobeornoto"

    map_next = build_kmp_automata(LETTERS, pat)
    print(map_next)

    for (s, mp) in enumerate(map_next):
        print(f"\n{s}:")
        for (c, nxt) in mp.items():
            # if nxt != 0:
            print(f"  {c} -> {nxt}")

    s = run(map_next, txt)

    print('\n')
    print("RESULT:", s)


    print('\n\nGRAPHVIZ:\n')
    print('digraph G {')
    print('  rankdir="LR";')

    for (s, mp) in enumerate(map_next):
        for (c, nxt) in mp.items():
            # if nxt != 0:
            print(f"  {s} -> {nxt} [label=\"{c}\"]")

    print('}')
