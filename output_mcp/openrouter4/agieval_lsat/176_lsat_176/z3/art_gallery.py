from z3 import *

solver = Solver()

# Students: G=0, H=1, J=2, K=3, L=4
G, H, J, K, L = 0, 1, 2, 3, 4
num_students = 5

# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
num_days = 5
# Shifts: first=0, second=1
num_shifts = 2

# assign[day][shift] = student (Int 0..4)
assign = [[Int(f'assign_{d}_{s}') for s in range(num_shifts)] for d in range(num_days)]

# Domain constraints
for d in range(num_days):
    for s in range(num_shifts):
        solver.add(And(assign[d][s] >= 0, assign[d][s] <= 4))

# Each shift is worked by exactly one student (implicit from variable structure)

# Each student works exactly two shifts total
student_shift_counts = [0] * num_students
for student in range(num_students):
    solver.add(Sum([If(assign[d][s] == student, 1, 0) for d in range(num_days) for s in range(num_shifts)]) == 2)

# No student works both shifts of any day
for d in range(num_days):
    solver.add(assign[d][0] != assign[d][1])

# On two consecutive days, Louise works the second shift
# There exist d such that assign[d][1] == L and assign[d+1][1] == L
consec_louise_second = False
for d in range(num_days - 1):
    consec_louise_second = Or(consec_louise_second, And(assign[d][1] == L, assign[d+1][1] == L))
solver.add(consec_louise_second)

# On two nonconsecutive days, Grecia works the first shift
# There exist d1, d2 with |d1-d2| > 1 such that assign[d1][0] == G and assign[d2][0] == G
nonconsec_grecia_first = False
for d1 in range(num_days):
    for d2 in range(num_days):
        if abs(d1 - d2) > 1:
            nonconsec_grecia_first = Or(nonconsec_grecia_first, And(assign[d1][0] == G, assign[d2][0] == G))
solver.add(nonconsec_grecia_first)

# Katya works on Tuesday and Friday (at least one shift each)
# Tuesday = day 1, Friday = day 4
solver.add(Or(assign[1][0] == K, assign[1][1] == K))
solver.add(Or(assign[4][0] == K, assign[4][1] == K))

# Hakeem and Joe work on the same day as each other at least once
h_j_same_day = False
for d in range(num_days):
    h_works = Or(assign[d][0] == H, assign[d][1] == H)
    j_works = Or(assign[d][0] == J, assign[d][1] == J)
    h_j_same_day = Or(h_j_same_day, And(h_works, j_works))
solver.add(h_j_same_day)

# Grecia and Louise never work on the same day as each other
for d in range(num_days):
    g_works = Or(assign[d][0] == G, assign[d][1] == G)
    l_works = Or(assign[d][0] == L, assign[d][1] == L)
    solver.add(Not(And(g_works, l_works)))

# Function to check if a student works on a given day
def works_on(student, day):
    return Or(assign[day][0] == student, assign[day][1] == student)

# Now we test each answer choice
# The question asks "which must be true?"
# For each option, we test if its NEGATION is consistent with the premises.
# If the negation is UNSAT, the option must be true.

options = {
    "A": Not(works_on(G, 1)),   # Grecia does not work on Tuesday
    "B": Not(works_on(H, 2)),   # Hakeem does not work on Wednesday
    "C": Not(works_on(J, 1)),   # Joe does not work on Tuesday
    "D": Not(works_on(J, 3)),   # Joe does not work on Thursday
    "E": Not(works_on(L, 1))    # Louise does not work on Tuesday
}

must_be_true = []
for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    # Add the NEGATION of the option (to see if it's possible that the option is false)
    solver.add(Not(options[letter]))
    if solver.check() == unsat:
        # The negation is impossible -> option must be true
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")