from z3 import *
import itertools

# Define bands and slots
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
slot_vars = {b: Int(f'slot_{b}') for b in bands}

# Base constraints (excluding the constraint to be substituted)
base_constraints = [
    slot_vars['V'] < slot_vars['Z'],  # Vegemite before Zircon
    Or(slot_vars['U'] == 4, slot_vars['U'] == 5, slot_vars['U'] == 6),  # Uneasy in last three
    Or(slot_vars['Y'] == 1, slot_vars['Y'] == 2, slot_vars['Y'] == 3),  # Yardsign in first three
    Distinct([slot_vars[b] for b in bands]),  # All slots distinct
    And([slot_vars[b] >= 1 for b in bands]),  # Slots between 1 and 6
    And([slot_vars[b] <= 6 for b in bands])
]

# Original constraint to be substituted
original_constraint = And(
    slot_vars['W'] < slot_vars['X'],
    slot_vars['Z'] < slot_vars['X']
)

# Option constraints
opt_a = And(
    slot_vars['V'] <= slot_vars['X'],
    slot_vars['W'] <= slot_vars['X'],
    slot_vars['Y'] <= slot_vars['X'],
    slot_vars['Z'] <= slot_vars['X']
)
opt_b = And(
    slot_vars['V'] < slot_vars['W'],
    slot_vars['W'] < slot_vars['Z']
)
opt_c = And(
    slot_vars['V'] < slot_vars['X'],
    slot_vars['W'] < slot_vars['X']
)
opt_d = Or(
    slot_vars['X'] == slot_vars['U'] - 1,
    slot_vars['X'] == slot_vars['U'] + 1
)
opt_e = Or(
    slot_vars['X'] == 5,
    slot_vars['X'] == 6
)

# Function to find all solutions for a given set of constraints
def find_all_solutions(constraints):
    s = Solver()
    s.add(constraints)
    solutions = []
    while s.check() == sat:
        m = s.model()
        # Capture the assignment as a tuple of slot values for each band in fixed order
        sol = tuple(m[slot_vars[b]].as_long() for b in bands)
        solutions.append(sol)
        # Block this solution
        s.add(Or([slot_vars[b] != m[slot_vars[b]] for b in bands]))
    return solutions

# Find solutions for original constraints
original_solutions = find_all_solutions(base_constraints + [original_constraint])
print(f"Original solutions count: {len(original_solutions)}")

# Find solutions for each option
option_solutions = {}
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    sols = find_all_solutions(base_constraints + [constr])
    option_solutions[letter] = sols
    print(f"Option {letter} solutions count: {len(sols)}")

# Compare sets
found_options = []
for letter, sols in option_solutions.items():
    if set(sols) == set(original_solutions):
        found_options.append(letter)

# Output using the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")