from z3 import *

solver = Solver()
O = [Int(f'O{i}') for i in range(1, 4)]
P = [Int(f'P{i}') for i in range(1, 4)]
S = [Int(f'S{i}') for i in range(1, 4)]
all_batches = O + P + S
for b in all_batches: solver.add(b >= 0, b <= 4)
solver.add(Distinct(O), Distinct(P), Distinct(S))
solver.add(Or([b == 0 for b in all_batches]))
solver.add(O[1] == P[0])
solver.add(S[1] == 3)

I = Or(O[0] == P[2], O[0] == S[2], P[0] == O[2], P[0] == S[2], S[0] == O[2], S[0] == P[2])
solver.add(I)

# Define options
# (A) At least one batch of cookies is made on each of the five days.
# (B) At least two batches of cookies are made on Wednesday.
# (C) Exactly one batch of cookies is made on Monday.
# (D) Exactly two batches of cookies are made on Tuesday.
# (E) Exactly one batch of cookies is made on Friday.

def count_on_day(day):
    return Sum([If(b == day, 1, 0) for b in all_batches])

opt_a = And([count_on_day(d) >= 1 for d in range(5)])
opt_b = count_on_day(2) >= 2
opt_c = count_on_day(0) == 1
opt_d = count_on_day(1) == 2
opt_e = count_on_day(4) == 1

# We want to find which of these COULD be false.
# So we check if (Constraints + I + Not(Option)) is SAT.
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Options that could be false: {found_options}")