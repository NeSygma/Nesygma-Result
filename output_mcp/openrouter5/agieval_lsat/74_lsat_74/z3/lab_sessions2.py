from z3 import *

# We have 6 lab sessions: 3 days (Wed, Thu, Fri) x 2 slots (morning, afternoon)
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Slots: 0=morning, 1=afternoon

assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

day = {a: Int(f'day_{a}') for a in assistants}
slot = {a: Int(f'slot_{a}') for a in assistants}

solver = Solver()

# Domain constraints: day in {0,1,2}, slot in {0,1}
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(slot[a] >= 0, slot[a] <= 1)

# Each session is different: each assistant gets a unique (day, slot) pair
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Or(day[a1] != day[a2], slot[a1] != slot[a2]))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day.
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day.
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa must lead an afternoon session.
solver.add(slot['Nessa'] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's.
solver.add(day['Julio'] < day['Olivia'])

# Additional condition: Julio and Kevin both lead morning sessions.
solver.add(slot['Julio'] == 0)
solver.add(slot['Kevin'] == 0)

# The question asks: "any of the following could be true EXCEPT"
# So we need to find which option CANNOT be true (is impossible).
# We test each option: if it's SAT, it COULD be true. If it's UNSAT, it CANNOT be true.
# The EXCEPT answer is the one that is UNSAT.

# Option A: Lan's session meets Wednesday morning. => day['Lan'] == 0, slot['Lan'] == 0
opt_a = And(day['Lan'] == 0, slot['Lan'] == 0)

# Option B: Lan's session meets Thursday afternoon. => day['Lan'] == 1, slot['Lan'] == 1
opt_b = And(day['Lan'] == 1, slot['Lan'] == 1)

# Option C: Nessa's session meets Friday afternoon. => day['Nessa'] == 2, slot['Nessa'] == 1
opt_c = And(day['Nessa'] == 2, slot['Nessa'] == 1)

# Option D: Olivia's session meets Thursday morning. => day['Olivia'] == 1, slot['Olivia'] == 0
opt_d = And(day['Olivia'] == 1, slot['Olivia'] == 0)

# Option E: Olivia's session meets Friday morning. => day['Olivia'] == 2, slot['Olivia'] == 0
opt_e = And(day['Olivia'] == 2, slot['Olivia'] == 0)

# Find which options are SAT (could be true) and which are UNSAT (cannot be true)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

# The EXCEPT answer is the one that CANNOT be true (unsat)
# There should be exactly one impossible option
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all could be true)")