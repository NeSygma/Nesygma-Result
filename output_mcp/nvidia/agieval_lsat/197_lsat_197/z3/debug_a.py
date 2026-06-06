from z3 import *

solver = Solver()

# Declare variables
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')

# Base constraints
solver.add(sundial != 0)  # not June 1
solver.add(Implies(harmonica < lamp, mirror < lamp))
solver.add(sundial < mirror)
solver.add(sundial < vase)
solver.add(Xor(table < harmonica, table < vase))
solver.add(Distinct([harmonica, lamp, mirror, sundial, table, vase]))

# Option A constraints
solver.add(table == 1)
solver.add(lamp == 2)

# Check
result = solver.check()
print("Result:", result)
if result == sat:
    m = solver.model()
    print("Model:")
    print("harmonica =", m[harmonica])
    print("lamp =", m[lamp])
    print("mirror =", m[mirror])
    print("sundial =", m[sundial])
    print("table =", m[table])
    print("vase =", m[vase])