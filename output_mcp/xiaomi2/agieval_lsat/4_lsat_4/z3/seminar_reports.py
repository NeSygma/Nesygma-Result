from z3 import *

solver = Solver()

# Students: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
names = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
N = 8

# For each student: whether they report, which day (0=Mon,1=Tue,2=Wed), which slot (0=morn,1=aft)
reports = [Bool(f"reports_{i}") for i in range(N)]
day = [Int(f"day_{i}") for i in range(N)]
slot = [Int(f"slot_{i}") for i in range(N)]

# Domain constraints for day and slot
for i in range(N):
    solver.add(day[i] >= 0, day[i] <= 2)
    solver.add(slot[i] >= 0, slot[i] <= 1)

# Exactly 6 of 8 students give reports
solver.add(Sum([If(reports[i], 1, 0) for i in range(N)]) == 6)

# Each of the 6 time slots (day d, slot s) has exactly one student
for d in range(3):
    for s in range(2):
        # At least one student in this slot
        solver.add(Or([And(reports[i], day[i] == d, slot[i] == s) for i in range(N)]))
        # At most one student in this slot
        for i in range(N):
            for j in range(i+1, N):
                solver.add(Implies(And(reports[i], day[i] == d, slot[i] == s,
                                       reports[j], day[j] == d, slot[j] == s), i == j))

# Constraint 1: Tuesday is the only day George can give a report
solver.add(Implies(reports[0], day[0] == 1))

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(reports[6], slot[6] == 0))  # Olivia
solver.add(Implies(reports[7], slot[7] == 0))  # Robert

# Constraint 3: If Nina reports and not on Wednesday, then next day Helen and Irving both report
# Nina on Monday (day=0) -> Helen and Irving both report on Tuesday (day=1)
solver.add(Implies(And(reports[5], day[5] == 0), And(reports[1], day[1] == 1, reports[2], day[2] == 1)))
# Nina on Tuesday (day=1) -> Helen and Irving both report on Wednesday (day=2)
solver.add(Implies(And(reports[5], day[5] == 1), And(reports[1], day[1] == 2, reports[2], day[2] == 2)))
# Nina on Wednesday (day=2) -> no constraint

# Additional conditions: George, Nina, Robert all give reports
solver.add(reports[0] == True)  # George
solver.add(reports[5] == True)  # Nina
solver.add(reports[7] == True)  # Robert

# George, Nina, Robert are on different days
solver.add(day[0] != day[5])  # George != Nina
solver.add(day[0] != day[7])  # George != Robert
solver.add(day[5] != day[7])  # Nina != Robert

# George is on Tuesday (from constraint 1)
solver.add(day[0] == 1)

# So Nina and Robert are on Monday and Wednesday (in some order)
# Nina != Tuesday, Robert != Tuesday

# Define option constraints
opt_a = And(reports[1], day[1] == 2)  # Helen reports on Wednesday
opt_b = And(reports[5], day[5] == 0)  # Nina reports on Monday
opt_c = And(reports[5], day[5] == 1)  # Nina reports on Tuesday
opt_d = And(reports[6], day[6] == 0)  # Olivia reports on Monday
opt_e = And(reports[7], day[7] == 2)  # Robert reports on Wednesday

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        for i in range(N):
            if m.evaluate(reports[i]):
                print(f"  {names[i]}: day={m[day[i]]}, slot={'morning' if m[slot[i]]==0 else 'afternoon'}")
    else:
        print(f"Option {letter}: {result}")
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