from z3 import *

# Helper function to check if a given option satisfies all constraints
def check_option_sat(order):
    solver = Solver()
    
    # Assign positions based on the order
    pos = {}
    for idx, comp in enumerate(order):
        pos[comp] = idx + 1
    
    # Constraint 1: T is immediately before F or immediately after R
    t_pos = pos['T']
    f_pos = pos['F']
    r_pos = pos['R']
    solver.add(Or(t_pos + 1 == f_pos, r_pos + 1 == t_pos))
    
    # Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
    solver.add(Abs(f_pos - r_pos) >= 3)
    
    # Constraint 3: O is performed either first or fifth
    o_pos = pos['O']
    solver.add(Or(o_pos == 1, o_pos == 5))
    
    # Constraint 4: The eighth composition performed is either L or H
    l_pos = pos['L']
    h_pos = pos['H']
    solver.add(Or(l_pos == 8, h_pos == 8))
    
    # Constraint 5: P is performed at some time before S
    p_pos = pos['P']
    s_pos = pos['S']
    solver.add(p_pos < s_pos)
    
    # Constraint 6: At least one composition is performed either after O and before S, or after S and before O
    solver.add(Abs(o_pos - s_pos) >= 2)
    
    # Check if all constraints are satisfied
    result = solver.check()
    return result == sat

# Define the options as lists of compositions in order
options = {
    "A": ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    "B": ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    "C": ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    "D": ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    "E": ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
}

# Evaluate each option
found_options = []
for letter, order in options.items():
    if check_option_sat(order):
        found_options.append(letter)

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")