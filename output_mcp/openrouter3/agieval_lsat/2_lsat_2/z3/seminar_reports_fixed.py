from z3 import *

# Students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_to_idx = {s: i for i, s in enumerate(students)}
N = len(students)

# Days and times
days = ["Monday", "Tuesday", "Wednesday"]
times = ["morning", "afternoon"]

# Create variables: report[student][day][time] = Bool (True if student gives report at that slot)
report = {}
for s in students:
    report[s] = {}
    for d in days:
        report[s][d] = {}
        for t in times:
            report[s][d][t] = Bool(f"report_{s}_{d}_{t}")

solver = Solver()

# Constraint 1: Exactly 6 students give reports (so exactly 2 don't)
# Count total reports across all slots
total_reports = Sum([If(report[s][d][t], 1, 0) for s in students for d in days for t in times])
solver.add(total_reports == 6 * 2)  # 6 students * 2 slots each = 12 reports total

# Constraint 2: Each day has exactly 2 reports (1 morning, 1 afternoon)
for d in days:
    morning_reports = Sum([If(report[s][d]["morning"], 1, 0) for s in students])
    afternoon_reports = Sum([If(report[s][d]["afternoon"], 1, 0) for s in students])
    solver.add(morning_reports == 1)
    solver.add(afternoon_reports == 1)

# Constraint 3: Each student gives at most 1 report total
for s in students:
    student_reports = Sum([If(report[s][d][t], 1, 0) for d in days for t in times])
    solver.add(student_reports <= 1)

# Constraint 4: Tuesday is the only day George can give a report
# George can only give report on Tuesday (morning or afternoon)
for d in days:
    for t in times:
        if d != "Tuesday":
            solver.add(Not(report["George"][d][t]))

# Constraint 5: Neither Olivia nor Robert can give afternoon reports
for d in days:
    solver.add(Not(report["Olivia"][d]["afternoon"]))
    solver.add(Not(report["Robert"][d]["afternoon"]))

# Constraint 6: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
# We need to model "next day" - for Monday Nina -> Tuesday Helen+Irving, for Tuesday Nina -> Wednesday Helen+Irving
# For Wednesday Nina, no constraint (unless Nina's report is on Wednesday, then no constraint)

# For Monday Nina -> Tuesday Helen and Irving both give reports (any time)
solver.add(Implies(Or(report["Nina"]["Monday"]["morning"], report["Nina"]["Monday"]["afternoon"]),
                   And(Sum([If(report["Helen"]["Tuesday"][t], 1, 0) for t in times]) == 1,
                       Sum([If(report["Irving"]["Tuesday"][t], 1, 0) for t in times]) == 1)))

# For Tuesday Nina -> Wednesday Helen and Irving both give reports (any time)
solver.add(Implies(Or(report["Nina"]["Tuesday"]["morning"], report["Nina"]["Tuesday"]["afternoon"]),
                   And(Sum([If(report["Helen"]["Wednesday"][t], 1, 0) for t in times]) == 1,
                       Sum([If(report["Irving"]["Wednesday"][t], 1, 0) for t in times]) == 1)))

# Wednesday Nina: no constraint (as per "unless Nina's report is given on Wednesday")

# Constraint 7: Kyle and Lenore do not give reports
for d in days:
    for t in times:
        solver.add(Not(report["Kyle"][d][t]))
        solver.add(Not(report["Lenore"][d][t]))

# Now, we need to evaluate the multiple choice options
# The question asks: "If Kyle and Lenore do not give reports, then the morning reports on Monday, Tuesday, and Wednesday, respectively, could be given by..."
# So we need to check which option is possible for morning reports on Mon, Tue, Wed

# Define options as constraints on morning reports
opt_a_constr = And(report["Helen"]["Monday"]["morning"],
                   report["George"]["Tuesday"]["morning"],
                   report["Nina"]["Wednesday"]["morning"])

opt_b_constr = And(report["Irving"]["Monday"]["morning"],
                   report["Robert"]["Tuesday"]["morning"],
                   report["Helen"]["Wednesday"]["morning"])

opt_c_constr = And(report["Nina"]["Monday"]["morning"],
                   report["Helen"]["Tuesday"]["morning"],
                   report["Olivia"]["Wednesday"]["morning"])

opt_d_constr = And(report["Olivia"]["Monday"]["morning"],
                   report["Robert"]["Tuesday"]["morning"],
                   report["Irving"]["Wednesday"]["morning"])

opt_e_constr = And(report["Robert"]["Monday"]["morning"],
                   report["George"]["Tuesday"]["morning"],
                   report["Helen"]["Wednesday"]["morning"])

# Test each option
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