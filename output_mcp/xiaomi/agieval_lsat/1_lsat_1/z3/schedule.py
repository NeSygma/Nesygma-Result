from z3 import *

# Define the students
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
days = ['Monday', 'Tuesday', 'Wednesday']
slots = ['morning', 'afternoon']

# Create symbolic variables: for each day and slot, which student gives the report
# We'll use Int variables representing student indices (0-7)
report = {}
for d in days:
    for s in slots:
        report[(d, s)] = Int(f'report_{d}_{s}')

solver = Solver()

# Each report must be a valid student index (0-7)
for d in days:
    for s in slots:
        solver.add(report[(d, s)] >= 0, report[(d, s)] <= 7)

# Exactly six students give reports (two per day, three days)
# So exactly six distinct students appear in the six slots
all_reports = [report[(d, s)] for d in days for s in slots]
solver.add(Distinct(all_reports))

# Exactly two reports per day (already enforced by having two slots per day)

# Condition 1: Tuesday is the only day on which George can give a report.
# George is index 0
george = 0
# George cannot give a report on Monday or Wednesday
solver.add(report[('Monday', 'morning')] != george)
solver.add(report[('Monday', 'afternoon')] != george)
solver.add(report[('Wednesday', 'morning')] != george)
solver.add(report[('Wednesday', 'afternoon')] != george)
# George can give a report on Tuesday (but not required)

# Condition 2: Neither Olivia nor Robert can give an afternoon report.
olivia = 6
robert = 7
solver.add(report[('Monday', 'afternoon')] != olivia)
solver.add(report[('Monday', 'afternoon')] != robert)
solver.add(report[('Tuesday', 'afternoon')] != olivia)
solver.add(report[('Tuesday', 'afternoon')] != robert)
solver.add(report[('Wednesday', 'afternoon')] != olivia)
solver.add(report[('Wednesday', 'afternoon')] != robert)

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
nina = 4
helen = 1
irving = 2

# For each day Nina could give a report (Monday or Tuesday)
# If Nina on Monday, then Tuesday must have both Helen and Irving
nina_monday = Or(report[('Monday', 'morning')] == nina, report[('Monday', 'afternoon')] == nina)
tuesday_has_helen = Or(report[('Tuesday', 'morning')] == helen, report[('Tuesday', 'afternoon')] == helen)
tuesday_has_irving = Or(report[('Tuesday', 'morning')] == irving, report[('Tuesday', 'afternoon')] == irving)
solver.add(Implies(nina_monday, And(tuesday_has_helen, tuesday_has_irving)))

# If Nina on Tuesday, then Wednesday must have both Helen and Irving
nina_tuesday = Or(report[('Tuesday', 'morning')] == nina, report[('Tuesday', 'afternoon')] == nina)
wednesday_has_helen = Or(report[('Wednesday', 'morning')] == helen, report[('Wednesday', 'afternoon')] == helen)
wednesday_has_irving = Or(report[('Wednesday', 'morning')] == irving, report[('Wednesday', 'afternoon')] == irving)
solver.add(Implies(nina_tuesday, And(wednesday_has_helen, wednesday_has_irving)))

# If Nina on Wednesday, no constraint (unless clause)

# Now define constraints for each answer choice
# Option A: Mon. morning: Helen; Mon. afternoon: Robert; Tues. morning: Olivia; Tues. afternoon: Irving; Wed. morning: Lenore; Wed. afternoon: Kyle
opt_a_constr = And(
    report[('Monday', 'morning')] == helen,
    report[('Monday', 'afternoon')] == robert,
    report[('Tuesday', 'morning')] == olivia,
    report[('Tuesday', 'afternoon')] == irving,
    report[('Wednesday', 'morning')] == 3,  # Lenore is index 3
    report[('Wednesday', 'afternoon')] == 5  # Kyle is index 5
)

# Option B: Mon. morning: Irving; Mon. afternoon: Olivia; Tues. morning: Helen; Tues. afternoon: Kyle; Wed. morning: Nina; Wed. afternoon: Lenore
opt_b_constr = And(
    report[('Monday', 'morning')] == irving,
    report[('Monday', 'afternoon')] == olivia,
    report[('Tuesday', 'morning')] == helen,
    report[('Tuesday', 'afternoon')] == 5,  # Kyle
    report[('Wednesday', 'morning')] == nina,
    report[('Wednesday', 'afternoon')] == 3  # Lenore
)

# Option C: Mon. morning: Lenore; Mon. afternoon: Helen; Tues. morning: George; Tues. afternoon: Kyle; Wed. morning: Robert; Wed. afternoon: Irving
opt_c_constr = And(
    report[('Monday', 'morning')] == 3,  # Lenore
    report[('Monday', 'afternoon')] == helen,
    report[('Tuesday', 'morning')] == george,
    report[('Tuesday', 'afternoon')] == 5,  # Kyle
    report[('Wednesday', 'morning')] == robert,
    report[('Wednesday', 'afternoon')] == irving
)

# Option D: Mon. morning: Nina; Mon. afternoon: Helen; Tues. morning: Robert; Tues. afternoon: Irving; Wed. morning: Olivia; Wed. afternoon: Lenore
opt_d_constr = And(
    report[('Monday', 'morning')] == nina,
    report[('Monday', 'afternoon')] == helen,
    report[('Tuesday', 'morning')] == robert,
    report[('Tuesday', 'afternoon')] == irving,
    report[('Wednesday', 'morning')] == olivia,
    report[('Wednesday', 'afternoon')] == 3  # Lenore
)

# Option E: Mon. morning: Olivia; Mon. afternoon: Nina; Tues. morning: Irving; Tues. afternoon: Helen; Wed. morning: Kyle; Wed. afternoon: George
opt_e_constr = And(
    report[('Monday', 'morning')] == olivia,
    report[('Monday', 'afternoon')] == nina,
    report[('Tuesday', 'morning')] == irving,
    report[('Tuesday', 'afternoon')] == helen,
    report[('Wednesday', 'morning')] == 5,  # Kyle
    report[('Wednesday', 'afternoon')] == george
)

# Evaluate each option
found_options = []
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