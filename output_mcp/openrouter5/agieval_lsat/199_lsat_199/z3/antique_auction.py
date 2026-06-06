from z3 import *

solver = Solver()

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
days = list(range(6))

# Antiques: harmonica, lamp, mirror, sundial, table, vase
# We'll assign each antique a day (0-5)
h, l, m, s, t, v = Ints('h l m s t v')

# All distinct and in range 0..5
solver.add(Distinct(h, l, m, s, t, v))
for var in [h, l, m, s, t, v]:
    solver.add(var >= 0, var <= 5)

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(s != 0)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(h < l, m < l))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(s < m)
solver.add(s < v)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(If(t < h, 1, 0) + If(t < v, 1, 0) == 1)

# Now evaluate each option: "X CANNOT be the antique auctioned on the day
# immediately preceding the day on which the vase is auctioned."
# That means: the antique auctioned on day (v - 1) is X.
# We test: can there be a valid assignment where the antique on day (v-1) is X?
# If it's SAT, then X CAN be that antique. If UNSAT, then X CANNOT be that antique.
# We want the one that CANNOT be, i.e., the one that is UNSAT.

options = {
    "A": h,  # harmonica
    "B": l,  # lamp
    "C": m,  # mirror
    "D": s,  # sundial
    "E": t   # table
}

found_options = []
for letter, var in options.items():
    solver.push()
    # The antique on day (v-1) is the given antique.
    # We need to express: the antique whose day is v-1 equals var.
    # Since all antiques have distinct days, we can say: var == v - 1
    # But we must ensure v > 0 so v-1 is a valid day.
    solver.add(v > 0)
    solver.add(var == v - 1)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")