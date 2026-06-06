from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = ['F', 'G', 'H', 'I', 'J']
day_names = {0: "Mon", 1: "Tue", 2: "Wed"}

day = {w: Int(f'day_{w}') for w in witnesses}

solver = Solver()

# Domain constraints: each day is 0, 1, or 2
for w in witnesses:
    solver.add(day[w] >= 0, day[w] <= 2)

# Franco does not testify on the same day as Garcia
solver.add(day['F'] != day['G'])

# Iturbe testifies on Wednesday (day 2)
solver.add(day['I'] == 2)

# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(day[w] == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday (day 0)
solver.add(day['H'] != 0)

# At least one witness testifies on Monday (day 0)
solver.add(Sum([If(day[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition: Jackson is scheduled to testify on Wednesday (day 2)
solver.add(day['J'] == 2)

# Let's enumerate all possible schedules
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {w: m[day[w]].as_long() for w in witnesses}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([day[w] != m[day[w]].as_long() for w in witnesses]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: ", end="")
    for w in witnesses:
        print(f"{w}={day_names[sol[w]]}", end=" ")
    print()

# Now check each option across all solutions
# Option A: Franco on Monday
all_a = all(sol['F'] == 0 for sol in solutions)
# Option B: Garcia on Monday
all_b = all(sol['G'] == 0 for sol in solutions)
# Option C: Exactly one on Monday
all_c = all(sum(1 for w in witnesses if sol[w] == 0) == 1 for sol in solutions)
# Option D: Exactly two on Monday
all_d = all(sum(1 for w in witnesses if sol[w] == 0) == 2 for sol in solutions)
# Option E: Garcia same day as Hong
all_e = all(sol['G'] == sol['H'] for sol in solutions)

print(f"\nA (Franco on Monday) must be true: {all_a}")
print(f"B (Garcia on Monday) must be true: {all_b}")
print(f"C (Exactly one on Monday) must be true: {all_c}")
print(f"D (Exactly two on Monday) must be true: {all_d}")
print(f"E (Garcia same day as Hong) must be true: {all_e}")