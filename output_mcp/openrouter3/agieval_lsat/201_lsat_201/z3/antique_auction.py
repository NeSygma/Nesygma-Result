from z3 import *

# Create solver
solver = Solver()

# Days: 1 to 6
days = [1, 2, 3, 4, 5, 6]

# Antiques
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Create variables: each antique gets a day
h = Int('harmonica')
l = Int('lamp')
m = Int('mirror')
s = Int('sundial')
t = Int('table')
v = Int('vase')

# All antiques must be on different days (1-6)
all_ants = [h, l, m, s, t, v]
solver.add(Distinct(all_ants))
for ant in all_ants:
    solver.add(ant >= 1, ant <= 6)

# Constraint 1: Sundial is not auctioned on June 1st
solver.add(s != 1)

# Constraint 2: If harmonica < lamp, then mirror < lamp
# This is: (h < l) => (m < l)
solver.add(Implies(h < l, m < l))

# Constraint 3: Sundial < mirror AND sundial < vase
solver.add(s < m)
solver.add(s < v)

# Constraint 4: Table < harmonica XOR table < vase
# Exactly one of these is true
solver.add(Or(And(t < h, Not(t < v)), And(Not(t < h), t < v)))

# Now test each option
found_options = []

# Option A: The sundial is auctioned on June 5th
opt_a = (s == 5)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The sundial is auctioned on June 4th
opt_b = (s == 4)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The lamp is auctioned on June 5th and the mirror is auctioned on June 6th
opt_c = And(l == 5, m == 6)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The table is auctioned on June 3rd and the lamp is auctioned on June 4th
opt_d = And(t == 3, l == 4)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The harmonica is auctioned on June 2nd and the vase is auctioned on June 3rd
opt_e = And(h == 2, v == 3)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")