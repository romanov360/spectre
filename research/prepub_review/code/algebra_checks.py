"""Exact checks of the algebraic numbers quoted in the paper (twist, s*, mu, lambda, nu)."""
import sympy as sp
x = sp.symbols('x')
s3, s5, s15 = sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)
tan = (5 * s3 - 6) / 13
cos2 = (1 - tan ** 2) / (1 + tan ** 2)
print("cos 2theta from tan formula == (4+3sqrt3)/10:", sp.simplify(cos2 - (4 + 3 * s3) / 10) == 0)
print("theta_S degrees:", sp.N(sp.atan(tan) * 180 / sp.pi, 12))
c2 = (4 + 3 * s3) / 10
print("minpoly cos2theta:", sp.minimal_polynomial(c2, x))
cos_t = sp.sqrt((1 + c2) / 2)
print("minpoly cos theta:", sp.minimal_polynomial(cos_t, x))
sin2 = 2 * tan / (1 + tan ** 2)
e = sp.nsimplify(sp.simplify(c2 - sp.I * sin2))
print("e^{-2i theta} =", sp.simplify(c2), "-i*", sp.simplify(sin2), " ; paper: (4+3sqrt3 + i(3-4sqrt3))/10 ->",
      sp.simplify(-sin2 - (3 - 4 * s3) / 10) == 0)
lam = sp.sqrt(4 + s15)
nu = 2 + s5
print("lam == (sqrt6+sqrt10)/2:", sp.simplify(lam ** 2 - ((sp.sqrt(6) + sp.sqrt(10)) / 2) ** 2) == 0)
print("minpoly lam:", sp.minimal_polynomial(lam, x))
print("(lam-1/lam)^2, (lam+1/lam)^2:", sp.simplify((lam - 1 / lam) ** 2), sp.simplify((lam + 1 / lam) ** 2))
print("lam^-4 = (4-sqrt15)^2:", sp.N((4 - s15) ** 2, 8))
mu = (4 + s15) / nu
print("minpoly mu:", sp.minimal_polynomial(mu, x), " mu =", sp.N(mu, 6))
print("s* =", sp.N(1 - sp.log(nu) / sp.log(4 + s15), 13), " D_b =", sp.N(sp.log(nu) / sp.log(lam), 13))
print("window dim =", sp.N(sp.log(5 + 2 * sp.sqrt(6)) / sp.log(4 + s15), 10),
      " (sqrt2+sqrt3)^2 =", sp.simplify(sp.expand((sp.sqrt(2) + s3) ** 2)), " minpoly sqrt2+sqrt3:",
      sp.minimal_polynomial(sp.sqrt(2) + s3, x))
print("Lucas: minpoly phi^3, phi^4:", sp.minimal_polynomial(((1 + s5) / 2) ** 3, x), sp.minimal_polynomial(((1 + s5) / 2) ** 4, x))
print("rem chi_M by x^2-4x-1:", sp.rem(x**5*(x-1)*(x+1)*(x**2-8*x+1), x**2-4*x-1), "; chi_H:", sp.rem((x-1)*(x+1)*(x**2-7*x+1), x**2-4*x-1))
print("F(n+6) == 4F(n+3)+F(n):", all(sp.fibonacci(n + 6) == 4 * sp.fibonacci(n + 3) + sp.fibonacci(n) for n in range(40)))
print("c^2 candidate root of 400x^4-1200x^3+840x^2-180x+9:",
      sp.simplify((400*x**4-1200*x**3+840*x**2-180*x+9).subs(x, (15+5*s3+3*s5+3*s15)/20)) == 0,
      sp.N((15+5*s3+3*s5+3*s15)/20, 6), " sqrt:", sp.N(sp.sqrt((15+5*s3+3*s5+3*s15)/20), 6))
