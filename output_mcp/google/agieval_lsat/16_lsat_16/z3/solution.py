from z3 import *

def solve():
    solver = Solver()
    
    # Compositions
    comp_names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
    pos = {c: Int(f'pos_{c}') for c in comp_names}
    
    # Positions are 1-8
    for c in comp_names:
        solver.add(pos[c] >= 1, pos[c] <= 8)
    
    # Each performed exactly once
    solver.add(Distinct([pos[c] for c in comp_names]))
    
    # 1. T is immediately before F or immediately after R
    solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))
    
    # 2. At least two compositions between F and R (|pos(F) - pos(R)| >= 3)
    solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))
    
    # 3. O is 1st or 5th
    solver.add(Or(pos['O'] == 1, pos['O'] == 5))
    
    # 4. 8th is L or H
    solver.add(Or(pos['L'] == 8, pos['H'] == 8))
    
    # 5. P is before S
    solver.add(pos['P'] < pos['S'])
    
    # 6. At least one composition between O and S (|pos(O) - pos(S)| >= 2)
    solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))
    
    # Q: S is performed fourth
    solver.add(pos['S'] == 4)
    
    # Options
    options = [
        ("A", [pos['F'] == 1, pos['H'] == 2, pos['P'] == 3]),
        ("B", [pos['H'] == 1, pos['P'] == 2, pos['L'] == 3]),
        ("C", [pos['O'] == 1, pos['P'] == 2, pos['R'] == 3]),
        ("D", [pos['O'] == 1, pos['P'] == 2, pos['T'] == 3]),
        ("E", [pos['P'] == 1, pos['R'] == 2, pos['T'] == 3])
    ]
    
    found_options = []
    for letter, constrs in options:
        solver.push()
        for c in constrs:
            solver.add(c)
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

solve()