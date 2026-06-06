from z3 import *

solver = Solver()

# Students: George(G), Helen(H), Irving(I), Kyle(K), Lenore(L), Nina(N), Olivia(O), Robert(R)
students = ['G', 'H', 'I', 'K', 'L', 'N', 'O', 'R']

# day[s] = 0 (no report), 1 (Monday), 2 (Tuesday), 3 (Wednesday)
day = {s: Int(f'day_{s}') for s in students}
# slot[s] = 0 (morning), 1 (afternoon)
slot = {s: Int(f'slot_{s}') for s in students}

# Domain constraints
for s in students:
    solver.add(day[s] >= 0, day[s] <= 3)
    solver.add(slot[s] >= 0, slot[s] <= 1)

# Exactly 6 students report (2 don't)
solver.add(Sum([If(day[s] > 0, 1, 0) for s in students]) == 6)

# For each day, exactly 2 students report
for d in [1, 2, 3]:
    solver.add(Sum([If(day[s] == d, 1, 0) for s in students]) == 2)

# For each day, exactly 1 morning and 1 afternoon
for d in [1, 2, 3]:
    solver.add(Sum([If(And(day[s] == d, slot[s] == 0), 1, 0) for s in students]) == 1)
    solver.add(Sum([If(And(day[s] == d, slot[s] == 1), 1, 0) for s in students]) == 1)

# Constraint 1: Tuesday is the only day George can give a report
# (George either reports on Tuesday or doesn't report at all)
solver.add(Or(day['G'] == 0, day['G'] == 2))

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(day['O'] > 0, slot['O'] == 0))
solver.add(Implies(day['R'] > 0, slot['R'] == 0))

# Constraint 3: If Nina gives a report, then on the next day Helen and Irving
# must both give reports, unless Nina's report is given on Wednesday.
# Nina on Monday -> Helen and Irving on Tuesday
solver.add(Implies(day['N'] == 1, And(day['H'] == 2, day['I'] == 2)))
# Nina on Tuesday -> Helen and Irving on Wednesday
solver.add(Implies(day['N'] == 2, And(day['H'] == 3, day['I'] == 3)))
# Nina on Wednesday or Nina doesn't report -> no constraint

# First, verify base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base constraints SAT. Example schedule:")
    for s in students:
        d = m[day[s]].as_long()
        sl = m[slot[s]].as_long()
        day_name = {0: "none", 1: "Mon", 2: "Tue", 3: "Wed"}[d]
        slot_name = {0: "AM", 1: "PM"}[sl] if d > 0 else ""
        print(f"  {s}: {day_name} {slot_name}")
else:
    print("Base constraints UNSAT - error in modeling!")

# Now check each option:
# "Which pair, if they give reports on the same day, MUST give reports on Wednesday?"
# For each option: add same-day constraint + day != Wednesday, check if UNSAT
options = {
    'A': ('G', 'L'),
    'B': ('H', 'N'),
    'C': ('I', 'R'),
    'D': ('K', 'N'),
    'E': ('O', 'K'),
}

found_options = []

for letter, (s1, s2) in options.items():
    solver.push()
    # Both students report (day > 0)
    solver.add(day[s1] > 0)
    solver.add(day[s2] > 0)
    # They are on the same day
    solver.add(day[s1] == day[s2])
    # Try to find a solution where they are NOT on Wednesday
    solver.add(day[s1] != 3)
    result = solver.check()
    if result == unsat:
        # They MUST be on Wednesday
        found_options.append(letter)
        print(f"Option {letter} ({s1},{s2}): MUST be Wednesday (no other day possible)")
    elif result == sat:
        m = solver.model()
        d = m[day[s1]].as_long()
        day_name = {1: "Monday", 2: "Tuesday", 3: "Wednesday"}[d]
        print(f"Option {letter} ({s1},{s2}): Can be on {day_name} - NOT forced to Wednesday")
    else:
        print(f"Option {letter} ({s1},{s2}): UNKNOWN")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")