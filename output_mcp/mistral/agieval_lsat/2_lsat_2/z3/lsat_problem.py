from z3 import *

# Students
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
student_to_id = {s: i for i, s in enumerate(students)}
id_to_student = {i: s for i, s in enumerate(students)}

# Days
days = ['Monday', 'Tuesday', 'Wednesday']

# Create a solver
solver = Solver()

# Each student is either giving a report or not
student_vars = {s: Bool(s) for s in students}

# Exactly 6 students give reports
solver.add(Sum([student_vars[s] for s in students]) == 6)

# Kyle and Lenore do not give reports (for this question)
solver.add(Not(student_vars['Kyle']))
solver.add(Not(student_vars['Lenore']))

# Assignments: for each day and time slot, which student gives the report (using student IDs)
# morning[d] = student ID giving morning report on day d
# afternoon[d] = student ID giving afternoon report on day d
morning = {d: Int(f'morning_{d}') for d in days}
afternoon = {d: Int(f'afternoon_{d}') for d in days}

# Each slot must be assigned to a student ID (0-7)
for d in days:
    solver.add(morning[d] >= 0, morning[d] < 8)
    solver.add(afternoon[d] >= 0, afternoon[d] < 8)

# Each student who gives a report must be assigned to exactly one slot
# This means: for each student s, if student_vars[s] is True, then s must appear exactly once in the 6 slots
# And if student_vars[s] is False, then s must not appear in any slot

# For each student, they can be assigned to at most one slot
for s in students:
    sid = student_to_id[s]
    # If student gives a report, they must be assigned to exactly one slot
    solver.add(Implies(student_vars[s], Or([morning[d] == sid for d in days] + [afternoon[d] == sid for d in days])))
    # If student doesn't give a report, they must not be assigned to any slot
    solver.add(Implies(Not(student_vars[s]), And([morning[d] != sid for d in days] + [afternoon[d] != sid for d in days])))

# Tuesday is the only day George can give a report
sid_george = student_to_id['George']
solver.add(Implies(student_vars['George'], Or(morning['Tuesday'] == sid_george, afternoon['Tuesday'] == sid_george)))

# Neither Olivia nor Robert can give an afternoon report
sid_olivia = student_to_id['Olivia']
sid_robert = student_to_id['Robert']
for d in days:
    solver.add(Implies(student_vars['Olivia'], afternoon[d] != sid_olivia))
    solver.add(Implies(student_vars['Robert'], afternoon[d] != sid_robert))

# Olivia and Robert must give reports in the morning if they give reports at all
for s, sid in [('Olivia', sid_olivia), ('Robert', sid_robert)]:
    solver.add(Implies(student_vars[s], Or([morning[d] == sid for d in days])))

# Nina's constraint: If Nina gives a report on Monday, then Helen and Irving must both give reports on Tuesday
# If Nina gives a report on Tuesday, then Helen and Irving must both give reports on Wednesday
sid_nina = student_to_id['Nina']
sid_helen = student_to_id['Helen']
sid_irving = student_to_id['Irving']

solver.add(Implies(Or(morning['Monday'] == sid_nina, afternoon['Monday'] == sid_nina),
                   And(Or(morning['Tuesday'] == sid_helen, afternoon['Tuesday'] == sid_helen),
                       Or(morning['Tuesday'] == sid_irving, afternoon['Tuesday'] == sid_irving))))

solver.add(Implies(Or(morning['Tuesday'] == sid_nina, afternoon['Tuesday'] == sid_nina),
                   And(Or(morning['Wednesday'] == sid_helen, afternoon['Wednesday'] == sid_helen),
                       Or(morning['Wednesday'] == sid_irving, afternoon['Wednesday'] == sid_irving))))

# Now I need to check each option for the morning assignments
# The options are:
# A) Monday: Helen, Tuesday: George, Wednesday: Nina
# B) Monday: Irving, Tuesday: Robert, Wednesday: Helen
# C) Monday: Nina, Tuesday: Helen, Wednesday: Olivia
# D) Monday: Olivia, Tuesday: Robert, Wednesday: Irving
# E) Monday: Robert, Tuesday: George, Wednesday: Helen

# For each option, I need to set the morning variables to the corresponding student IDs
options = {
    'A': And(morning['Monday'] == sid_helen, morning['Tuesday'] == sid_george, morning['Wednesday'] == sid_nina),
    'B': And(morning['Monday'] == sid_irving, morning['Tuesday'] == sid_robert, morning['Wednesday'] == sid_helen),
    'C': And(morning['Monday'] == sid_nina, morning['Tuesday'] == sid_helen, morning['Wednesday'] == sid_olivia),
    'D': And(morning['Monday'] == sid_olivia, morning['Tuesday'] == sid_robert, morning['Wednesday'] == sid_irving),
    'E': And(morning['Monday'] == sid_robert, morning['Tuesday'] == sid_george, morning['Wednesday'] == sid_helen)
}

# Now I need to check each option
found_options = []
for letter, constr in options.items():
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