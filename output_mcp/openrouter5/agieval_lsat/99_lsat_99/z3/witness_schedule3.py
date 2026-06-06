from z3 import *

witnesses = ['F', 'G', 'H', 'I', 'J']
day_of = {w: Int(f'day_{w}') for w in witnesses}

# Base constraints
def add_base_constraints(s):
    for w in witnesses:
        s.add(day_of[w] >= 0, day_of[w] <= 2)
    s.add(day_of['F'] != day_of['G'])
    s.add(day_of['I'] == 2)
    s.add(Sum([If(day_of[w] == 1, 1, 0) for w in witnesses]) == 2)
    s.add(day_of['H'] != 0)
    s.add(Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Option A: Franco is the only witness scheduled to testify on Monday.
opt_a = And(day_of['F'] == 0, Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 1)

# Option B: Franco is scheduled to testify on the same day as Iturbe.
opt_b = (day_of['F'] == day_of['I'])

# Option C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(day_of['G'] == 1, day_of['H'] == 1)

# Option D: Garcia is the only witness scheduled to testify on Monday
# and Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d = And(
    day_of['G'] == 0,
    Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 1,
    day_of['H'] == 2,
    Sum([If(day_of[w] == 2, 1, 0) for w in witnesses]) == 2
)

# Option E: Jackson is scheduled to testify on Tuesday
# and two witnesses are scheduled to testify on Monday.
opt_e = And(
    day_of['J'] == 1,
    Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) == 2
)

# Use the exact skeleton from the prompt
solver = Solver()
add_base_constraints(solver)

found_options = []
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