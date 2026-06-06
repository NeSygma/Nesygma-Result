from z3 import *

solver = Solver()

F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
positions = [F, H, L, O, P, R, S, T]

for p in positions:
    solver.add(p >= 1, p <= 8)
solver.add(Distinct(positions))

# Given: T is performed fifth and F is performed sixth
solver.add(T == 5)
solver.add(F == 6)

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions between F and R
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed before S
solver.add(P < S)

# Condition 6: At least one composition between O and S
solver.add(Or(O - S >= 2, S - O >= 2))

# Find all possible values of S
possible_S = []
for s_val in range(1, 9):
    solver.push()
    solver.add(S == s_val)
    if solver.check() == sat:
        possible_S.append(s_val)
        m = solver.model()
        print(f"S={s_val} is possible: F={m[F]}, H={m[H]}, L={m[L]}, O={m[O]}, P={m[P]}, R={m[R]}, S={m[S]}, T={m[T]}")
    solver.pop()

print(f"\nPossible values of S: {possible_S}")
print(f"Number of possible values: {len(possible_S)}")

# Now check which answer choice exactly matches
opt_a = {4, 7}
opt_b = {3, 6}
opt_c = {3, 4}
opt_d = {2, 7}
opt_e = {1, 4}

possible_S_set = set(possible_S)
print(f"\nS possible set: {possible_S_set}")
print(f"A matches: {opt_a == possible_S_set}")
print(f"B matches: {opt_b == possible_S_set}")
print(f"C matches: {opt_c == possible_S_set}")
print(f"D matches: {opt_d == possible_S_set}")
print(f"E matches: {opt_e == possible_S_set}")

# The question says "S must be performed either X or Y"
# This means S can ONLY be one of those two values
# So we need the answer choice whose set equals the possible_S set
matching = []
for letter, opt_set in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    if opt_set == possible_S_set:
        matching.append(letter)

if len(matching) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{matching[0]}")
elif len(matching) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple matches {matching}")
else:
    print(f"\nSTATUS: unsat")
    print(f"Refine: No exact match found")