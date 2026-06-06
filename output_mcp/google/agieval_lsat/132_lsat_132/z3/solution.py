from z3 import *

# Movies: 0:H, 1:M, 2:R, 3:S, 4:W
# Slots: 0:S1_7, 1:S1_9, 2:S2_7, 3:S2_9, 4:S3_8
# Screen mapping: 0:1, 1:1, 2:2, 3:2, 4:3
# Time mapping: 0:7, 1:9, 2:7, 3:9, 4:8

def solve():
    solver = Solver()
    
    # pos[movie] = slot_index
    pos = [Int(f'pos_{m}') for m in range(5)]
    
    # Each movie in exactly one slot
    solver.add(Distinct(pos))
    for m in range(5):
        solver.add(pos[m] >= 0, pos[m] <= 4)
        
    # Helper functions for screen and time of a slot
    def get_screen(slot):
        return If(slot == 0, 1, If(slot == 1, 1, If(slot == 2, 2, If(slot == 3, 2, 3))))
    
    def get_time(slot):
        return If(slot == 0, 7, If(slot == 1, 9, If(slot == 2, 7, If(slot == 3, 9, 8))))
    
    # Constraints
    # 1. Western begins before Horror
    solver.add(get_time(pos[4]) < get_time(pos[0]))
    
    # 2. Sci-fi not on screen 3
    solver.add(get_screen(pos[3]) != 3)
    
    # 3. Romance not on screen 2
    solver.add(get_screen(pos[2]) != 2)
    
    # 4. Horror and Mystery on different screens
    solver.add(get_screen(pos[0]) != get_screen(pos[1]))
    
    # Options: (7 PM, 9 PM) on Screen 1
    # Movies: 0:H, 1:M, 2:R, 3:S, 4:W
    # Screen 1 slots are 0 (7 PM) and 1 (9 PM)
    
    # A: S, H
    opt_a = And(pos[3] == 0, pos[0] == 1)
    # B: S, M
    opt_b = And(pos[3] == 0, pos[1] == 1)
    # C: W, H
    opt_c = And(pos[4] == 0, pos[0] == 1)
    # D: W, M
    opt_d = And(pos[4] == 0, pos[1] == 1)
    # E: W, S
    opt_e = And(pos[4] == 0, pos[3] == 1)
    
    # The question asks which CANNOT be true.
    # So we look for the option that makes the system UNSAT.
    
    found_options = []
    for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
        solver.push()
        solver.add(constr)
        if solver.check() == unsat:
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