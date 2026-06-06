from z3 import *

def get_base_solver():
    solver = Solver()
    
    # Compositions: F, H, L, O, P, R, S, T
    # Their positions: 1 to 8
    pos = {}
    names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
    for name in names:
        pos[name] = Int(f'pos_{name}')
        solver.add(pos[name] >= 1, pos[name] <= 8)
    
    # All positions are distinct
    solver.add(Distinct([pos[name] for name in names]))
    
    # Constraint 1: T is performed either immediately before F or immediately after R.
    solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))
    
    # Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
    solver.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))
    
    # Constraint 3: O is performed either first or fifth.
    solver.add(Or(pos['O'] == 1, pos['O'] == 5))
    
    # Constraint 4: The eighth composition performed is either L or H.
    solver.add(Or(pos['L'] == 8, pos['H'] == 8))
    
    # Constraint 5: P is performed at some time before S.
    solver.add(pos['P'] < pos['S'])
    
    # Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
    solver.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))
    
    # Additional condition: O is performed immediately after T
    solver.add(pos['T'] + 1 == pos['O'])
    
    return solver, pos, names

# First, find all possible positions for F
solver, pos, names = get_base_solver()
possible_f_positions = set()

while solver.check() == sat:
    m = solver.model()
    f_pos = m.eval(pos['F']).as_long()
    possible_f_positions.add(f_pos)
    solver.add(Or([pos[name] != m.eval(pos[name]).as_long() for name in names]))

print(f"Possible positions for F: {sorted(possible_f_positions)}")

# Now test each option with a fresh solver
options = {
    'A': {1, 2},
    'B': {2, 3},
    'C': {4, 6},
    'D': {4, 7},
    'E': {6, 7}
}

found_options = []
for letter, pos_set in options.items():
    s, p, _ = get_base_solver()
    # Try to find a solution where F is NOT in the given set
    # If unsat, then F must be in the given set
    s.add(And([p['F'] != v for v in pos_set]))
    if s.check() == unsat:
        found_options.append(letter)
    
print(f"Options where F must be in the given positions: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    # Find which one exactly matches
    for letter, pos_set in options.items():
        if possible_f_positions == pos_set:
            print(f"Exact match found: {letter}")
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")