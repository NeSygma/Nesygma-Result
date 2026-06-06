from z3 import *

# Five students: Grecia, Hakeem, Joe, Katya, Louise
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Shifts: first=0, second=1

students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
days = [0, 1, 2, 3, 4]
shifts = [0, 1]

# Decision variable: assign[student][day][shift] = Bool
assign = {}
for s in students:
    assign[s] = {}
    for d in days:
        assign[s][d] = {}
        for sh in shifts:
            assign[s][d][sh] = Bool(f"{s}_{d}_{sh}")

solver = Solver()

# Each shift is worked by exactly one student
for d in days:
    for sh in shifts:
        solver.add(Sum([If(assign[s][d][sh], 1, 0) for s in students]) == 1)

# Each student works exactly two shifts total
for s in students:
    solver.add(Sum([If(assign[s][d][sh], 1, 0) for d in days for sh in shifts]) == 2)

# No student works both shifts of any day
for s in students:
    for d in days:
        solver.add(Not(And(assign[s][d][0], assign[s][d][1])))

# On two consecutive days, Louise works the second shift.
# Louise works exactly 2 shifts. So she works second shift on day d and day d+1.
louise_consec = []
for d in range(4):
    louise_consec.append(And(assign["Louise"][d][1], assign["Louise"][d+1][1]))
solver.add(Or(louise_consec))

# On two nonconsecutive days, Grecia works the first shift.
# Grecia works exactly 2 shifts. Both are first shift, on nonconsecutive days.
grecia_pairs = []
for d1 in days:
    for d2 in days:
        if d1 < d2 and abs(d1 - d2) > 1:
            grecia_pairs.append(And(assign["Grecia"][d1][0], assign["Grecia"][d2][0]))
solver.add(Or(grecia_pairs))

# Katya works on Tuesday and Friday.
solver.add(Or(assign["Katya"][1][0], assign["Katya"][1][1]))
solver.add(Or(assign["Katya"][4][0], assign["Katya"][4][1]))
for d in [0, 2, 3]:
    solver.add(Not(Or(assign["Katya"][d][0], assign["Katya"][d][1])))

# Hakeem and Joe work on the same day as each other at least once.
hakeem_joe_same = []
for d in days:
    hakeem_joe_same.append(And(
        Or(assign["Hakeem"][d][0], assign["Hakeem"][d][1]),
        Or(assign["Joe"][d][0], assign["Joe"][d][1])
    ))
solver.add(Or(hakeem_joe_same))

# Grecia and Louise never work on the same day as each other.
for d in days:
    solver.add(Not(And(
        Or(assign["Grecia"][d][0], assign["Grecia"][d][1]),
        Or(assign["Louise"][d][0], assign["Louise"][d][1])
    )))

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    print("Base constraints are SAT")
    m = solver.model()
    # Print a schedule
    for d in days:
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for sh in shifts:
            shift_names = ["first", "second"]
            for s in students:
                if is_true(m[assign[s][d][sh]]):
                    print(f"{day_names[d]} {shift_names[sh]}: {s}")
else:
    print("Base constraints are UNSAT")
    exit()

# Now let's think more carefully about what "must be true" means.
# We need to find which option is entailed by the constraints.
# An option "must be true" if in EVERY valid schedule, that option holds.
# So we check: is there a valid schedule where the option is FALSE?
# If no such schedule exists, the option must be true.

# Reset solver
solver2 = Solver()
# Add all base constraints again
for d in days:
    for sh in shifts:
        solver2.add(Sum([If(assign[s][d][sh], 1, 0) for s in students]) == 1)
for s in students:
    solver2.add(Sum([If(assign[s][d][sh], 1, 0) for d in days for sh in shifts]) == 2)
for s in students:
    for d in days:
        solver2.add(Not(And(assign[s][d][0], assign[s][d][1])))
louise_consec2 = []
for d in range(4):
    louise_consec2.append(And(assign["Louise"][d][1], assign["Louise"][d+1][1]))
solver2.add(Or(louise_consec2))
grecia_pairs2 = []
for d1 in days:
    for d2 in days:
        if d1 < d2 and abs(d1 - d2) > 1:
            grecia_pairs2.append(And(assign["Grecia"][d1][0], assign["Grecia"][d2][0]))
solver2.add(Or(grecia_pairs2))
solver2.add(Or(assign["Katya"][1][0], assign["Katya"][1][1]))
solver2.add(Or(assign["Katya"][4][0], assign["Katya"][4][1]))
for d in [0, 2, 3]:
    solver2.add(Not(Or(assign["Katya"][d][0], assign["Katya"][d][1])))
hakeem_joe_same2 = []
for d in days:
    hakeem_joe_same2.append(And(
        Or(assign["Hakeem"][d][0], assign["Hakeem"][d][1]),
        Or(assign["Joe"][d][0], assign["Joe"][d][1])
    ))
solver2.add(Or(hakeem_joe_same2))
for d in days:
    solver2.add(Not(And(
        Or(assign["Grecia"][d][0], assign["Grecia"][d][1]),
        Or(assign["Louise"][d][0], assign["Louise"][d][1])
    )))

# Now for each option, check if its NEGATION is satisfiable with base constraints.
# If the negation is UNSAT, then the option MUST be true.
print("\nChecking which options must be true...")
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver2.push()
    solver2.add(Not(constr))  # Try to find a counterexample where option is false
    if solver2.check() == unsat:
        must_be_true.append(letter)
    solver2.pop()

print(f"Options that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")