from z3 import *

def solve():
    solver = Solver()
    
    # Positions 1-8
    pos = {name: Int(name) for name in ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']}
    for name in pos:
        solver.add(pos[name] >= 1, pos[name] <= 8)
    
    solver.add(Distinct(list(pos.values())))
    
    # C1: T is immediately before F OR T is immediately after R
    solver.add(Or(pos['F'] == pos['T'] + 1, pos['T'] == pos['R'] + 1))
    
    # C2: At least two compositions between F and R (|pos(F) - pos(R)| >= 3)
    # |pos(F) - pos(R)| >= 3 means pos(F) - pos(R) >= 3 OR pos(R) - pos(F) >= 3
    solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))
    
    # C3: O is 1st or 5th
    solver.add(Or(pos['O'] == 1, pos['O'] == 5))
    
    # C4: 8th is L or H
    solver.add(Or(pos['L'] == 8, pos['H'] == 8))
    
    # C5: P is before S
    solver.add(pos['P'] < pos['S'])
    
    # C6: At least one composition between O and S (|pos(O) - pos(S)| >= 2)
    solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))
    
    # Condition: O is performed immediately after T
    condition = (pos['O'] == pos['T'] + 1)
    
    # Options
    options = [
        ("A", Or(pos['F'] == 1, pos['F'] == 2)),
        ("B", Or(pos['F'] == 2, pos['F'] == 3)),
        ("C", Or(pos['F'] == 4, pos['F'] == 6)),
        ("D", Or(pos['F'] == 4, pos['F'] == 7)),
        ("E", Or(pos['F'] == 6, pos['F'] == 7))
    ]
    
    # We want to find which option is necessarily true given the condition.
    # An option is necessarily true if (Base AND Condition AND NOT Option) is UNSAT.
    
    valid_options = []
    for label, opt_constr in options:
        solver.push()
        solver.add(condition)
        solver.add(Not(opt_constr))
        if solver.check() == unsat:
            valid_options.append(label)
        solver.pop()
        
    if len(valid_options) == 1:
        print("STATUS: sat")
        print(f"answer:{valid_options[0]}")
    elif len(valid_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {valid_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()