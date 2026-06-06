from z3 import *

solver = Solver()

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
days = list(range(6))

# Antiques: harmonica, lamp, mirror, sundial, table, vase
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

# Now test each option: X CANNOT be the antique on the day immediately before vase.
# That means: there is NO valid model where X == v - 1.
# We want the option that is UNSAT (impossible).

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
    # vase must be at least day 1 so that v-1 >= 0
    solver.add(v >= 1)
    solver.add(var == v - 1)
    res = solver.check()
    if res == sat:
        found_options.append(letter)
        mod = solver.model()
        print(f"Option {letter} ({var}): SAT")
        print(f"  h={mod.eval(h)}, l={mod.eval(l)}, m={mod.eval(m)}, s={mod.eval(s)}, t={mod.eval(t)}, v={mod.eval(v)}")
    else:
        print(f"Option {letter} ({var}): UNSAT")
    solver.pop()

print(f"\nFound options (CAN be immediately before vase): {found_options}")

# The answer is the one that CANNOT be, i.e., the one NOT in found_options
all_letters = ["A", "B", "C", "D", "E"]
cannot_be = [x for x in all_letters if x not in found_options]

if len(cannot_be) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be[0]}")
elif len(cannot_be) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be {cannot_be}")
else:
    print("STATUS: unsat")
    print("Refine: No options found (all can be)")