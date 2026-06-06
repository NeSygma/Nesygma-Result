from z3 import *

def solve():
    solver = Solver()
    
    # rug_of[color] = rug_id (0, 1, 2)
    # used[color] = boolean
    rug_of = [Int(f'rug_of_{c}') for c in range(6)]
    used = [Bool(f'used_{c}') for c in range(6)]
    
    for c in range(6):
        solver.add(rug_of[c] >= 0, rug_of[c] <= 2)
        
    # Exactly 5 colors used
    solver.add(Sum([If(used[c], 1, 0) for c in range(6)]) == 5)
    
    # Rug contents
    # rug_size[r] = number of colors in rug r
    # Use Or-loop pattern for symbolic indexing
    rug_size = [Sum([If(And(used[c], rug_of[c] == r), 1, 0) for c in range(6)]) for r in range(3)]
    
    # Exactly 2 solid rugs (size 1)
    is_solid = [rug_size[r] == 1 for r in range(3)]
    solver.add(Sum([If(is_solid[r], 1, 0) for r in range(3)]) == 2)
    
    # Rule 1: If W is used, it must be in a rug of size 3.
    # W is index 4.
    for r in range(3):
        solver.add(Implies(And(used[4], rug_of[4] == r), rug_size[r] == 3))
    
    # Rule 2: If O is used, P is also used in that same rug.
    # O is index 1, P is index 2.
    solver.add(Implies(used[1], And(used[2], rug_of[1] == rug_of[2])))
    
    # Rule 3: F and T not together. (0 and 3)
    for r in range(3):
        solver.add(Not(And(used[0], used[3], rug_of[0] == r, rug_of[3] == r)))
        
    # Rule 4: P and T not together. (2 and 3)
    for r in range(3):
        solver.add(Not(And(used[2], used[3], rug_of[2] == r, rug_of[3] == r)))
        
    # Rule 5: P and Y not together. (2 and 5)
    for r in range(3):
        solver.add(Not(And(used[2], used[5], rug_of[2] == r, rug_of[5] == r)))
        
    # Solid rug definition: rug_size[r] == 1
    # A color c is in a solid rug if is_solid[rug_of[c]] is true.
    # To check if two colors c1, c2 are the two solid rugs:
    # They must be used, they must be in different rugs, and both those rugs must be solid.
    def is_solid_pair(c1, c2):
        return And(used[c1], used[c2], 
                   Or([And(rug_of[c1] == r, is_solid[r]) for r in range(3)]),
                   Or([And(rug_of[c2] == r, is_solid[r]) for r in range(3)]),
                   rug_of[c1] != rug_of[c2])
    
    options = [
        ("A", (0, 2)), # F, P
        ("B", (0, 5)), # F, Y
        ("C", (2, 3)), # P, T
        ("D", (2, 5)), # P, Y
        ("E", (3, 5))  # T, Y
    ]
    
    found_options = []
    for letter, (c1, c2) in options:
        solver.push()
        solver.add(is_solid_pair(c1, c2))
        if solver.check() == sat:
            found_options.append(letter)
        solver.pop()
        
    # The question asks: "If there are exactly two solid rugs, then the colors of those two rugs CANNOT be..."
    # This means we are looking for the option that is NOT possible.
    # So we want to find which options are NOT satisfiable.
    
    # Wait, the question is "If there are exactly two solid rugs, then the colors of those two rugs CANNOT be..."
    # This means we want to find the option that is NOT possible.
    # Let's re-read: "If there are exactly two solid rugs, then the colors of those two rugs CANNOT be..."
    # This means for a given option (c1, c2), if it's possible to have c1 and c2 as the two solid rugs, then that option is NOT the answer.
    # We want the option that is NOT possible.
    
    # Let's re-evaluate:
    # If an option is SAT, it means it IS possible for those two to be the solid rugs.
    # If an option is UNSAT, it means it is NOT possible for those two to be the solid rugs.
    # The question asks which one CANNOT be the colors of the two solid rugs.
    # So we are looking for the option that is UNSAT.
    
    # Let's check all options.
    
    results = {}
    for letter, (c1, c2) in options:
        solver.push()
        solver.add(is_solid_pair(c1, c2))
        res = solver.check()
        results[letter] = res
        solver.pop()
        
    print(results)
    
    # If only one is UNSAT, that's our answer.
    unsat_options = [l for l, res in results.items() if res == unsat]
    
    if len(unsat_options) == 1:
        print("STATUS: sat")
        print(f"answer:{unsat_options[0]}")
    elif len(unsat_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {unsat_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()