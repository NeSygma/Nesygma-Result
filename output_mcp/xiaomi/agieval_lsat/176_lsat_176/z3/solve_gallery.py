from z3 import *

solver = Solver()

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=first, 1=second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# schedule[d][s] = student working day d, shift s
schedule = [[Int(f'schedule_{d}_{s}') for s in range(2)] for d in range(5)]

# Each shift is worked by exactly one student (0-4)
for d in range(5):
    for s in range(2):
        solver.add(schedule[d][s] >= 0, schedule[d][s] <= 4)

# No student works both shifts of any day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# Each student works exactly 2 shifts
for student in range(5):
    solver.add(Sum([If(schedule[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# Louise (4) works second shift on two consecutive days
# Find two consecutive days where Louise works second shift
louise_consec = []
for d in range(4):
    louise_consec.append(And(schedule[d][1] == 4, schedule[d+1][1] == 4))
solver.add(Or(louise_consec))

# Grecia (0) works first shift on two nonconsecutive days
grecia_first_days = [Bool(f'grecia_first_{d}') for d in range(5)]
for d in range(5):
    solver.add(grecia_first_days[d] == (schedule[d][0] == 0))

# Exactly 2 days Grecia works first shift
solver.add(Sum([If(grecia_first_days[d], 1, 0) for d in range(5)]) == 2)

# Those 2 days must be nonconsecutive
for d in range(4):
    solver.add(Not(And(grecia_first_days[d], grecia_first_days[d+1])))

# Katya (3) works on Tuesday (1) and Friday (4)
# Katya works at least one shift on Tuesday and at least one shift on Friday
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Hakeem (1) and Joe (2) work on the same day at least once
hj_same_day = []
for d in range(5):
    # Both work on day d (each at least one shift)
    hakeem_d = Or(schedule[d][0] == 1, schedule[d][1] == 1)
    joe_d = Or(schedule[d][0] == 2, schedule[d][1] == 2)
    hj_same_day.append(And(hakeem_d, joe_d))
solver.add(Or(hj_same_day))

# Grecia (0) and Louise (4) never work on the same day
for d in range(5):
    grecia_d = Or(schedule[d][0] == 0, schedule[d][1] == 0)
    louise_d = Or(schedule[d][0] == 4, schedule[d][1] == 4)
    solver.add(Not(And(grecia_d, louise_d)))

# Now check which options MUST be true
# We check each option by trying to find a model where it's FALSE
# If we can't find such a model (unsat), it MUST be true

# Option A: Grecia does not work on Tuesday
# Negation: Grecia works on Tuesday (either shift)
opt_a_neg = Or(schedule[1][0] == 0, schedule[1][1] == 0)

# Option B: Hakeem does not work on Wednesday
# Negation: Hakeem works on Wednesday
opt_b_neg = Or(schedule[2][0] == 1, schedule[2][1] == 1)

# Option C: Joe does not work on Tuesday
# Negation: Joe works on Tuesday
opt_c_neg = Or(schedule[1][0] == 2, schedule[1][1] == 2)

# Option D: Joe does not work on Thursday
# Negation: Joe works on Thursday
opt_d_neg = Or(schedule[3][0] == 2, schedule[3][1] == 2)

# Option E: Louise does not work on Tuesday
# Negation: Louise works on Tuesday
opt_e_neg = Or(schedule[1][0] == 4, schedule[1][1] == 4)

options = [
    ("A", opt_a_neg, "Grecia does not work on Tuesday"),
    ("B", opt_b_neg, "Hakeem does not work on Wednesday"),
    ("C", opt_c_neg, "Joe does not work on Tuesday"),
    ("D", opt_d_neg, "Joe does not work on Thursday"),
    ("E", opt_e_neg, "Louise does not work on Tuesday"),
]

must_be_true = []
for letter, neg_constr, desc in options:
    s = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s.add(c)
    # Try to find a model where the option is FALSE
    s.add(neg_constr)
    result = s.check()
    if result == unsat:
        # Cannot make it false, so it MUST be true
        must_be_true.append(letter)
        print(f"Option {letter} ({desc}): MUST BE TRUE (negation is unsat)")
    elif result == sat:
        print(f"Option {letter} ({desc}): NOT necessarily true (found counterexample)")
    else:
        print(f"Option {letter} ({desc}): UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")