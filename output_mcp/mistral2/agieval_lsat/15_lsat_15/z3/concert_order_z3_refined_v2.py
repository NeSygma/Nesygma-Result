from z3 import *

solver = Solver()

# Declare the compositions as integers representing their identities
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# Assign each composition a unique value from 1 to 8
solver.add(F >= 1, F <= 8)
solver.add(H >= 1, H <= 8)
solver.add(L >= 1, L <= 8)
solver.add(O >= 1, O <= 8)
solver.add(P >= 1, P <= 8)
solver.add(R >= 1, R <= 8)
solver.add(S >= 1, S <= 8)
solver.add(T >= 1, T <= 8)
solver.add(Distinct([F, H, L, O, P, R, S, T]))

# Declare the order of performances as a list of Z3 integers
# Each position in the list represents the performance order (1 to 8)
# The value at each position is the composition performed there
order = [Int(f'order_{i+1}') for i in range(8)]

# Each position in the order must be one of the compositions
for i in range(8):
    solver.add(Or(
        order[i] == F,
        order[i] == H,
        order[i] == L,
        order[i] == O,
        order[i] == P,
        order[i] == R,
        order[i] == S,
        order[i] == T
    ))

# All compositions are unique in the order
solver.add(Distinct(order))

# Condition 1: T is performed either immediately before F or immediately after R
# Find the positions of T, F, and R in the order
# T is immediately before F
solver.add(Or(
    Exists([pos_T, pos_F], And(
        pos_F == pos_T + 1,
        order[pos_T] == T,
        order[pos_F] == F
    )),
    Exists([pos_R, pos_T], And(
        pos_T == pos_R + 1,
        order[pos_R] == R,
        order[pos_T] == T
    ))
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This is complex, so we will handle it by ensuring the positions of F and R are such that there are at least two compositions between them in either order
solver.add(
    Or(
        # Case 1: F before R, at least two compositions after F and before R
        Exists([pos_F, pos_R], And(
            pos_F < pos_R,
            pos_R - pos_F >= 3  # At least two compositions between F and R
        )),
        # Case 2: R before F, at least two compositions after R and before F
        Exists([pos_R, pos_F], And(
            pos_R < pos_F,
            pos_F - pos_R >= 3  # At least two compositions between R and F
        ))
    )
)

# Condition 3: O is performed either first or fifth
solver.add(Or(order[0] == O, order[4] == O))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(order[7] == L, order[7] == H))

# Condition 5: P is performed at some time before S
solver.add(
    Exists([pos_P, pos_S], And(
        pos_P < pos_S,
        order[pos_P] == P,
        order[pos_S] == S
    ))
)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
solver.add(
    Or(
        # Case 1: O before S, at least one composition after O and before S
        Exists([pos_O, pos_S], And(
            pos_O < pos_S,
            pos_S - pos_O >= 2
        )),
        # Case 2: S before O, at least one composition after S and before O
        Exists([pos_S, pos_O], And(
            pos_S < pos_O,
            pos_O - pos_S >= 2
        ))
    )
)

# Additional constraint: If O is performed immediately after T, then F must be performed either ...
# We will handle this in the multiple-choice evaluation part

# Find the positions of O and T to enforce O is immediately after T
solver.add(
    Exists([pos_T, pos_O], And(
        pos_O == pos_T + 1,
        order[pos_T] == T,
        order[pos_O] == O
    ))
)

# Now, evaluate the multiple-choice options
found_options = []

# Option A: F is first or second
opt_a_constr = Or(
    order[0] == F,
    order[1] == F
)

# Option B: F is second or third
opt_b_constr = Or(
    order[1] == F,
    order[2] == F
)

# Option C: F is fourth or sixth
opt_c_constr = Or(
    order[3] == F,
    order[5] == F
)

# Option D: F is fourth or seventh
opt_d_constr = Or(
    order[3] == F,
    order[6] == F
)

# Option E: F is sixth or seventh
opt_e_constr = Or(
    order[5] == F,
    order[6] == F
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