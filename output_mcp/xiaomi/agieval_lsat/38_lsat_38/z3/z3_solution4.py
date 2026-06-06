from z3 import *

# Let me re-read the problem more carefully.
# "How many of the days, Monday through Friday, are such that at most two batches 
# of cookies could be made on that day?"
#
# I think this is asking: for how many days is it POSSIBLE that at most 2 batches are made?
# i.e., there exists a valid schedule where that day has <= 2 batches.
#
# But that would be all 5 days since you could always arrange for any day to have 0 batches.
# Unless the constraints force certain days to have batches...
#
# Wait, let me reconsider. Maybe the question is asking:
# "How many days MUST have at most 2 batches?" - i.e., in ALL valid schedules, those days have <= 2.
#
# But my previous check showed all days CAN have 3 batches. Let me verify by finding actual models.

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 1st, 2nd, 3rd for each type

solver = Solver()

batch = [[Int(f'batch_{t}_{b}') for b in range(3)] for t in range(3)]

for t in range(3):
    for b in range(3):
        solver.add(batch[t][b] >= 0, batch[t][b] <= 4)

for t in range(3):
    solver.add(Distinct(batch[t][0], batch[t][1], batch[t][2]))

all_batches = [batch[t][b] for t in range(3) for b in range(3)]
solver.add(Or([b == 0 for b in all_batches]))

solver.add(batch[0][1] == batch[1][0])
solver.add(batch[2][1] == 3)

# Let me find all valid schedules and count batches per day
solutions = []
decision_vars = [batch[t][b] for t in range(3) for b in range(3)]

while solver.check() == sat:
    m = solver.model()
    sol = {}
    for t in range(3):
        for b in range(3):
            sol[(t,b)] = m[batch[t][b]].as_long()
    solutions.append(sol)
    solver.add(Or([batch[t][b] != m[batch[t][b]] for t in range(3) for b in range(3)]))

print(f"Total valid schedules: {len(solutions)}")

# For each solution, count batches per day
for i, sol in enumerate(solutions):
    day_counts = [0]*5
    for (t,b), d in sol.items():
        day_counts[d] += 1
    print(f"Schedule {i}: day_counts={day_counts}, schedule={sol}")

# Now check: for each day, what are the possible batch counts?
for d in range(5):
    counts = set()
    for sol in solutions:
        day_count = sum(1 for (t,b), dd in sol.items() if dd == d)
        counts.add(day_count)
    print(f"Day {d}: possible counts = {counts}")