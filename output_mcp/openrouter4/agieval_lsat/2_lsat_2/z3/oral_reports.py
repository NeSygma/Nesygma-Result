from z3 import *

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: AM=0, PM=1
# Students: 0=George, 1=Helen, 2=Irving, 3=Nina, 4=Olivia, 5=Robert
# (Kyle and Lenore don't give reports, so only these 6 report)

students = ["George", "Helen", "Irving", "Nina", "Olivia", "Robert"]
n_students = 6
days = [0, 1, 2]  # Mon, Tue, Wed
times = [0, 1]    # AM, PM

# assign[s][d][t] is a Bool variable
assign = [[[Bool(f"assign_{s}_{d}_{t}") for t in times] for d in days] for s in range(n_students)]

solver = Solver()

# 1. Each slot has exactly one report
for d in days:
    for t in times:
        solver.add(Sum([If(assign[s][d][t], 1, 0) for s in range(n_students)]) == 1)

# 2. Each student gives exactly one report
for s in range(n_students):
    solver.add(Sum([If(assign[s][d][t], 1, 0) for d in days for t in times]) == 1)

# 3. George (index 0) can only give on Tuesday (day 1)
for d in days:
    for t in times:
        if d != 1:
            solver.add(assign[0][d][t] == False)

# 4. Neither Olivia (index 4) nor Robert (index 5) can give an afternoon report
for d in days:
    solver.add(assign[4][d][1] == False)  # Olivia no PM
    solver.add(assign[5][d][1] == False)  # Robert no PM

# 5. If Nina gives a report, then on the next day Helen and Irving must both give reports,
#    unless Nina's report is given on Wednesday (day 2).
# For each day d (0=Mon, 1=Tue), if Nina gives that day, then next day (d+1) must have Helen and Irving.
for d in [0, 1]:
    nina_gives_day = Or([assign[3][d][t] for t in times])  # Nina = index 3
    helen_gives_next = Or([assign[1][d+1][t] for t in times])  # Helen = index 1
    irving_gives_next = Or([assign[2][d+1][t] for t in times])  # Irving = index 2
    solver.add(Implies(nina_gives_day, And(helen_gives_next, irving_gives_next)))

# Now evaluate each answer choice
options = [
    ("A", (1, 0, 3)),  # Helen, George, Nina -> indices (1, 0, 3)
    ("B", (2, 5, 1)),  # Irving, Robert, Helen -> (2, 5, 1)
    ("C", (3, 1, 4)),  # Nina, Helen, Olivia -> (3, 1, 4)
    ("D", (4, 5, 2)),  # Olivia, Robert, Irving -> (4, 5, 2)
    ("E", (5, 0, 1)),  # Robert, George, Helen -> (5, 0, 1)
]

found_options = []
for letter, (mon_am, tue_am, wed_am) in options:
    solver.push()
    # morning reports: Monday AM, Tuesday AM, Wednesday AM
    solver.add(assign[mon_am][0][0] == True)  # Monday AM
    solver.add(assign[tue_am][1][0] == True)  # Tuesday AM
    solver.add(assign[wed_am][2][0] == True)  # Wednesday AM
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