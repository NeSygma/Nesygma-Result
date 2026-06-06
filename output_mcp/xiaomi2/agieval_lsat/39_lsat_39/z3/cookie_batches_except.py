from z3 import *

solver = Solver()

# Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
# Cookie kinds: Oatmeal (O), Peanut Butter (PB), Sugar (S)
# Each has 3 batches: batch 1, 2, 3

O = [Int(f'O_{i}') for i in range(1, 4)]   # Oatmeal batches 1,2,3
PB = [Int(f'PB_{i}') for i in range(1, 4)] # Peanut Butter batches 1,2,3
S = [Int(f'S_{i}') for i in range(1, 4)]   # Sugar batches 1,2,3

all_vars = O + PB + S

# Each batch is on a day 1-5
for v in all_vars:
    solver.add(And(v >= 1, v <= 5))

# No two batches of the same kind on the same day
solver.add(Distinct(O))
solver.add(Distinct(PB))
solver.add(Distinct(S))

# At least one batch on Monday
solver.add(Or([v == 1 for v in all_vars]))

# The second batch of oatmeal is on the same day as the first batch of peanut butter
solver.add(O[1] == PB[0])

# The second batch of sugar is on Thursday
solver.add(S[1] == 4)

# Given: The first batch of peanut butter is on Tuesday
solver.add(PB[0] == 2)

# From constraint 3 + given: O_2 = 2

# Test each option for satisfiability
# (A) Two different kinds have their first batch on Monday
opt_a = And(O[0] == 1, S[0] == 1)

# (B) Two different kinds have their first batch on Tuesday
opt_b = (S[0] == 2)

# (C) Two different kinds have their second batch on Wednesday
opt_c = Or(
    And(O[1] == 3, PB[1] == 3),
    And(O[1] == 3, S[1] == 3),
    And(PB[1] == 3, S[1] == 3)
)

# (D) Two different kinds have their second batch on Thursday
opt_d = (PB[1] == 4)

# (E) Two different kinds have their third batch on Friday
opt_e = Or(
    And(O[2] == 5, PB[2] == 5),
    And(O[2] == 5, S[2] == 5),
    And(PB[2] == 5, S[2] == 5)
)

# For EXCEPT question: find the one that CANNOT be true (UNSAT)
impossible_options = []
possible_options = []

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        possible_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT (could be true) - O={[m[O[i]] for i in range(3)]}, PB={[m[PB[i]] for i in range(3)]}, S={[m[S[i]] for i in range(3)]}")
    else:
        impossible_options.append(letter)
        print(f"Option {letter}: {result} (CANNOT be true)")
    solver.pop()

print()
print(f"Possible options: {possible_options}")
print(f"Impossible options: {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")