from z3 import *

# Buildings in order: Garza Tower, Yates House, Zimmer House, Flores Tower, Lynch Building, King Building, Meyer Building, Ortiz Building
buildings = ["Garza", "Yates", "Zimmer", "Flores", "Lynch", "King", "Meyer", "Ortiz"]
classes = [1, 3, 3, 1, 2, 2, 2, 2]  # class 1,2,3
values = [4 if c == 1 else 2 if c == 2 else 1 for c in classes]  # value weights

# Companies: 0 = RealProp, 1 = Southco, 2 = Trustcorp
owner = [Int(f'owner_{i}') for i in range(8)]

solver = Solver()

# Each building owned by exactly one company (0,1,2)
for i in range(8):
    solver.add(Or(owner[i] == 0, owner[i] == 1, owner[i] == 2))

# Compute total value per company
def total_value(company):
    return Sum([If(owner[i] == company, values[i], 0) for i in range(8)])

# Each company must have total value 6
for c in range(3):
    solver.add(total_value(c) == 6)

# Define option constraints: for each option, we add the condition that the option is true.
# Option A: RealProp owns Lynch, Meyer, Ortiz (indices 5,6,7) and no others.
opt_a = And(
    owner[5] == 0, owner[6] == 0, owner[7] == 0,
    *[owner[i] != 0 for i in range(8) if i not in [5,6,7]]
)

# Option B: Southco owns Garza (0) and Meyer (6)
opt_b = And(
    owner[0] == 1, owner[6] == 1,
    *[owner[i] != 1 for i in range(8) if i not in [0,6]]
)

# Option C: Southco owns King (5), Meyer (6), Ortiz (7)
opt_c = And(
    owner[5] == 1, owner[6] == 1, owner[7] == 1,
    *[owner[i] != 1 for i in range(8) if i not in [5,6,7]]
)

# Option D: Trustcorp owns Flores (3) and Yates (1)
opt_d = And(
    owner[3] == 2, owner[1] == 2,
    *[owner[i] != 2 for i in range(8) if i not in [1,3]]
)

# Option E: Trustcorp owns Garza (0) and Lynch (5)
opt_e = And(
    owner[0] == 2, owner[5] == 2,
    *[owner[i] != 2 for i in range(8) if i not in [0,5]]
)

# Use the exact skeleton for multiple choice evaluation
found_options = []
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# According to the skeleton, if exactly one option is sat, that is the answer.
# But here we want the option that CANNOT be true, i.e., the one that is unsat.
# So we need to invert: the correct answer is the one NOT in found_options.
# However, the skeleton expects exactly one sat option. In this problem, four options are possible, one is not.
# So found_options will have four letters, which triggers the "Multiple options found" case.
# To adhere to the skeleton, we can instead collect unsat options.
# Let's modify: we'll collect unsat options by checking unsat.
unsat_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")