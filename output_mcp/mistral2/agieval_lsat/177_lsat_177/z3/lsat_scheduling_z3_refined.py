from z3 import *

# Base constraints and setup
solver = Solver()

# Days and shifts
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
Shifts = ["First", "Second"]

# Students
Students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Assignments: student assigned to a shift on a day
# assignment[student][day][shift] = Bool
assignment = {s: {d: {sh: Bool(f"{s}_{d}_{sh}") for sh in Shifts} for d in Days} for s in Students}

# Helper: Exactly one student per shift per day
for d in Days:
    for sh in Shifts:
        solver.add(Or([assignment[s][d][sh] for s in Students]),
                   Distinct([assignment[s][d][sh] for s in Students]))

# Each student works exactly two shifts
for s in Students:
    solver.add(Sum([If(assignment[s][d][sh], 1, 0) for d in Days for sh in Shifts]) == 2)

# No student works both shifts of any day
for s in Students:
    for d in Days:
        solver.add(Not(And(assignment[s][d]["First"], assignment[s][d]["Second"])))

# On two consecutive days, Louise works the second shift
consecutive_pairs = [
    ("Monday", "Tuesday"),
    ("Tuesday", "Wednesday"),
    ("Wednesday", "Thursday"),
    ("Thursday", "Friday")
]
for d1, d2 in consecutive_pairs:
    solver.add(Or(
        assignment["Louise"][d1]["Second"],
        assignment["Louise"][d2]["Second"]
    ))

# On two nonconsecutive days, Grecia works the first shift
nonconsecutive_pairs = [
    ("Monday", "Wednesday"),
    ("Monday", "Thursday"),
    ("Monday", "Friday"),
    ("Tuesday", "Thursday"),
    ("Tuesday", "Friday"),
    ("Wednesday", "Friday")
]
for d1, d2 in nonconsecutive_pairs:
    solver.add(Or(
        assignment["Grecia"][d1]["First"],
        assignment["Grecia"][d2]["First"]
    ))

# Katya works on Tuesday and Friday
solver.add(Or([assignment["Katya"][d]["First"] for d in ["Tuesday", "Friday"]]))
solver.add(Or([assignment["Katya"][d]["Second"] for d in ["Tuesday", "Friday"]]))

# Hakeem and Joe work on the same day at least once
same_day = Or([
    And(
        Or(assignment["Hakeem"][d]["First"], assignment["Hakeem"][d]["Second"]),
        Or(assignment["Joe"][d]["First"], assignment["Joe"][d]["Second"])
    ) for d in Days
])
solver.add(same_day)

# Grecia and Louise never work on the same day
for d in Days:
    solver.add(Not(Or(
        And(assignment["Grecia"][d]["First"], assignment["Louise"][d]["First"]),
        And(assignment["Grecia"][d]["First"], assignment["Louise"][d]["Second"]),
        And(assignment["Grecia"][d]["Second"], assignment["Louise"][d]["First"]),
        And(assignment["Grecia"][d]["Second"], assignment["Louise"][d]["Second"])
    )))

# Hakeem works on Wednesday
solver.add(Or(assignment["Hakeem"]["Wednesday"]["First"], assignment["Hakeem"]["Wednesday"]["Second"]))

# Now evaluate the multiple choice options
# We need to check which pair of days Joe must work if Hakeem works on Wednesday

# Define the options as constraints on Joe's assignments
# Option A: Joe works Monday and Wednesday
opt_a_constr = And(
    Or(assignment["Joe"]["Monday"]["First"], assignment["Joe"]["Monday"]["Second"]),
    Or(assignment["Joe"]["Wednesday"]["First"], assignment["Joe"]["Wednesday"]["Second"])
)

# Option B: Joe works Monday and Thursday
opt_b_constr = And(
    Or(assignment["Joe"]["Monday"]["First"], assignment["Joe"]["Monday"]["Second"]),
    Or(assignment["Joe"]["Thursday"]["First"], assignment["Joe"]["Thursday"]["Second"])
)

# Option C: Joe works Tuesday and Wednesday
opt_c_constr = And(
    Or(assignment["Joe"]["Tuesday"]["First"], assignment["Joe"]["Tuesday"]["Second"]),
    Or(assignment["Joe"]["Wednesday"]["First"], assignment["Joe"]["Wednesday"]["Second"])
)

# Option D: Joe works Tuesday and Thursday
opt_d_constr = And(
    Or(assignment["Joe"]["Tuesday"]["First"], assignment["Joe"]["Tuesday"]["Second"]),
    Or(assignment["Joe"]["Thursday"]["First"], assignment["Joe"]["Thursday"]["Second"])
)

# Option E: Joe works Wednesday and Thursday
opt_e_constr = And(
    Or(assignment["Joe"]["Wednesday"]["First"], assignment["Joe"]["Wednesday"]["Second"]),
    Or(assignment["Joe"]["Thursday"]["First"], assignment["Joe"]["Thursday"]["Second"])
)

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