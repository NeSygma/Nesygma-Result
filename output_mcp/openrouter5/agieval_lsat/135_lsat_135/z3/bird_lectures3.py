from z3 import *

solver = Solver()

# 5 lectures, positions 0..4 (first=0, fourth=3)
# Locations: 0 = Gladwyn Hall, 1 = Howard Auditorium
loc = [Int(f"loc_{i}") for i in range(5)]
for i in range(5):
    solver.add(Or(loc[i] == 0, loc[i] == 1))

# Birds: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# We assign each bird to a position (0..4)
bird_pos = [Int(f"bird_{b}") for b in range(5)]
for b in range(5):
    solver.add(bird_pos[b] >= 0, bird_pos[b] <= 4)
solver.add(Distinct(bird_pos))

# The first lecture (position 0) is in Gladwyn Hall.
solver.add(loc[0] == 0)

# The fourth lecture (position 3) is in Howard Auditorium.
solver.add(loc[3] == 1)

# Exactly three of the lectures are in Gladwyn Hall.
solver.add(Sum([If(loc[i] == 0, 1, 0) for i in range(5)]) == 3)

# The lecture on sandpipers (bird 3) is in Howard Auditorium and is given earlier than the lecture on oystercatchers (bird 0).
# sandpipers in Howard: loc[bird_pos[3]] == 1
solver.add(Or([And(bird_pos[3] == i, loc[i] == 1) for i in range(5)]))
# sandpipers earlier than oystercatchers
solver.add(bird_pos[3] < bird_pos[0])

# The lecture on terns (bird 4) is given earlier than the lecture on petrels (bird 1), which is in Gladwyn Hall.
solver.add(bird_pos[4] < bird_pos[1])
# petrels in Gladwyn: loc[bird_pos[1]] == 0
solver.add(Or([And(bird_pos[1] == i, loc[i] == 0) for i in range(5)]))

# The question asks: "Which one of the following must be false?"
# This means we need to find the option that is IMPOSSIBLE (unsat) under the constraints.
# The other options should be possible (sat).

# Let's check each option individually.
results = {}
for letter, constr in [("A", And(loc[0] == 0, loc[1] == 0)),
                        ("B", And(loc[1] == 1, loc[2] == 1)),
                        ("C", And(loc[1] == 0, loc[4] == 0)),
                        ("D", And(loc[2] == 1, loc[3] == 1)),
                        ("E", And(loc[2] == 0, loc[4] == 0))]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    results[letter] = res
    solver.pop()
    print(f"Option {letter}: {res}")

# The option that is UNSAT is the one that must be false.
unsat_options = [letter for letter, res in results.items() if res == unsat]
sat_options = [letter for letter, res in results.items() if res == sat]

print(f"\nUNSAT options (must be false): {unsat_options}")
print(f"SAT options (could be true): {sat_options}")

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")