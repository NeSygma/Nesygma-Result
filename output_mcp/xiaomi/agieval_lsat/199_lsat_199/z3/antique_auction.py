from z3 import *

solver = Solver()

# Days: 1=June1, 2=June2, ..., 6=June6
# Antiques: harmonica, lamp, mirror, sundial, table, vase
# Each antique is assigned to a unique day

h = Int('h')  # harmonica
l = Int('l')  # lamp
m = Int('m')  # mirror
s = Int('s')  # sundial
t = Int('t')  # table
v = Int('v')  # vase

antiques = [h, l, m, s, t, v]

# Each antique on a unique day 1-6
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(s != 1)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(h < l, m < l))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(s < m)
solver.add(s < v)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(Or(And(t < h, Not(t < v)), And(Not(t < h), t < v)))

# Now test each option: which antique CANNOT immediately precede the vase?
# "immediately preceding" means the antique's day == vase's day - 1

found_options = []

# (A) the harmonica immediately precedes the vase
solver.push()
solver.add(h == v - 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) the lamp immediately precedes the vase
solver.push()
solver.add(l == v - 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) the mirror immediately precedes the vase
solver.push()
solver.add(m == v - 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) the sundial immediately precedes the vase
solver.push()
solver.add(s == v - 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) the table immediately precedes the vase
solver.push()
solver.add(t == v - 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# The question asks which CANNOT be the antique immediately preceding the vase.
# So we want the option that is NOT in found_options (i.e., unsatisfiable).
# But per the skeleton, we report which CAN be done. The answer is the one NOT found.
cannot_options = [l for l in ["A","B","C","D","E"] if l not in found_options]

print(f"Options that CAN precede vase: {found_options}")
print(f"Options that CANNOT precede vase: {cannot_options}")

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: All options possible")