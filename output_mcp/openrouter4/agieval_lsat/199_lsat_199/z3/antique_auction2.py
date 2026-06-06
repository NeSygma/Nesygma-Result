from z3 import *

solver = Solver()

# Antiques: positions 1 through 6 (June 1st to June 6th)
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')

# All distinct and in range 1-6
antiques = [harmonica, lamp, mirror, sundial, table, vase]
solver.add(Distinct(antiques))
for a in antiques:
    solver.add(a >= 1, a <= 6)

# Constraint 1: Sundial is not auctioned on June 1st
solver.add(sundial != 1)

# Constraint 2: If harmonica is earlier than lamp, then mirror is also earlier than lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: Sundial is earlier than mirror and earlier than vase
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: Table is earlier than harmonica OR earlier than vase, but not both
# XOR: (table < harmonica) != (table < vase)
solver.add((table < harmonica) != (table < vase))

# The question asks: Which CANNOT be the antique auctioned on the day immediately preceding the vase?
# We test each option: if the option being the predecessor leads to UNSAT, it CANNOT be.
# We want exactly one such option.

impossible_options = []

for letter, constr in [
    ("A", harmonica + 1 == vase),
    ("B", lamp + 1 == vase),
    ("C", mirror + 1 == vase),
    ("D", sundial + 1 == vase),
    ("E", table + 1 == vase)
]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")