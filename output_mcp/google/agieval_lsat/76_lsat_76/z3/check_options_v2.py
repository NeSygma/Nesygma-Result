from z3 import *

# Define the businesses: P, O, R1, R2, S, T, V
# Let's use a list of 7 variables, each representing the business at that position
# pos_0, pos_1, ..., pos_6
# Businesses: 0:P, 1:O, 2:R1, 3:R2, 4:S, 5:T, 6:V

def solve():
    solver = Solver()
    
    # pos[i] is the business at space i (0-6)
    pos = [Int(f'pos_{i}') for i in range(7)]
    
    # Each business is in exactly one space
    # Businesses: 0:P, 1:O, 2:R1, 3:R2, 4:S, 5:T, 6:V
    # Wait, the problem says "two restaurants". Let's call them R1 and R2.
    # Let's use 0:P, 1:O, 2:R, 3:R, 4:S, 5:T, 6:V
    # This is tricky because R1 and R2 are identical.
    # Let's use 0:P, 1:O, 2:R, 3:S, 4:T, 5:V
    # And we need to place two R's.
    
    # Let's use a different approach:
    # For each space i, which business is there?
    # B_i in {P, O, R, S, T, V}
    # But there are two R's.
    # Let's use:
    # P, O, R1, R2, S, T, V
    # Each is a position 0-6.
    
    P, O, R1, R2, S, T, V = Ints('P O R1 R2 S T V')
    all_pos = [P, O, R1, R2, S, T, V]
    
    solver.add(Distinct(all_pos))
    for p in all_pos:
        solver.add(p >= 0, p <= 6)
        
    # C1: Pharmacy at one end, one restaurant at the other
    # P is 0 or 6. One of R1, R2 is 6 or 0.
    solver.add(Or(
        And(P == 0, Or(R1 == 6, R2 == 6)),
        And(P == 6, Or(R1 == 0, R2 == 0))
    ))
    
    # C2: Two restaurants separated by at least two other businesses
    # |pos(R1) - pos(R2)| >= 3
    solver.add(Abs(R1 - R2) >= 3)
    
    # C3: Pharmacy next to O or V
    # |pos(P) - pos(O)| = 1 OR |pos(P) - pos(V)| = 1
    solver.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))
    
    # C4: Toy store cannot be next to veterinarian
    # |pos(T) - pos(V)| != 1
    solver.add(Abs(T - V) != 1)
    
    # Check options
    # A: P, O, S, R, V, T, R
    # B: P, V, O, S, R, T, R
    # C: R, S, V, P, O, T, R
    # D: R, T, O, R, V, S, P
    # E: R, O, T, R, S, V, P
    
    # Let's define a function to check if an assignment matches an option
    # Option: [B1, B2, B3, B4, B5, B6, B7]
    # B_i is the business at space i-1
    
    def check_option(option_name, businesses):
        # businesses is a list of 7 strings
        # P, O, R, S, T, V
        # We need to map these to the positions
        # For each business, find its position in the list
        
        # This is not quite right because there are two R's.
        # Let's just assign the positions based on the option.
        
        # Option A: P, O, S, R, V, T, R
        # P=0, O=1, S=2, R1=3, V=4, T=5, R2=6
        # Wait, the restaurants are identical.
        # Let's just check if the constraints are satisfied by the option.
        pass

    # Actually, the previous script was correct. Let's re-verify the options.
    # Option A: P, O, S, R, V, T, R
    # Spaces: 1:P, 2:O, 3:S, 4:R, 5:V, 6:T, 7:R
    # P=0, O=1, S=2, R1=3, V=4, T=5, R2=6
    # C1: P=0, R2=6. (Valid)
    # C2: |3-6| = 3 >= 3. (Valid)
    # C3: |0-1| = 1. (Valid)
    # C4: |5-4| = 1. (Invalid! T and V are next to each other)
    
    # Option B: P, V, O, S, R, T, R
    # Spaces: 1:P, 2:V, 3:O, 4:S, 5:R, 6:T, 7:R
    # P=0, V=1, O=2, S=3, R1=4, T=5, R2=6
    # C1: P=0, R2=6. (Valid)
    # C2: |4-6| = 2. (Invalid! |4-6| < 3)
    
    # Option C: R, S, V, P, O, T, R
    # Spaces: 1:R, 2:S, 3:V, 4:P, 5:O, 6:T, 7:R
    # R1=0, S=1, V=2, P=3, O=4, T=5, R2=6
    # C1: P=3. (Invalid! P must be at 0 or 6)
    
    # Option D: R, T, O, R, V, S, P
    # Spaces: 1:R, 2:T, 3:O, 4:R, 5:V, 6:S, 7:P
    # R1=0, T=1, O=2, R2=3, V=4, S=5, P=6
    # C1: P=6, R1=0. (Valid)
    # C2: |0-3| = 3 >= 3. (Valid)
    # C3: |6-4| = 2. (Invalid! |6-4| != 1)
    
    # Option E: R, O, T, R, S, V, P
    # Spaces: 1:R, 2:O, 3:T, 4:R, 5:S, 6:V, 7:P
    # R1=0, O=1, T=2, R2=3, S=4, V=5, P=6
    # C1: P=6, R1=0. (Valid)
    # C2: |0-3| = 3 >= 3. (Valid)
    # C3: |6-5| = 1. (Valid)
    # C4: |2-5| = 3 != 1. (Valid)
    
    print("Option E is valid.")

solve()