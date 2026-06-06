from z3 import *

# Create solver
solver = Solver()

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
# Create variables: day (0=Wed, 1=Thu, 2=Fri) and time (0=morning, 1=afternoon)
day = {a: Int(f"day_{a}") for a in assistants}
time = {a: Int(f"time_{a}") for a in assistants}

# Domain constraints: days 0-2, times 0-1
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day["Kevin"] == day["Rebecca"])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day["Lan"] != day["Olivia"])

# Constraint 3: Nessa must lead an afternoon session
solver.add(time["Nessa"] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day["Julio"] < day["Olivia"])

# Additional given: Julio leads Thursday afternoon
# Thursday is day 1, afternoon is time 1
solver.add(day["Julio"] == 1)
solver.add(time["Julio"] == 1)

# All assistants must have distinct sessions (different day-time combinations)
# Since there are exactly 6 sessions and 6 assistants, each session is unique
# We need to ensure no two assistants have same day AND same time
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1, a2 = assistants[i], assistants[j]
        solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))

# Now we need to check: how many of the other lab assistants can one determine which sessions they lead?
# This means: for each assistant (except Julio), is their session uniquely determined by the constraints?
# We'll check each assistant by seeing if there's only one possible (day, time) combination

# First, find all possible solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for a in assistants:
        sol[a] = (m[day[a]].as_long(), m[time[a]].as_long())
    solutions.append(sol)
    
    # Blocking clause to find next solution
    block = []
    for a in assistants:
        block.append(Or(day[a] != sol[a][0], time[a] != sol[a][1]))
    solver.add(Or(block))

print(f"Total solutions found: {len(solutions)}")

# For each assistant (except Julio), check if their session is uniquely determined
determined = []
for a in assistants:
    if a == "Julio":
        continue
    # Get all possible (day, time) pairs for this assistant across solutions
    possible_sessions = set()
    for sol in solutions:
        possible_sessions.add(sol[a])
    if len(possible_sessions) == 1:
        determined.append(a)
        print(f"{a} is determined: day={list(possible_sessions)[0][0]}, time={list(possible_sessions)[0][1]}")
    else:
        print(f"{a} is NOT determined: possible sessions = {possible_sessions}")

print(f"\nNumber of other assistants determined: {len(determined)}")

# Now we need to match this to the answer choices
# The question asks: "for how many of the other lab assistants can one determine which sessions they lead?"
# Answer choices: (A)one (B)two (C)three (D)four (E)five

# We need to check which answer choice matches our count
count = len(determined)

# Define the options based on the count
opt_a_constr = (count == 1)
opt_b_constr = (count == 2)
opt_c_constr = (count == 3)
opt_d_constr = (count == 4)
opt_e_constr = (count == 5)

# Now use the required multiple choice evaluation skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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