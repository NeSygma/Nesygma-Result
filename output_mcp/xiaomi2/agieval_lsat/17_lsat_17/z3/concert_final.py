from z3 import *

solver = Solver()

F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]

for c in comps:
    solver.add(c >= 1, c <= 8)

solver.add(Distinct(comps))

# Given: P is third, S is sixth
solver.add(P == 3)
solver.add(S == 6)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (|F-R| >= 3)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P < S
solver.add(P < S)

# Constraint 6: At least one composition between O and S (|O-S| >= 2)
solver.add(Or(O - S >= 2, S - O >= 2))

# Position 5 must be F or T (from enumeration: pos5 is always F or T)
pos5 = Int('pos5')

# Define options: what MUST be at position 5
# (A) F or H  (B) F or O  (C) F or T  (D) H or L  (E) O or R
opt_a_constr = Or(pos5 == F, pos5 == H)
opt_b_constr = Or(pos5 == F, pos5 == O)
opt_c_constr = Or(pos5 == F, pos5 == T)
opt_d_constr = Or(pos5 == H, pos5 == L)
opt_e_constr = Or(pos5 == O, pos5 == R)

# We need to find which option is ALWAYS true (i.e., its negation is unsat)
# For each option, check if NOT(option) is unsat given the constraints
# pos5 is the composition at position 5: pos5 == comp means that comp is at position 5
# We need: for all valid assignments, pos5 is one of the option's values
# Equivalently: NOT(option) should be unsat

# Add: pos5 is the composition at position 5
# pos5 is one of the 8 compositions, and its position is 5
solver.add(Or([And(c == 5) for c in [F, H, L, O, P, R, S, T]]))

# Actually, let me re-approach. We enumerate all solutions and check pos5.
# But using the required skeleton, let's check each option as a "must be true" constraint.

# The question asks what MUST be at position 5. We check each option by seeing
# if adding NOT(option) makes it unsat (meaning option is always true).

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Check if this option is ALWAYS true by trying to find a counterexample
    # A counterexample would be a valid assignment where pos5 is NOT in the option
    # pos5 is the composition at position 5
    # We need to find which composition is at position 5
    # Let's define: pos5_val is the name-index of the composition at position 5
    # Actually, let's use a different approach:
    # For each option, check if there exists a valid solution where the option is violated
    # Option violated means: pos5 is neither of the two values in the option
    
    # pos5 is the composition at position 5
    # We need: the composition at position 5 is NOT F and NOT T (for option C)
    # i.e., H is at 5, or L is at 5, or O is at 5, or P is at 5, or R is at 5, or S is at 5
    
    # For option A (F or H): violated if pos5 is not F and not H
    # For option C (F or T): violated if pos5 is not F and not T
    
    # Let's define pos5 as the composition whose position is 5
    # We already have all compositions with positions 1-8
    # pos5 is the composition at position 5
    # We need to check: is there a valid assignment where pos5 is NOT in the option set?
    
    # For option C: violated if F != 5 AND T != 5
    if letter == "A":
        solver.add(And(F != 5, H != 5))
    elif letter == "B":
        solver.add(And(F != 5, O != 5))
    elif letter == "C":
        solver.add(And(F != 5, T != 5))
    elif letter == "D":
        solver.add(And(H != 5, L != 5))
    elif letter == "E":
        solver.add(And(O != 5, R != 5))
    
    if solver.check() == sat:
        # Counterexample exists, so this option is NOT always true
        pass
    else:
        # No counterexample, this option is ALWAYS true
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