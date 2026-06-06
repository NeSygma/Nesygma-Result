from z3 import *

solver = Solver()

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (first, second, third)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Constraint: No batch on Wednesday (day 2)

O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Domain: each batch is made on Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch of cookies is made on Monday
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
solver.add(O2 == P1)

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(S2 == 3)

# IF condition: No batch of cookies is made on Wednesday (day 2)
solver.add(And([b != 2 for b in all_batches]))

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    for b in all_batches:
        print(f"  {b} = {m[b]}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now let's think more carefully.
# We have 9 batches total. No Wednesday means 9 batches spread over 4 days (Mon, Tue, Thu, Fri).
# Each kind has 3 batches on 3 different days.
# S2 is Thursday. So Sugar has batches on Thu and two other days (not Wed, not same day).
# O2 = P1, so O2 and P1 are on the same day.

# Let's enumerate all solutions to see what MUST be true
solutions = []
solver.push()
while solver.check() == sat:
    m = solver.model()
    sol = {str(b): m.eval(b, model_completion=True).as_long() for b in all_batches}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([b != m.eval(b, model_completion=True).as_long() for b in all_batches]))
solver.pop()

print(f"\nTotal solutions: {len(solutions)}")

# For each solution, compute the counts per day
def day_counts(sol):
    counts = {0:0, 1:0, 3:0, 4:0}  # Mon, Tue, Thu, Fri (Wed=2 excluded)
    for b_name, day in sol.items():
        if day in counts:
            counts[day] += 1
    return counts

# Check each option across all solutions
# Option A: Exactly 3 on Tuesday
all_a = all(day_counts(s)[1] == 3 for s in solutions)
# Option B: Exactly 3 on Friday
all_b = all(day_counts(s)[4] == 3 for s in solutions)
# Option C: At least 2 on Monday
all_c = all(day_counts(s)[0] >= 2 for s in solutions)
# Option D: At least 2 on Thursday
all_d = all(day_counts(s)[3] >= 2 for s in solutions)
# Option E: Fewer on Monday than Tuesday
all_e = all(day_counts(s)[0] < day_counts(s)[1] for s in solutions)

print(f"A (exactly 3 on Tue) holds in all solutions: {all_a}")
print(f"B (exactly 3 on Fri) holds in all solutions: {all_b}")
print(f"C (at least 2 on Mon) holds in all solutions: {all_c}")
print(f"D (at least 2 on Thu) holds in all solutions: {all_d}")
print(f"E (Mon < Tue) holds in all solutions: {all_e}")

# Also print some sample solutions to understand the pattern
print("\nSample solutions (first 5):")
for i, sol in enumerate(solutions[:5]):
    counts = day_counts(sol)
    print(f"  Solution {i+1}: Mon={counts[0]}, Tue={counts[1]}, Thu={counts[3]}, Fri={counts[4]}")
    print(f"    O1={sol['O1']}, O2={sol['O2']}, O3={sol['O3']}, P1={sol['P1']}, P2={sol['P2']}, P3={sol['P3']}, S1={sol['S1']}, S2={sol['S2']}, S3={sol['S3']}")