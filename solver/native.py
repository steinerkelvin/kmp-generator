
from typing import Tuple, List, Dict
from itertools import starmap
import sympy
from sympy import Symbol, Expr


def solve_system(
        z: Symbol,
        st_syms: List[Symbol],
        eq_map: Dict[Symbol, Expr],
    ) -> Tuple[Symbol, Dict[Symbol, Expr]]:

    eqs = list(starmap( sympy.Eq, eq_map.items() ))
    sols = sympy.solve(eqs, st_syms)
    return z, sols
