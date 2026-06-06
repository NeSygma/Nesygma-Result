from z3 import *
Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon = Ints('Uneasy Vegemite Wellspring Xpert Yardsign Zircon')
solver = Solver()
for b in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]:
    solver.add(b>=1, b<=6)
solver.add(Distinct(Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon))
solver.add(Vegemite < Zircon)
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)
solver.add(Uneasy >=4)
solver.add(Yardsign <=3)
solver.add(Zircon + 1 == Wellspring)
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m[v].as_long() for v in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]}
    solutions.append(sol)
    # block
    solver.add(Or([v != m[v] for v in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]]))
print('total', len(solutions))
for s in solutions:
    print(s)