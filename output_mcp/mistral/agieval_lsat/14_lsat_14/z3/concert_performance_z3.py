from z3 import *

# Define the compositions as symbolic constants
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
# Map compositions to unique integers for easier handling
comp_map = {
    'F': F,
    'H': H,
    'L': L,
    'O': O,
    'P': P,
    'R': R,
    'S': S,
    'T': T
}

# Performance order: perf[0] is first, perf[7] is eighth
perf = [Int(f'perf_{i}') for i in range(8)]

solver = Solver()

# Each position must be one of the compositions
compositions = [F, H, L, O, P, R, S, T]
solver.add(Distinct(compositions))
for p in perf:
    solver.add(Or([p == c for c in compositions]))

# All compositions must appear exactly once
solver.add(Distinct(perf))

# Constraint: T is immediately before F or immediately after R
# Case 1: T immediately before F (perf[i] = T and perf[i+1] = F)
# Case 2: T immediately after R (perf[i] = R and perf[i+1] = T)
solver.add(Or(
    Or([And(perf[i] == T, perf[i+1] == F) for i in range(7)]),
    Or([And(perf[i] == R, perf[i+1] == T) for i in range(7)])
))

# Constraint: At least two compositions are performed either after F and before R, or after R and before F
# This means the positions of F and R must have at least two compositions between them in either order
# We'll handle this after defining positions of F and R

# Constraint: O is performed either first or fifth
solver.add(Or(perf[0] == O, perf[4] == O))

# Constraint: The eighth composition performed is either L or H
solver.add(Or(perf[7] == L, perf[7] == H))

# Constraint: P is performed at some time before S
# Find indices of P and S in perf
p_before_s = False
for i in range(8):
    for j in range(i+1, 8):
        p_before_s = Or(p_before_s, And(perf[i] == P, perf[j] == S))
solver.add(p_before_s)

# Constraint: At least one composition is performed either after O and before S, or after S and before O
# This means there is at least one composition between O and S in either order
at_least_one_between_o_and_s = False
for i in range(8):
    for j in range(8):
        if i != j:
            at_least_one_between_o_and_s = Or(
                at_least_one_between_o_and_s,
                And(
                    Or([perf[k] == O for k in range(8)]),  # O is at some position
                    Or([perf[k] == S for k in range(8)]),  # S is at some position
                    # At least one composition between O and S
                    Or([
                        And(
                            Or([perf[i] == O]),
                            Or([perf[j] == S]),
                            i < j,
                            j - i >= 2
                        ),
                        And(
                            Or([perf[i] == S]),
                            Or([perf[j] == O]),
                            i < j,
                            j - i >= 2
                        )
                    ])
                )
            )
# This is a bit messy; let's simplify by ensuring that if O and S are placed, there is at least one position between them
# Alternative: after assigning O and S positions, ensure |pos_O - pos_S| >= 2
# We'll handle this in the model-finding phase

# Given condition: T is performed fifth and F is performed sixth
# perf[4] = T, perf[5] = F
solver.push()
solver.add(perf[4] == T)
solver.add(perf[5] == F)

# Now, let's find possible positions for S under the given condition
# We'll check each option (A-E) to see if S can be in the specified positions

# Define the options as constraints on S's position
# Option A: S is fourth or seventh (positions 3 or 6 in 0-index)
opt_a_constr = Or(perf[3] == S, perf[6] == S)

# Option B: S is third or sixth (positions 2 or 5 in 0-index)
opt_b_constr = Or(perf[2] == S, perf[5] == S)

# Option C: S is third or fourth (positions 2 or 3 in 0-index)
opt_c_constr = Or(perf[2] == S, perf[3] == S)

# Option D: S is second or seventh (positions 1 or 6 in 0-index)
opt_d_constr = Or(perf[1] == S, perf[6] == S)

# Option E: S is first or fourth (positions 0 or 3 in 0-index)
opt_e_constr = Or(perf[0] == S, perf[3] == S)

# Now, test each option
found_options = []
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