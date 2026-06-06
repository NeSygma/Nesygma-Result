from z3 import *

solver = Solver()

# Paintings: 0=F_O, 1=F_W, 2=G_O, 3=G_W, 4=H_O, 5=H_W, 6=I_O, 7=I_W
# Walls: 0,1,2,3 (corresponding to walls 1,2,3,4)
# Each wall has upper and lower position

upper = [Int(f'upper_{w}') for w in range(4)]
lower = [Int(f'lower_{w}') for w in range(4)]

# Each position holds a painting 0-7
for w in range(4):
    solver.add(upper[w] >= 0, upper[w] <= 7)
    solver.add(lower[w] >= 0, lower[w] <= 7)

# All 8 paintings used exactly once
all_positions = upper + lower
solver.add(Distinct(all_positions))

# Constraint 1: No wall has only watercolors (paintings 1,3,5,7 are watercolors)
# Each wall must have at least one oil painting (0,2,4,6)
for w in range(4):
    # painting is oil iff painting % 2 == 0
    solver.add(Or(upper[w] % 2 == 0, lower[w] % 2 == 0))

# Constraint 2: No wall has work of only one student
# Student of painting p: p // 2 (0=F, 1=G, 2=H, 3=I)
for w in range(4):
    solver.add(upper[w] / 2 != lower[w] / 2)

# Constraint 3: No wall has both Franz (0,1) and Isaacs (6,7)
for w in range(4):
    u_is_franz = Or(upper[w] == 0, upper[w] == 1)
    u_is_isaacs = Or(upper[w] == 6, upper[w] == 7)
    l_is_franz = Or(lower[w] == 0, lower[w] == 1)
    l_is_isaacs = Or(lower[w] == 6, lower[w] == 7)
    solver.add(Not(And(u_is_franz, l_is_isaacs)))
    solver.add(Not(And(u_is_isaacs, l_is_franz)))

# Constraint 4: Greene's watercolor (3) is in upper position of wall where Franz's oil (0) is
# So there exists wall w: upper[w] == 3 and lower[w] == 0
solver.add(Or([And(upper[w] == 3, lower[w] == 0) for w in range(4)]))

# Constraint 5: Isaacs's oil (6) is in lower position of wall 4 (index 3)
solver.add(lower[3] == 6)

# Answer choices for lower positions on walls 1-4:
# (A) F_O=0, F_W=1, G_O=2, I_O=6
# (B) F_O=0, H_W=5, I_W=7, I_O=6
# (C) G_O=2, F_O=0, I_O=6, H_O=4
# (D) H_O=4, G_O=2, G_W=3, I_O=6
# (E) H_W=5, F_O=0, G_O=2, I_O=6

options = {
    "A": [0, 1, 2, 6],
    "B": [0, 5, 7, 6],
    "C": [2, 0, 6, 4],
    "D": [4, 2, 3, 6],
    "E": [5, 0, 2, 6],
}

found_options = []
for letter, lower_vals in options.items():
    solver.push()
    for w in range(4):
        solver.add(lower[w] == lower_vals[w])
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for w in range(4):
            print(f"  Wall {w+1}: upper={m[upper[w]]}, lower={m[lower[w]]}")
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