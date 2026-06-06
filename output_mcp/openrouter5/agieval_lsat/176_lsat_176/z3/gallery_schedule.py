from z3 import *

# Five students: Grecia, Hakeem, Joe, Katya, Louise
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Shifts: first=0, second=1

students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
days = [0, 1, 2, 3, 4]  # Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
shifts = [0, 1]  # first=0, second=1

# Decision variable: assign[student][day][shift] = Bool (True if student works that shift)
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
# So there exist two consecutive days d, d+1 such that Louise works second shift on both.
# We need exactly two such days? "On two consecutive days, Louise works the second shift."
# Means: there is a pair of consecutive days where Louise works second shift on both.
# It doesn't say "exactly" two consecutive days, just that it happens.
# But we need to ensure it's at least one pair.
# However, Louise works exactly 2 shifts total. So if she works second shift on two consecutive days,
# that uses both her shifts. So she can't work any other shifts.
# So: Louise works second shift on day d and day d+1 for some d in {0,1,2,3}.
louise_consec = []
for d in range(4):
    louise_consec.append(And(assign["Louise"][d][1], assign["Louise"][d+1][1]))
solver.add(Or(louise_consec))

# On two nonconsecutive days, Grecia works the first shift.
# Grecia works first shift on two days that are NOT consecutive.
# Grecia works exactly 2 shifts total. So both her shifts are first shift, on nonconsecutive days.
# So there exist two days d1, d2 with |d1-d2| > 1 such that Grecia works first shift on both.
# And she doesn't work any other shifts.
grecia_pairs = []
for d1 in days:
    for d2 in days:
        if d1 < d2 and abs(d1 - d2) > 1:
            grecia_pairs.append(And(assign["Grecia"][d1][0], assign["Grecia"][d2][0]))
solver.add(Or(grecia_pairs))

# Katya works on Tuesday and Friday.
# Katya works exactly 2 shifts. So she works one shift on Tuesday and one on Friday.
solver.add(Or(assign["Katya"][1][0], assign["Katya"][1][1]))  # works Tuesday
solver.add(Or(assign["Katya"][4][0], assign["Katya"][4][1]))  # works Friday
# Katya doesn't work on other days
for d in [0, 2, 3]:
    solver.add(Not(Or(assign["Katya"][d][0], assign["Katya"][d][1])))

# Hakeem and Joe work on the same day as each other at least once.
# There exists a day d where both Hakeem and Joe work (any shift).
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

# Now evaluate each option
# (A) Grecia does not work at the gallery on Tuesday.
opt_a = Not(Or(assign["Grecia"][1][0], assign["Grecia"][1][1]))

# (B) Hakeem does not work at the gallery on Wednesday.
opt_b = Not(Or(assign["Hakeem"][2][0], assign["Hakeem"][2][1]))

# (C) Joe does not work at the gallery on Tuesday.
opt_c = Not(Or(assign["Joe"][1][0], assign["Joe"][1][1]))

# (D) Joe does not work at the gallery on Thursday.
opt_d = Not(Or(assign["Joe"][3][0], assign["Joe"][3][1]))

# (E) Louise does not work at the gallery on Tuesday.
opt_e = Not(Or(assign["Louise"][1][0], assign["Louise"][1][1]))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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