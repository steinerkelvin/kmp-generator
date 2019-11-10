
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.serializers import export

input_str = "Solve[{a == 1 + 25*z*a + 24*z*b + 24*z*c + 24*z*d + 24*z*e + 24*z*f + 24*z*g + 24*z*h + 25*z*i + 24*z*j + 24*z*k + 24*z*l + 24*z*m, b == z*a + z*b + z*c + z*d + z*e + z*f + z*g + z*h + z*k + z*l + z*m, c == b*z + j*z, d == c*z, e == d*z, f == e*z, g == f*z, h == g*z, i == h*z, j == i*z, k == j*z, l == k*z, m == l*z, n == m*z}, {a, b, c, d, e, f, g, h, i, j, k, l, m, n}]"

with WolframLanguageSession() as session:

    exp = wlexpr(input_str)
    print(exp)

    result = session.evaluate(exp)
    eq = result[0][1]
    print(eq)

    # print(export(eq, target_format = "wl"))
