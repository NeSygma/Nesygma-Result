from z3 import *

solver = Solver()

# Pianists: 0 = Wayne, 1 = Zara
P = [Int(f'P_{i}') for i in range(5)]
# Types: 0 = Modern, 1 = Traditional
T = [Int(f'T_{i}') for i in range(5)]

for i in range(5):
    solver.add(P[i] >= 0, P[i] <= 1)
    solver.add(T[i] >= 0, T[i] <= 1)

# 1. The third solo is a traditional piece.
solver.add(T[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# This means exactly one pair (i, i+1) such that T[i] == 1 and T[i+1] == 1.
solver.add(Sum([If(And(T[i] == 1, T[i+1] == 1), 1, 0) for i in range(4)]) == 1)

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# (P[3] == 0 and T[3] == 1) or (P[3] == 1 and T[3] == 0)
solver.add(Or(And(P[3] == 0, T[3] == 1), And(P[3] == 1, T[3] == 0)))

# 4. The pianist who performs the second solo does not perform the fifth solo.
solver.add(P[1] != P[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# For all i, if T[i] == 1, then there exists j < i such that P[j] == 0 and T[j] == 0.
for i in range(5):
    # If T[i] == 1, then there must be a j < i with P[j] == 0 and T[j] == 0
    has_modern_wayne_before = Or([And(P[j] == 0, T[j] == 0) for j in range(i)])
    solver.add(Implies(T[i] == 1, has_modern_wayne_before))

# Condition: The pianist who performs the first solo also performs the second solo.
solver.add(P[0] == P[1])

# Define options
opt_a_constr = (P[0] == 1) # Zara performs the first solo
opt_b_constr = (P[2] == 0) # Wayne performs the third solo
opt_c_constr = (P[4] == 1) # Zara performs the fifth solo
opt_d_constr = (T[1] == 1) # The second solo is a traditional piece
opt_e_constr = (T[3] == 0) # The fourth solo is a modern piece

# Check which options MUST be true (i.e., Not(option) is unsat)
# We need to check if the option is true in ALL models.
# So we check if (Base Constraints AND Not(Option)) is UNSAT.

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
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