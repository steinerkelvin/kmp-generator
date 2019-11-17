
from typing import Tuple, List, Dict
import sympy

from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.serializers import export

from wolframclient.language.expression import WLFunction, WLSymbol

def remove_prefix(txt: str, prefix: str):
    if txt.startswith(prefix):
        n = len(prefix)
        return txt[n:]
    return txt

class BaseTransformer:
    _symbols: List[sympy.Symbol]

    def __init__(self):
        self._symbols = []

    def transform(self, tree):
        return self._handle_node(tree)

    def _handle_node(self, tree):
        if isinstance(tree, WLFunction):
            # print(f"{tree.head.name=}")  ## DEBUG
            return self._handle_function(tree)
        elif isinstance(tree, WLSymbol):
            # print(f"{tree.name=}")  ## DEBUG
            newsb = self._handle_symbol(tree)
            # print(f"{newsb=}")  ## DEBUG
            return newsb
        else:
            return tree

    def _handle_function(self, func: WLFunction):
        # print()  ## DEBUG
        # print(func)  ## DEBUG

        head = func.head
        head_name = head.name
        args = func.args

        new_children = tuple(map(self._handle_node, args))
        handler = getattr(self, head_name, None)

        if handler:
            new_tree = handler(new_children)
        else:
            new_tree = WLFunction(head, new_children)

        return new_tree

    def _handle_symbol(self, symbol: WLSymbol):
        name: str = symbol.name
        # print(f"{name=}")  ## DEBUG
        return sympy.Symbol(name)

class WlTransformer(BaseTransformer):
    def _handle_symbol(self, symbol: WLSymbol):
        name: str = symbol.name
        name = remove_prefix(name, 'Global`')
        return sympy.Symbol(name)

    def Rule(self, args):
        return sympy.Eq(*args)
    def Plus(self, args):
        return sympy.Add(*args)
    def Times(self, args):
        return sympy.Mul(*args)
    def Power(self, args):
        return sympy.Pow(*args)

def extract_wolfram_solution(
        wsolution: Tuple[WLFunction],
    ) -> Dict[str, sympy.Expr]:

    results = {}

    for ri, rule in enumerate(wsolution):
        print(f"RULE {ri}:")

        wsymb, wexp = rule
        
        name = remove_prefix(wsymb.name, 'Global`')
        transf = WlTransformer()
        exp = transf.transform(wexp)

        results[name] = exp
        print(f"{name} -> {exp}")

    return results



if __name__ == '__main__':

    with WolframLanguageSession() as wsession:
        from pprint import pprint

        input_str = "Solve[{a == 1 + 25*z*a + 24*z*b + 24*z*c + 24*z*d + 24*z*e + 24*z*f + 24*z*g + 24*z*h + 25*z*i + 24*z*j + 24*z*k + 24*z*l + 24*z*m, b == z*a + z*b + z*c + z*d + z*e + z*f + z*g + z*h + z*k + z*l + z*m, c == b*z + j*z, d == c*z, e == d*z, f == e*z, g == f*z, h == g*z, i == h*z, j == i*z, k == j*z, l == k*z, m == l*z, n == m*z}, {a, b, c, d, e, f, g, h, i, j, k, l, m, n}]"

        exp = wlexpr(input_str)

        wsolutions = wsession.evaluate(exp)
        wsolution = wsolutions[0]

        solution = extract_wolfram_solution(wsolution)
