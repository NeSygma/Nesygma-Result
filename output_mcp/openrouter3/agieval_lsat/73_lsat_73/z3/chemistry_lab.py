from z3 import *

# Create solver
solver = Solver()

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
J, K, L, N, O, R = 0, 1, 2, 3, 4, 5  # indices for convenience

# Variables: day[assistant] (0=Wed, 1=Thu, 2=Fri), time[assistant] (0=morning, 1=afternoon)
day = [Int(f"day_{a}") for a in assistants]
time = [Int(f"time_{a}") for a in assistants]

# Domain constraints for days and times
for i in range(6):
    solver.add(day[i] >= 0, day[i] <= 2)  # 0=Wed, 1=Thu, 2=Fri
    solver.add(time[i] >= 0, time[i] <= 1)  # 0=morning, 1=afternoon

# Constraint 1: Kevin and Rebecca same day
solver.add(day[K] == day[R])

# Constraint 2: Lan and Olivia different days
solver.add(day[L] != day[O])

# Constraint 3: Nessa afternoon
solver.add(time[N] == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(day[J] < day[O])

# Constraint 5: Kevin's day is day before Nessa's
solver.add(day[K] == day[N] - 1)

# Additional: All sessions must be distinct (each day-time combination used exactly once)
# There are 6 sessions: 3 days × 2 times
# We need to ensure no two assistants have same (day, time) pair
for i in range(6):
    for j in range(i+1, 6):
        solver.add(Or(day[i] != day[j], time[i] != time[j]))

# Now test each answer choice for Thursday afternoon session
# Thursday is day 1, afternoon is time 1
# So we're looking for assistants who could have day=1 and time=1

# Define options as constraints that the assistant could be Thursday afternoon
# Option A: Julio or Nessa could be Thursday afternoon
opt_a = Or(And(day[J] == 1, time[J] == 1), And(day[N] == 1, time[N] == 1))

# Option B: Kevin or Rebecca could be Thursday afternoon
opt_b = Or(And(day[K] == 1, time[K] == 1), And(day[R] == 1, time[R] == 1))

# Option C: Kevin, Nessa, or Rebecca could be Thursday afternoon
opt_c = Or(And(day[K] == 1, time[K] == 1), 
           And(day[N] == 1, time[N] == 1),
           And(day[R] == 1, time[R] == 1))

# Option D: Julio, Kevin, Nessa, or Rebecca could be Thursday afternoon
opt_d = Or(And(day[J] == 1, time[J] == 1),
           And(day[K] == 1, time[K] == 1),
           And(day[N] == 1, time[N] == 1),
           And(day[R] == 1, time[R] == 1))

# Option E: Julio, Kevin, Lan, Nessa, or Rebecca could be Thursday afternoon
opt_e = Or(And(day[J] == 1, time[J] == 1),
           And(day[K] == 1, time[K] == 1),
           And(day[L] == 1, time[L] == 1),
           And(day[N] == 1, time[N] == 1),
           And(day[R] == 1, time[R] == 1))

# Test each option
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