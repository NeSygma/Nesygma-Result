from z3 import *

# Define students as symbolic constants
students = [
    "George", "Helen", "Irving", "Kyle", 
    "Lenore", "Nina", "Olivia", "Robert"
]
student_to_int = {s: i for i, s in enumerate(students)}
int_to_student = students

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Time: 0=Morning, 1=Afternoon
# Schedule: schedule[day][time] = student (as Int)
schedule = [[Int(f"schedule_{d}_{t}") for t in range(2)] for d in range(3)]

# Helper: All assigned students must be distinct and from the list
all_slots = [schedule[d][t] for d in range(3) for t in range(2)]

solver = Solver()

# Constraint 1: Exactly 6 distinct students are assigned (2 per day, 3 days = 6 slots)
# We enforce that all assigned students are distinct and from the list
for slot in all_slots:
    solver.add(Or([slot == student_to_int[s] for s in students]))

solver.add(Distinct(all_slots))

# Constraint 2: George can only give a report on Tuesday
solver.add(schedule[0][0] != student_to_int["George"])
solver.add(schedule[0][1] != student_to_int["George"])
solver.add(schedule[2][0] != student_to_int["George"])
solver.add(schedule[2][1] != student_to_int["George"])

# Constraint 3: Neither Olivia nor Robert can give an afternoon report
solver.add(schedule[0][1] != student_to_int["Olivia"])
solver.add(schedule[1][1] != student_to_int["Olivia"])
solver.add(schedule[2][1] != student_to_int["Olivia"])

solver.add(schedule[0][1] != student_to_int["Robert"])
solver.add(schedule[1][1] != student_to_int["Robert"])
solver.add(schedule[2][1] != student_to_int["Robert"])

# Constraint 4: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday.
# We need to check for Nina in Monday or Tuesday slots
nina_idx = student_to_int["Nina"]
helen_idx = student_to_int["Helen"]
irving_idx = student_to_int["Irving"]

# If Nina is on Monday morning (day 0, time 0)
solver.add(Implies(
    schedule[0][0] == nina_idx,
    And(
        Or([schedule[1][0] == helen_idx, schedule[1][1] == helen_idx]),
        Or([schedule[1][0] == irving_idx, schedule[1][1] == irving_idx])
    )
))

# If Nina is on Monday afternoon (day 0, time 1)
solver.add(Implies(
    schedule[0][1] == nina_idx,
    And(
        Or([schedule[1][0] == helen_idx, schedule[1][1] == helen_idx]),
        Or([schedule[1][0] == irving_idx, schedule[1][1] == irving_idx])
    )
))

# If Nina is on Tuesday morning (day 1, time 0)
solver.add(Implies(
    schedule[1][0] == nina_idx,
    And(
        Or([schedule[2][0] == helen_idx, schedule[2][1] == helen_idx]),
        Or([schedule[2][0] == irving_idx, schedule[2][1] == irving_idx])
    )
))

# If Nina is on Tuesday afternoon (day 1, time 1)
solver.add(Implies(
    schedule[1][1] == nina_idx,
    And(
        Or([schedule[2][0] == helen_idx, schedule[2][1] == helen_idx]),
        Or([schedule[2][0] == irving_idx, schedule[2][1] == irving_idx])
    )
))

# If Nina is on Wednesday, no constraint (already handled by Implies structure)

# Now evaluate each option
found_options = []

# Option A: Mon. morning: Helen; Mon. afternoon: Robert; Tues. morning: Olivia; Tues. afternoon: Irving; Wed. morning: Lenore; Wed. afternoon: Kyle
opt_a_constr = And(
    schedule[0][0] == student_to_int["Helen"],
    schedule[0][1] == student_to_int["Robert"],
    schedule[1][0] == student_to_int["Olivia"],
    schedule[1][1] == student_to_int["Irving"],
    schedule[2][0] == student_to_int["Lenore"],
    schedule[2][1] == student_to_int["Kyle"]
)

# Option B: Mon. morning: Irving; Mon. afternoon: Olivia; Tues. morning: Helen; Tues. afternoon: Kyle; Wed. morning: Nina; Wed. afternoon: Lenore
opt_b_constr = And(
    schedule[0][0] == student_to_int["Irving"],
    schedule[0][1] == student_to_int["Olivia"],
    schedule[1][0] == student_to_int["Helen"],
    schedule[1][1] == student_to_int["Kyle"],
    schedule[2][0] == student_to_int["Nina"],
    schedule[2][1] == student_to_int["Lenore"]
)

# Option C: Mon. morning: Lenore; Mon. afternoon: Helen; Tues. morning: George; Tues. afternoon: Kyle; Wed. morning: Robert; Wed. afternoon: Irving
opt_c_constr = And(
    schedule[0][0] == student_to_int["Lenore"],
    schedule[0][1] == student_to_int["Helen"],
    schedule[1][0] == student_to_int["George"],
    schedule[1][1] == student_to_int["Kyle"],
    schedule[2][0] == student_to_int["Robert"],
    schedule[2][1] == student_to_int["Irving"]
)

# Option D: Mon. morning: Nina; Mon. afternoon: Helen; Tues. morning: Robert; Tues. afternoon: Irving; Wed. morning: Olivia; Wed. afternoon: Lenore
opt_d_constr = And(
    schedule[0][0] == student_to_int["Nina"],
    schedule[0][1] == student_to_int["Helen"],
    schedule[1][0] == student_to_int["Robert"],
    schedule[1][1] == student_to_int["Irving"],
    schedule[2][0] == student_to_int["Olivia"],
    schedule[2][1] == student_to_int["Lenore"]
)

# Option E: Mon. morning: Olivia; Mon. afternoon: Nina; Tues. morning: Irving; Tues. afternoon: Helen; Wed. morning: Kyle; Wed. afternoon: George
opt_e_constr = And(
    schedule[0][0] == student_to_int["Olivia"],
    schedule[0][1] == student_to_int["Nina"],
    schedule[1][0] == student_to_int["Irving"],
    schedule[1][1] == student_to_int["Helen"],
    schedule[2][0] == student_to_int["Kyle"],
    schedule[2][1] == student_to_int["George"]
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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