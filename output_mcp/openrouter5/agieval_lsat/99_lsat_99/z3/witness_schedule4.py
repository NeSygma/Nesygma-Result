from z3 import *

witnesses = ['F', 'G', 'H', 'I', 'J']
day_of = {w: Int(f'day_{w}') for w in witnesses}

# Base constraints
def add_base_constraints(s):
    for w in witnesses:
        s.add(day_of[w] >= 0, day_of[w] <= 2)
    s.add(day_of['F'] != day_of['G'])
    s.add(day_of['I'] == 2)  # Wednesday
    s.add(Sum([If(day_of[w] == 1, 1, 0) for w in witnesses]) == 2)  # exactly two on Tuesday
    s.add(day_of['H'] != 0)  # Hong not Monday
    s.add(Sum([If(day_of[w] == 0, 1, 0) for w in witnesses]) >= 1)  # at least one Monday

# The question asks: "Which one of the following CANNOT be true?"
# So we need to find the option that is UNSAT (impossible) under the base constraints.
# Let's check each option individually.

solver = Solver()
add_base_constraints(solver)

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

# For "CANNOT be true", we want the option that is UNSAT (impossible).
# So we check each option. The one that returns unsat is the answer.
# But we need exactly one unsat option.

results = {}
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    add_base_constraints(s)
    s.add(constr)
    res = s.check()
    results[letter] = res
    print(f"Option {letter}: {res}")

# Find which option is unsat
unsat_options = [k for k, v in results.items() if v == unsat]
sat_options = [k for k, v in results.items() if v == sat]

print(f"unsat options: {unsat_options}")
print(f"sat options: {sat_options}")

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")