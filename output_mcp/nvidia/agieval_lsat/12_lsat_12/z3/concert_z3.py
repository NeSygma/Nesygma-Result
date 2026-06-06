from z3 import *
solver = Solver()

# Declare integer variables for each composition
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

# All positions must be distinct
solver.add(Distinct([F, H, L, O, P, R, S, T]))

# Global constraints
global_constraints = And(
    Or(T + 1 == F, R + 1 == T),                # T immediately before F or after R
    Or(F >= R + 3, R >= F + 3),                # at least two between F and R
    Or(O == 0, O == 4),                        # O is first or fifth
    Or(L == 7, H == 7),                        # eighth is L or H
    P < S,                                     # P before S
    Or(O >= S + 2, S >= O + 2)                 # at least one between O and S
)

# Define the ordering equalities for each option
option_equalities = {
    'A': [L == 0, P == 1, S == 2, R == 3, O == 4, T == 5, F == 6, H == 7],
    'B': [O == 0, T == 1, P == 2, F == 3, S == 4, H == 5, R == 6, L == 7],
    'C': [P == 0, T == 1, F == 2, S == 3, L == 4, R == 5, O == 6, H == 7],
    'D': [P == 0, T == 1, F == 2, S == 3, O == 4, R == 5, L == 6, H == 7],
    'E': [T == 0, F == 1, P == 2, R == 3, O == 4, L == 5, S == 6, H == 7]
}

found_options = []
for letter, equalities in option_equalities.items():
    solver.push()
    # Add the equalities for this option
    solver.add(And(*equalities))
    # Also add the global constraints
    solver.add(global_constraints)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')