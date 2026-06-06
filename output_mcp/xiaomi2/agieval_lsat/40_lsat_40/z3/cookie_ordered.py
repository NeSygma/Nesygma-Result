from z3 import *

# Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
# Wednesday (3) is excluded
VALID_DAYS = [1, 2, 4, 5]

# Batches ordered chronologically: O1<O2<O3 means O1 is earliest oatmeal batch
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

all_batches = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

solver = Solver()

# Each batch on a valid day (not Wednesday)
for b in all_batches:
    solver.add(Or([b == d for d in VALID_DAYS]))

# Chronological ordering within each kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)

# At least one batch on Monday
solver.add(Or([b == 1 for b in all_batches]))

# Second oatmeal same day as first peanut butter
solver.add(O2 == P1)

# Second sugar on Thursday
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
        sol[f"{'O1 O2 O3 P1 P2 P3 S1 S2 S3'.split()[i]}"] = day_names[int(str(m.eval(b)))]
    
    counts = {}
    for d in VALID_DAYS:
        counts[day_names[d]] = sum(1 for b in all_batches if int(str(m.eval(b))) == d)
    sol['counts'] = counts
    solutions.append(sol)
    
    solver.add(Or([b != m.eval(b) for b in all_batches]))

print(f"Total solutions: {len(solutions)}")
print()

# Check what's common across all solutions
a_true = all(s['counts']['Tue'] == 3 for s in solutions)
print(f"A (exactly 3 on Tue): {a_true}")

b_true = all(s['counts']['Fri'] == 3 for s in solutions)
print(f"B (exactly 3 on Fri): {b_true}")

c_true = all(s['counts']['Mon'] >= 2 for s in solutions)
print(f"C (at least 2 on Mon): {c_true}")

d_true = all(s['counts']['Thu'] >= 2 for s in solutions)
print(f"D (at least 2 on Thu): {d_true}")

e_true = all(s['counts']['Mon'] < s['counts']['Tue'] for s in solutions)
print(f"E (Mon < Tue): {e_true}")

print()
# Show first 10 solutions
for i, s in enumerate(solutions[:20]):
    print(f"  Sol {i+1}: {s['counts']} | {s}")