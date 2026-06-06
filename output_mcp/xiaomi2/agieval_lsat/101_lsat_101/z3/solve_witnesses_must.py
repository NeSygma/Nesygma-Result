from z3 import *

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2

def make_base_solver():
    solver = Solver()
    days = [Int(f'day_{i}') for i in range(5)]
    F, G, H, I, J = 0, 1, 2, 3, 4

    for d in days:
        solver.add(Or(d == 0, d == 1, d == 2))

    # Franco and Garcia on different days
    solver.add(days[F] != days[G])

    # Iturbe on Wednesday
    solver.add(days[I] == 2)

    # Exactly 2 witnesses on Tuesday
    solver.add(Sum([If(days[i] == 1, 1, 0) for i in range(5)]) == 2)

    # Hong not on Monday
    solver.add(days[H] != 0)

    # At least 1 witness on Monday
    solver.add(Sum([If(days[i] == 0, 1, 0) for i in range(5)]) >= 1)

    # Jackson is the ONLY witness on Monday
    solver.add(days[J] == 0)
    solver.add(Sum([If(days[i] == 0, 1, 0) for i in range(5)]) == 1)

    return solver, days

# First, let's enumerate all valid schedules to understand the solution space
solver, days = make_base_solver()
F, G, H, I, J = 0, 1, 2, 3, 4

all_schedules = []
while solver.check() == sat:
    m = solver.model()
    sched = [m.evaluate(days[i]).as_long() for i in range(5)]
    all_schedules.append(sched)
    solver.add(Or([days[i] != sched[i] for i in range(5)]))

print(f"Total valid schedules: {len(all_schedules)}")
for s in all_schedules:
    day_names = ['Mon', 'Tue', 'Wed']
    print(f"  F={day_names[s[0]]}, G={day_names[s[1]]}, H={day_names[s[2]]}, I={day_names[s[3]]}, J={day_names[s[4]]}")

# Now check which options MUST be true (true in ALL schedules)
options = {
    "A": lambda d: d[F] == 2,  # Franco on Wednesday
    "B": lambda d: d[H] == 1,  # Hong on Tuesday
    "C": lambda d: d[G] == 1,  # Garcia on Tuesday
    "D": lambda d: d[F] == d[H],  # Franco same day as Hong
    "E": lambda d: d[G] == d[H],  # Garcia same day as Hong
}

must_be_true = []
for letter, cond_fn in options.items():
    all_true = all(cond_fn(s) for s in all_schedules)
    if all_true:
        must_be_true.append(letter)
    print(f"Option {letter}: {'MUST be true' if all_true else 'not necessarily true'}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-true options found")