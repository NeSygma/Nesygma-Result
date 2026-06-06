from z3 import *

# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
# Wednesday (3) is excluded
VALID_DAYS = [1, 2, 4, 5]

# Batches: O1,O2,O3 (oatmeal), P1,P2,P3 (peanut butter), S1,S2,S3 (sugar)
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]
batch_names = ['O1', 'O2', 'O3', 'P1', 'P2', 'P3', 'S1', 'S2', 'S3']

solver = Solver()

# Each batch on a valid day (not Wednesday)
for b in all_batches:
    solver.add(Or([b == d for d in VALID_DAYS]))

# No two batches of same kind on same day
solver.add(Distinct(O1, O2, O3))
solver.add(Distinct(P1, P2, P3))
solver.add(Distinct(S1, S2, S3))

# At least one batch on Monday
solver.add(Or([b == 1 for b in all_batches]))

# O2 same day as P1
solver.add(O2 == P1)

# S2 on Thursday
solver.add(S2 == 4)

# Count batches per day helper
def batches_on_day(d):
    return Sum([If(b == d, 1, 0) for b in all_batches])

# Enumerate all solutions
solutions = []
decision_vars = all_batches

while solver.check() == sat:
    m = solver.model()
    sol = {}
    day_names = {1: "Mon", 2: "Tue", 4: "Thu", 5: "Fri"}
    for i, b in enumerate(all_batches):
        sol[batch_names[i]] = day_names[int(str(m.eval(b)))]
    
    # Compute day counts
    counts = {}
    for d in VALID_DAYS:
        counts[day_names[d]] = sum(1 for b in all_batches if int(str(m.eval(b))) == d)
    sol['counts'] = counts
    solutions.append(sol)
    
    # Block this solution
    solver.add(Or([b != m.eval(b) for b in all_batches]))

print(f"Total solutions: {len(solutions)}")
print()

# Check what's common across all solutions
# Option A: Exactly 3 batches on Tuesday
a_true = all(s['counts']['Tue'] == 3 for s in solutions)
print(f"A (exactly 3 on Tue): {a_true}")

# Option B: Exactly 3 batches on Friday
b_true = all(s['counts']['Fri'] == 3 for s in solutions)
print(f"B (exactly 3 on Fri): {b_true}")

# Option C: At least 2 batches on Monday
c_true = all(s['counts']['Mon'] >= 2 for s in solutions)
print(f"C (at least 2 on Mon): {c_true}")

# Option D: At least 2 batches on Thursday
d_true = all(s['counts']['Thu'] >= 2 for s in solutions)
print(f"D (at least 2 on Thu): {d_true}")

# Option E: Fewer on Mon than Tue
e_true = all(s['counts']['Mon'] < s['counts']['Tue'] for s in solutions)
print(f"E (Mon < Tue): {e_true}")

print()
print("Day count distributions across all solutions:")
for i, s in enumerate(solutions):
    print(f"  Sol {i+1}: {s['counts']} | {s}")