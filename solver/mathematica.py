
from typing import Tuple, List, Dict
import sympy

from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.serializers import export

from wolframclient.language.expression import WLFunction, WLSymbol


def remove_prefix(txt: str, prefix: str):
    if txt.startswith(prefix):
        size = len(prefix)
        return txt[size:]
    return txt


class BaseTransformer:
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

        return new_tree        # print()  ## DEBUG
        # print(func)  ## DEBUG
        return name


class WlSympyTransformer(BaseTransformer):
    _wsym_map: Dict[WLSymbol, sympy.Symbol]
    _sym_per_name: Dict[str, sympy.Symbol]

    def __init__(self):
        self._wsym_map = {}
        self._sym_per_name = {}

    def get_symbols(self) -> Dict[str, sympy.Symbol]:
        return dict(self._sym_per_name)

    def _make_symbol(self, wsym: WLSymbol):
        name: str = wsym.name
        name = remove_prefix(name, 'Global`')
        sym = sympy.Symbol(name)
        self._wsym_map[wsym] = sym
        self._sym_per_name[name] = sym
        return sym

    def _handle_symbol(self, wsym: WLSymbol):
        sym = self._wsym_map.get(wsym, None)
        if sym is None:
            sym = self._make_symbol(wsym)
        return sym

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
    ) -> Tuple[Dict[str, sympy.Symbol], Dict[str, sympy.Expr]]:

    transformer = WlSympyTransformer()

    results = {}
    for ri, rule in enumerate(wsolution):
        # print(f"RULE {ri}:")  ## DEBUG

        wsymb, wexp = rule
        var_name = remove_prefix(wsymb.name, 'Global`')

        exp = transformer.transform(wexp)

        results[var_name] = exp
        # print(f"{var_name} -> {exp}")  ## DEBUG
        # print()  ## DEBUG

    symbs = transformer.get_symbols()
    # print(symbs)  ## DEBUG

    return symbs, results


WOLFRAM_SOLVE_TEMPLATE = "Solve[ {{ {eqs} }}, {{ {syms} }} ]"

def txt_eq(eq_item):
    lhs, rhs = eq_item
    return " == ".join(map(str, (lhs, rhs)))

def build_wsystem_txt(
        syms: List[sympy.Symbol],
        eq_map: Dict[sympy.Symbol, sympy.Expr],
    ):

    txt_syms = ", ".join(map(str, syms))
    txt_eqs = ", ".join(map(txt_eq, eq_map.items()))

    wex = WOLFRAM_SOLVE_TEMPLATE.format( eqs=txt_eqs, syms=txt_syms )
    return wex

def solve_system(
        syms: List[sympy.Symbol],
        eq_map: Dict[sympy.Symbol, sympy.Expr],
    ):
    wex_txt = build_wsystem_txt(syms, eq_map)

    with WolframLanguageSession() as wsession:
        wexp = wlexpr(wex_txt)

        wsolutions = wsession.evaluate(wexp)
        wsolution, *_ = wsolutions

        ressyms, results = extract_wolfram_solution(wsolution)

    return ressyms, results


if __name__ == '__main__':
    from pprint import pprint

    # Entrada para o do Wolfram hardcodeada
    input_str = """
        Solve[{
            s0 == 1 + 25*z*s0 + 24*z*s1 + 24*z*s2 + 24*z*s3 + 24*z*s4 + 24*z*s5 + 24*z*s6 + 24*z*s7 + 25*z*s8 + 24*z*s9 + 24*z*s10 + 24*z*s11 + 24*z*s12,
            s1 == z*s0 + z*s1 + z*s2 + z*s3 + z*s4 + z*s5 + z*s6 + z*s7 + z*s10 + z*s11 + z*s12,
            s2 == s1*z + s9*z,
            s3 == s2*z,
            s4 == s3*z,
            s5 == s4*z,
            s6 == s5*z,
            s7 == s6*z,
            s8 == s7*z,
            s9 == s8*z,
            s10 == s9*z,
            s11 == s10*z,
            s12 == s11*z,
            s13 == s12*z
        }, {s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13}]
        """


    # Criando entrada para o Wolfram a partir de expressões do SymPy

    z = sympy.Symbol('z')
    s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13 = st_syms = (
        sympy.symbols('s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13')
    )

    # Mapeia cada símbolo referente a uma variável (que representará uma função
    # geradora e fica do lado esquerdo) e uma expressão da equação (lado direito)
    eq_map = {
        s0 : 1 + 25*z*s0 + 24*z*s1 + 24*z*s2 + 24*z*s3 + 24*z*s4 + 24*z*s5 + 24*z*s6 + 24*z*s7 + 25*z*s8 + 24*z*s9 + 24*z*s10 + 24*z*s11 + 24*z*s12,
        s1 : z*s0 + z*s1 + z*s2 + z*s3 + z*s4 + z*s5 + z*s6 + z*s7 + z*s10 + z*s11 + z*s12,
        s2 : s1*z + s9*z,
        s3 : s2*z,
        s4 : s3*z,
        s5 : s4*z,
        s6 : s5*z,
        s7 : s6*z,
        s8 : s7*z,
        s9 : s8*z,
        s10: s9*z,
        s11: s10*z,
        s12: s11*z,
        s13: s12*z,
    }


    built_winput = build_wsystem_txt(st_syms, eq_map)

    ressyms, results = solve_system(st_syms, eq_map)
    print(ressyms)

    for s, ex in results.items():
        print('\n')
        print(f'{s}:')
        sympy.pprint(ex)
