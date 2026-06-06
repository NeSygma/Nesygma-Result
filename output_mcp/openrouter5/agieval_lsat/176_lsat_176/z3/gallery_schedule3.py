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

def add_base_constraints(s):
    # Each shift is worked by exactly one student
    for d in days:
        for sh in shifts:
            s.add(Sum([If(assign[st][d][sh], 1, 0) for st in students]) == 1)

    # Each student works exactly two shifts total
    for st in students:
        s.add(Sum([If(assign[st][d][sh], 1, 0) for d in days for sh in shifts]) == 2)

    # No student works both shifts of any day
    for st in students:
        for d in days:
            s.add(Not(And(assign[st][d][0], assign[st][d][1])))

    # On two consecutive days, Louise works the second shift.
    louise_consec = []
    for d in range(4):
        louise_consec.append(And(assign["Louise"][d][1], assign["Louise"][d+1][1]))
    s.add(Or(louise_consec))

    # On two nonconsecutive days, Grecia works the first shift.
    grecia_pairs = []
    for d1 in days:
        for d2 in days:
            if d1 < d2 and abs(d1 - d2) > 1:
                grecia_pairs.append(And(assign["Grecia"][d1][0], assign["Grecia"][d2][0]))
    s.add(Or(grecia_pairs))

    # Katya works on Tuesday and Friday.
    s.add(Or(assign["Katya"][1][0], assign["Katya"][1][1]))
    s.add(Or(assign["Katya"][4][0], assign["Katya"][4][1]))
    for d in [0, 2, 3]:
        s.add(Not(Or(assign["Katya"][d][0], assign["Katya"][d][1])))

    # Hakeem and Joe work on the same day as each other at least once.
    hakeem_joe_same = []
    for d in days:
        hakeem_joe_same.append(And(
            Or(assign["Hakeem"][d][0], assign["Hakeem"][d][1]),
            Or(assign["Joe"][d][0], assign["Joe"][d][1])
        ))
    s.add(Or(hakeem_joe_same))

    # Grecia and Louise never work on the same day as each other.
    for d in days:
        s.add(Not(And(
            Or(assign["Grecia"][d][0], assign["Grecia"][d][1]),
            Or(assign["Louise"][d][0], assign["Louise"][d][1])
        )))

# Define the options
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

# For each option, check if its NEGATION is satisfiable with base constraints.
# If the negation is UNSAT, then the option MUST be true.
print("Checking which options must be true...")
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    add_base_constraints(s)
    s.add(Not(constr))  # Try to find a counterexample where option is false
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is UNSAT)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (negation is SAT)")
    else:
        print(f"Option {letter}: UNKNOWN")

print(f"\nOptions that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")