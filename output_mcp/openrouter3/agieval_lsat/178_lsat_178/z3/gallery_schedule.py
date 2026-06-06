from z3 import *

# Student IDs
G, H, J, K, L = 0, 1, 2, 3, 4
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=first, 1=second
work = [[Int(f"work_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Each shift has exactly one student (0-4)
for d in range(5):
    for s in range(2):
        solver.add(work[d][s] >= 0)
        solver.add(work[d][s] <= 4)

# No student works both shifts of any day
for d in range(5):
    solver.add(work[d][0] != work[d][1])

# Each student works exactly two shifts total
student_shifts = [Sum([If(work[d][s] == sid, 1, 0) for d in range(5) for s in range(2)]) for sid in range(5)]
for sid in range(5):
    solver.add(student_shifts[sid] == 2)

# Louise works the second shift on two consecutive days
# Means: there exists some day d (0-3) such that work[d][1] == L and work[d+1][1] == L
louise_consecutive = Or([And(work[d][1] == L, work[d+1][1] == L) for d in range(4)])
solver.add(louise_consecutive)

# Grecia works the first shift on two nonconsecutive days
# Means: there exist two days d1, d2 with |d1-d2| >= 2 such that work[d1][0] == G and work[d2][0] == G
grecia_nonconsecutive = Or([And(work[d1][0] == G, work[d2][0] == G, Abs(d1 - d2) >= 2) for d1 in range(5) for d2 in range(5) if d1 != d2])
solver.add(grecia_nonconsecutive)

# Katya works on Tuesday and Friday (day 1 and day 4)
# Means: on day 1, at least one shift is K; on day 4, at least one shift is K
solver.add(Or(work[1][0] == K, work[1][1] == K))
solver.add(Or(work[4][0] == K, work[4][1] == K))

# Hakeem and Joe work on the same day at least once
same_day_HJ = Or([And(work[d][0] == H, work[d][1] == J) for d in range(5)])  # H first, J second
same_day_JH = Or([And(work[d][0] == J, work[d][1] == H) for d in range(5)])  # J first, H second
solver.add(Or(same_day_HJ, same_day_JH))

# Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(And(work[d][0] == G, work[d][1] == L)))
    solver.add(Not(And(work[d][0] == L, work[d][1] == G)))
    # Also ensure they don't both work on same day in any shift combination
    solver.add(Or(work[d][0] != G, work[d][1] != L))
    solver.add(Or(work[d][0] != L, work[d][1] != G))

# Additional condition: At least one day where Grecia and Joe both work
gj_together = Or([Or(And(work[d][0] == G, work[d][1] == J), And(work[d][0] == J, work[d][1] == G)) for d in range(5)])
solver.add(gj_together)

# Now test each option
found_options = []

# Option A: Grecia works the first shift on Tuesday (day 1, shift 0)
opt_a = (work[1][0] == G)

# Option B: Hakeem works the second shift on Monday (day 0, shift 1)
opt_b = (work[0][1] == H)

# Option C: Hakeem works the second shift on Wednesday (day 2, shift 1)
opt_c = (work[2][1] == H)

# Option D: Joe works the first shift on Wednesday (day 2, shift 0)
opt_d = (work[2][0] == J)

# Option E: Joe works the first shift on Thursday (day 3, shift 0)
opt_e = (work[3][0] == J)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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