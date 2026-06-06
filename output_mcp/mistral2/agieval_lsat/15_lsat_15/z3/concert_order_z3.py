from z3 import *

solver = Solver()

# Declare the compositions as integers representing their positions (1 to 8)
# We will use a list where the index represents the position and the value represents the composition
compositions = [Int(f'pos_{i+1}') for i in range(8)]

# Each composition is unique and ranges from 1 to 8 (representing F, H, L, O, P, R, S, T)
# We will map the letters to numbers for easier handling
F, H, L, O, P, R, S, T = 1, 2, 3, 4, 5, 6, 7, 8

# Assign each position a unique composition
solver.add(Distinct(compositions))
for i in range(8):
    solver.add(compositions[i] >= 1, compositions[i] <= 8)

# Condition 1: T is performed either immediately before F or immediately after R
# Find the positions of T, F, and R
pos_T = None
pos_F = None
pos_R = None
for i in range(8):
    solver.add(Or(
        And(compositions[i] == T, pos_T == None, pos_T := i),
        And(compositions[i] == F, pos_F == None, pos_F := i),
        And(compositions[i] == R, pos_R == None, pos_R := i)
    ))

# T is immediately before F
solver.add(Or(
    And(pos_T != None, pos_F != None, pos_F == pos_T + 1),
    # T is immediately after R
    And(pos_T != None, pos_R != None, pos_T == pos_R + 1)
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This is a bit complex, so we will handle it by ensuring the positions of F and R are such that there are at least two compositions between them in either order
solver.add(Or(
    # Case 1: F before R, at least two compositions after F and before R
    And(
        pos_F != None, pos_R != None, pos_F < pos_R,
        pos_R - pos_F >= 3  # At least two compositions between F and R
    ),
    # Case 2: R before F, at least two compositions after R and before F
    And(
        pos_R != None, pos_F != None, pos_R < pos_F,
        pos_F - pos_R >= 3  # At least two compositions between R and F
    )
))

# Condition 3: O is performed either first or fifth
pos_O = None
for i in range(8):
    solver.add(Or(
        And(compositions[i] == O, pos_O == None, pos_O := i, i == 0),
        And(compositions[i] == O, pos_O == None, pos_O := i, i == 4)
    ))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(compositions[7] == L, compositions[7] == H))

# Condition 5: P is performed at some time before S
pos_P = None
pos_S = None
for i in range(8):
    solver.add(Or(
        And(compositions[i] == P, pos_P == None, pos_P := i),
        And(compositions[i] == S, pos_S == None, pos_S := i)
    ))
solver.add(pos_P != None, pos_S != None, pos_P < pos_S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This is a bit complex, so we will handle it by ensuring there is at least one composition between O and S in either order
solver.add(Or(
    # Case 1: O before S, at least one composition after O and before S
    And(
        pos_O != None, pos_S != None, pos_O < pos_S,
        pos_S - pos_O >= 2
    ),
    # Case 2: S before O, at least one composition after S and before O
    And(
        pos_S != None, pos_O != None, pos_S < pos_O,
        pos_O - pos_S >= 2
    )
))

# Additional constraint: If O is performed immediately after T, then F must be performed either ...
# We will handle this in the multiple-choice evaluation part

# Base constraints are now added. Now, we will evaluate the multiple-choice options.
# We need to check each option under the condition that O is performed immediately after T.

# First, let's find the position of O and T to enforce O is immediately after T
pos_O = None
pos_T = None
for i in range(8):
    solver.add(Or(
        And(compositions[i] == O, pos_O == None, pos_O := i),
        And(compositions[i] == T, pos_T == None, pos_T := i)
    ))

# O is immediately after T
solver.add(And(pos_O != None, pos_T != None, pos_O == pos_T + 1))

# Now, evaluate the multiple-choice options
found_options = []

# Option A: F is first or second
opt_a_constr = Or(
    And(pos_F != None, pos_F == 0),
    And(pos_F != None, pos_F == 1)
)

# Option B: F is second or third
opt_b_constr = Or(
    And(pos_F != None, pos_F == 1),
    And(pos_F != None, pos_F == 2)
)

# Option C: F is fourth or sixth
opt_c_constr = Or(
    And(pos_F != None, pos_F == 3),
    And(pos_F != None, pos_F == 5)
)

# Option D: F is fourth or seventh
opt_d_constr = Or(
    And(pos_F != None, pos_F == 3),
    And(pos_F != None, pos_F == 6)
)

# Option E: F is sixth or seventh
opt_e_constr = Or(
    And(pos_F != None, pos_F == 5),
    And(pos_F != None, pos_F == 6)
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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