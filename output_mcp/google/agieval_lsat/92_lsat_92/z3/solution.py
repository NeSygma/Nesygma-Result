from z3 import *

# Pianists: 0 = Wayne, 1 = Zara
# Types: 0 = Modern, 1 = Traditional
# Solos: 0, 1, 2, 3, 4 (representing 1st, 2nd, 3rd, 4th, 5th)

P = [Int(f'P_{i}') for i in range(5)]
T = [Int(f'T_{i}') for i in range(5)]

solver = Solver()

# Domains
for i in range(5):
    solver.add(P[i] >= 0, P[i] <= 1)
    solver.add(T[i] >= 0, T[i] <= 1)

# 1. The third solo is a traditional piece.
solver.add(T[2] == 1)

# 2. Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair (i, i+1) such that T[i]=1 and T[i+1]=1.
# And no other T's are adjacent.
# Let's define a helper for consecutive T's
is_consecutive_T = [And(T[i] == 1, T[i+1] == 1) for i in range(4)]
solver.add(Sum([If(is_consecutive_T[i], 1, 0) for i in range(4)]) == 1)
# Also, no other T's are adjacent. This is already covered by the sum == 1.
# Wait, what if there are three T's in a row? T, T, T.
# Then is_consecutive_T[0] is true and is_consecutive_T[1] is true. Sum would be 2.
# So Sum == 1 ensures exactly one pair of consecutive T's.
# What if there are T, T, M, T, T? Then Sum would be 2.
# So this constraint seems to mean exactly one pair of consecutive T's.

# 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# (P[3] == 0 and T[3] == 1) OR (P[3] == 1 and T[3] == 0)
solver.add(Or(And(P[3] == 0, T[3] == 1), And(P[3] == 1, T[3] == 0)))

# 4. The pianist who performs the second solo does not perform the fifth solo.
solver.add(P[1] != P[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# If T[i] == 1, then there exists j < i such that P[j] == 0 and T[j] == 0.
for i in range(5):
    solver.add(Implies(T[i] == 1, Or([And(P[j] == 0, T[j] == 0) for j in range(i)])))

# Q: If in the fifth solo Wayne performs a traditional piece, which one of the following could be true?
# Condition: P[4] == 0 and T[4] == 1
solver.add(P[4] == 0, T[4] == 1)

# Answer Choices:
# (A) Zara performs the first solo. (P[0] == 1)
# (B) Wayne performs the second solo. (P[1] == 0)
# (C) Zara performs the third solo. (P[2] == 1)
# (D) The second solo is a modern piece. (T[1] == 0)
# (E) The fourth solo is a traditional piece. (T[3] == 1)

opt_a_constr = (P[0] == 1)
opt_b_constr = (P[1] == 0)
opt_c_constr = (P[2] == 1)
opt_d_constr = (T[1] == 0)
opt_e_constr = (T[3] == 1)

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