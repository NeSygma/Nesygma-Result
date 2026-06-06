from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare shelf variables for each book
# 0 = Top, 1 = Middle, 2 = Bottom
shelves = {
    'F': Int('F'),
    'G': Int('G'),
    'H': Int('H'),
    'I': Int('I'),
    'K': Int('K'),
    'L': Int('L'),
    'M': Int('M'),
    'O': Int('O'),
}

# Base constraints
solver = Solver()

# Each book is on exactly one shelf
for book in shelves:
    solver.add(Or(shelves[book] == 0, shelves[book] == 1, shelves[book] == 2))

# At least two books on each shelf
solver.add(Sum([If(shelves[b] == 0, 1, 0) for b in shelves]) >= 2)
solver.add(Sum([If(shelves[b] == 1, 1, 0) for b in shelves]) >= 2)
solver.add(Sum([If(shelves[b] == 2, 1, 0) for b in shelves]) >= 2)

# More books on the bottom shelf than the top shelf
solver.add(Sum([If(shelves[b] == 2, 1, 0) for b in shelves]) > Sum([If(shelves[b] == 0, 1, 0) for b in shelves]))

# I is on the middle shelf
solver.add(shelves['I'] == 1)

# K is on a higher shelf than F
solver.add(shelves['K'] > shelves['F'])

# O is on a higher shelf than L
solver.add(shelves['O'] > shelves['L'])

# F is on the same shelf as M
solver.add(shelves['F'] == shelves['M'])

# Define the options as constraints on the bottom shelf (shelf 2)
# Option A: F, M on bottom shelf
opt_a_constr = And(
    shelves['F'] == 2,
    shelves['M'] == 2
)

# Option B: F, H, M on bottom shelf
opt_b_constr = And(
    shelves['F'] == 2,
    shelves['H'] == 2,
    shelves['M'] == 2
)

# Option C: G, H, K on bottom shelf
opt_c_constr = And(
    shelves['G'] == 2,
    shelves['H'] == 2,
    shelves['K'] == 2
)

# Option D: F, G, M, O on bottom shelf
opt_d_constr = And(
    shelves['F'] == 2,
    shelves['G'] == 2,
    shelves['M'] == 2,
    shelves['O'] == 2
)

# Option E: G, H, L, M on bottom shelf
opt_e_constr = And(
    shelves['G'] == 2,
    shelves['H'] == 2,
    shelves['L'] == 2,
    shelves['M'] == 2
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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