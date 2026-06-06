from z3 import *

# Buildings: G(1), Y(3), Z(3), F(1), L(2), K(2), M(2), O(2)
# Owners: R, S, T
# Initial: G:R, Y:R, Z:R, F:S, L:S, K:T, M:T, O:T

# We need to model the state transitions and find which option is always true.
# Since the number of states is small (16 final states), we can just check the options.

# The previous script found 16 final states.
# Let's re-verify the options for all 16 states.

final_states = [
    ('S', 'S', 'S', 'T', 'R', 'T', 'R', 'R'),
    ('S', 'T', 'T', 'T', 'S', 'R', 'R', 'R'),
    ('T', 'S', 'S', 'S', 'T', 'R', 'R', 'R'),
    ('S', 'S', 'S', 'T', 'R', 'R', 'T', 'R'),
    ('S', 'S', 'S', 'T', 'T', 'R', 'R', 'R'),
    ('T', 'S', 'S', 'S', 'R', 'R', 'R', 'T'),
    ('S', 'T', 'T', 'T', 'R', 'S', 'R', 'R'),
    ('T', 'S', 'S', 'S', 'R', 'T', 'R', 'R'),
    ('S', 'S', 'S', 'T', 'R', 'R', 'R', 'T'),
    ('S', 'T', 'T', 'T', 'R', 'R', 'R', 'S'),
    ('T', 'T', 'T', 'S', 'R', 'R', 'S', 'R'),
    ('S', 'T', 'T', 'T', 'R', 'R', 'S', 'R'),
    ('T', 'T', 'T', 'S', 'R', 'S', 'R', 'R'),
    ('T', 'S', 'S', 'S', 'R', 'R', 'T', 'R'),
    ('T', 'T', 'T', 'S', 'S', 'R', 'R', 'R'),
    ('T', 'T', 'T', 'S', 'R', 'R', 'R', 'S')
]

# Buildings: G, Y, Z, F, L, K, M, O
# Classes: G:1, Y:3, Z:3, F:1, L:2, K:2, M:2, O:2

def check_options():
    results = {'A': True, 'B': True, 'C': True, 'D': True, 'E': True}
    
    for s in final_states:
        owners = {'G':s[0], 'Y':s[1], 'Z':s[2], 'F':s[3], 'L':s[4], 'K':s[5], 'M':s[6], 'O':s[7]}
        
        # (A) Trustcorp owns a class 1 building.
        a = (owners['G'] == 'T' or owners['F'] == 'T')
        if not a: results['A'] = False
        
        # (B) Trustcorp owns the Meyer Building.
        b = (owners['M'] == 'T')
        if not b: results['B'] = False
        
        # (C) Southco owns a class 2 Building.
        c = (owners['L'] == 'S' or owners['K'] == 'S' or owners['M'] == 'S' or owners['O'] == 'S')
        if not c: results['C'] = False
        
        # (D) Southco owns both of the class 3 buildings.
        d = (owners['Y'] == 'S' and owners['Z'] == 'S')
        if not d: results['D'] = False
        
        # (E) Southco owns the Flores Tower.
        e = (owners['F'] == 'S')
        if not e: results['E'] = False
        
    print(results)

check_options()