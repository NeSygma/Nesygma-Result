from z3 import *

# Student names for reference
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_to_idx = {name: i for i, name in enumerate(students)}
N = len(students)

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = ["Monday", "Tuesday", "Wednesday"]
D = len(days)

# For each student and each day, we need to know:
# 1. Whether they give a report on that day
# 2. If they do, whether it's morning or afternoon
# We'll use arrays: reports[student][day] = 0 (no report), 1 (morning), 2 (afternoon)
reports = [[Int(f"reports_{s}_{d}") for d in range(D)] for s in range(N)]

solver = Solver()

# Base constraints:
# 1. Each student can give at most one report per day (morning OR afternoon, not both)
for s in range(N):
    for d in range(D):
        solver.add(Or(reports[s][d] == 0, reports[s][d] == 1, reports[s][d] == 2))

# 2. Exactly 2 reports per day (one morning, one afternoon)
for d in range(D):
    morning_count = Sum([If(reports[s][d] == 1, 1, 0) for s in range(N)])
    afternoon_count = Sum([If(reports[s][d] == 2, 1, 0) for s in range(N)])
    solver.add(morning_count == 1)
    solver.add(afternoon_count == 1)

# 3. Each student gives at most one report total (across all days)
for s in range(N):
    total_student_reports = Sum([If(reports[s][d] != 0, 1, 0) for d in range(D)])
    solver.add(total_student_reports <= 1)

# 4. Exactly 6 students give reports total
total_reports = Sum([If(reports[s][d] != 0, 1, 0) for s in range(N) for d in range(D)])
solver.add(total_reports == 6)

# 5. Tuesday is the only day George can give a report
george_idx = student_to_idx["George"]
for d in range(D):
    if d != 1:  # Not Tuesday
        solver.add(reports[george_idx][d] == 0)

# 6. Neither Olivia nor Robert can give an afternoon report
olivia_idx = student_to_idx["Olivia"]
robert_idx = student_to_idx["Robert"]
for d in range(D):
    solver.add(reports[olivia_idx][d] != 2)
    solver.add(reports[robert_idx][d] != 2)

# 7. If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
nina_idx = student_to_idx["Nina"]
helen_idx = student_to_idx["Helen"]
irving_idx = student_to_idx["Irving"]

# For each day except Wednesday
for d in range(2):  # Monday (0) and Tuesday (1)
    # If Nina gives a report on day d (morning or afternoon)
    nina_gives = Or(reports[nina_idx][d] == 1, reports[nina_idx][d] == 2)
    # Then on day d+1, both Helen and Irving must give reports (morning or afternoon)
    helen_next = Or(reports[helen_idx][d+1] == 1, reports[helen_idx][d+1] == 2)
    irving_next = Or(reports[irving_idx][d+1] == 1, reports[irving_idx][d+1] == 2)
    solver.add(Implies(nina_gives, And(helen_next, irving_next)))

# 8. Additional given: Kyle gives afternoon report on Tuesday
kyle_idx = student_to_idx["Kyle"]
solver.add(reports[kyle_idx][1] == 2)  # Tuesday is index 1

# 9. Additional given: Helen gives afternoon report on Wednesday
solver.add(reports[helen_idx][2] == 2)  # Wednesday is index 2

# Now evaluate each answer choice
# Answer choices are about morning reports on Monday, Tuesday, Wednesday respectively
# We need to check which choice is consistent with all constraints

found_options = []

# Option A: Irving, Lenore, Nina (morning reports on Mon, Tue, Wed)
opt_a = And(
    reports[student_to_idx["Irving"]][0] == 1,  # Irving morning Monday
    reports[student_to_idx["Lenore"]][1] == 1,  # Lenore morning Tuesday
    reports[student_to_idx["Nina"]][2] == 1     # Nina morning Wednesday
)

# Option B: Lenore, George, Irving
opt_b = And(
    reports[student_to_idx["Lenore"]][0] == 1,  # Lenore morning Monday
    reports[student_to_idx["George"]][1] == 1,  # George morning Tuesday
    reports[student_to_idx["Irving"]][2] == 1   # Irving morning Wednesday
)

# Option C: Nina, Irving, Lenore
opt_c = And(
    reports[student_to_idx["Nina"]][0] == 1,    # Nina morning Monday
    reports[student_to_idx["Irving"]][1] == 1,  # Irving morning Tuesday
    reports[student_to_idx["Lenore"]][2] == 1   # Lenore morning Wednesday
)

# Option D: Robert, George, Irving
opt_d = And(
    reports[student_to_idx["Robert"]][0] == 1,  # Robert morning Monday
    reports[student_to_idx["George"]][1] == 1,  # George morning Tuesday
    reports[student_to_idx["Irving"]][2] == 1   # Irving morning Wednesday
)

# Option E: Robert, Irving, Lenore
opt_e = And(
    reports[student_to_idx["Robert"]][0] == 1,  # Robert morning Monday
    reports[student_to_idx["Irving"]][1] == 1,  # Irving morning Tuesday
    reports[student_to_idx["Lenore"]][2] == 1   # Lenore morning Wednesday
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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