
from typing import Tuple, List, Dict

import sympy
from sympy import Symbol, Expr

from wolframclient.language import wlexpr
from wolframclient.evaluation import WolframLanguageSession
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
            return self._handle_function(tree)
        elif isinstance(tree, WLSymbol):
            return self._handle_symbol(tree)
        else:
            return tree

    def _handle_function(self, func: WLFunction):
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

    def _handle_symbol(self, wsym: WLSymbol):
        name: str = wsym.name
        return name


class WlSympyTransformer(BaseTransformer):
    _wsym_map: Dict[WLSymbol, Symbol]
    _sym_per_name: Dict[str, Symbol]

    def __init__(self):
        self._wsym_map = {}
        self._sym_per_name = {}

    def get_symbols(self) -> Dict[str, Symbol]:
        return dict(self._sym_per_name)

    def _make_symbol(self, wsym: WLSymbol):
        name: str = wsym.name
        name = remove_prefix(name, 'Global`')
        sym = Symbol(name)
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
    ) -> Tuple[Dict[str, Symbol], Dict[str, Expr]]:

    transformer = WlSympyTransformer()

    results = {}
    for rule in wsolution:
        wsymb, wexp = rule
        exp = transformer.transform(wexp)

        var_name = remove_prefix(wsymb.name, 'Global`')
        results[var_name] = exp

    symb_map = transformer.get_symbols()

    return symb_map, results


WOLFRAM_SOLVE_TEMPLATE = "Solve[ {{ {eqs} }}, {{ {syms} }} ]"

def txt_eq(eq_item):
    lhs, rhs = eq_item
    return " == ".join(map(str, (lhs, rhs)))

def build_wsystem_txt(
        syms: List[Symbol],
        eq_map: Dict[Symbol, Expr],
    ):

    txt_syms = ", ".join(map(str, syms))
    txt_eqs = ", ".join(map(txt_eq, eq_map.items()))

    wex = WOLFRAM_SOLVE_TEMPLATE.format( eqs=txt_eqs, syms=txt_syms )
    return wex

def solve_system(
        z: Symbol,
        st_syms: List[Symbol],
        eq_map: Dict[Symbol, Expr],
    ) -> Tuple[Symbol, Dict[Symbol, Expr]]:

    sym_for_name = { v.name: v for v in st_syms }

    wex_txt = build_wsystem_txt(st_syms, eq_map)
    wexp = wlexpr(wex_txt)

    with WolframLanguageSession() as wsession:
        wsolutions = wsession.evaluate(wexp)
        wsolution, *_ = wsolutions
        res_sym_map, _results = extract_wolfram_solution(wsolution)

    res_z = res_sym_map[z.name]

    results = {
        sym_for_name[sym_name]: result
        for sym_name, result
        in _results.items()
    }

    return res_z, results


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

    z = Symbol('z')
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

    z, results = solve_system(z, st_syms, eq_map)

    for s, ex in results.items():
        print('\n')
        print(f'{s}:')
        sympy.pprint(ex)
