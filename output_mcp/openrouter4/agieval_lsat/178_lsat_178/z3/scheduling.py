from z3 import *

solver = Solver()

# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
# Students: G=0, H=1, J=2, K=3, L=4
G, H, J, K, L = 0, 1, 2, 3, 4

first = [Int(f'first_{d}') for d in range(5)]
second = [Int(f'second_{d}') for d in range(5)]

# Domain: each shift is worked by exactly one student
for d in range(5):
    solver.add(first[d] >= 0, first[d] <= 4)
    solver.add(second[d] >= 0, second[d] <= 4)

# Each student works exactly two shifts
for student in range(5):
    count = Sum([If(first[d] == student, 1, 0) for d in range(5)] + 
                [If(second[d] == student, 1, 0) for d in range(5)])
    solver.add(count == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(first[d] != second[d])

# On two consecutive days, Louise works the second shift
consec_louise_second = Or([And(second[d] == L, second[d+1] == L) for d in range(4)])
solver.add(consec_louise_second)

# On two nonconsecutive days, Grecia works the first shift
g_first_count = Sum([If(first[d] == G, 1, 0) for d in range(5)])
solver.add(g_first_count == 2)

# The two days must be nonconsecutive
nonconsec_g_first = Or([And(first[d1] == G, first[d2] == G, d2 - d1 > 1) for d1 in range(5) for d2 in range(d1+1, 5)])
solver.add(nonconsec_g_first)

# Katya works on Tuesday and Friday
solver.add(Or(first[1] == K, second[1] == K))  # Tuesday
solver.add(Or(first[4] == K, second[4] == K))  # Friday

# Hakeem and Joe work on the same day as each other at least once
h_j_same_day = Or([And(Or(first[d] == H, second[d] == H), Or(first[d] == J, second[d] == J)) for d in range(5)])
solver.add(h_j_same_day)

# Grecia and Louise never work on the same day as each other
for d in range(5):
    solver.add(Not(And(Or(first[d] == G, second[d] == G), Or(first[d] == L, second[d] == L))))

# Conditional premise: there is at least one day on which Grecia and Joe both work
g_j_same_day = Or([And(Or(first[d] == G, second[d] == G), Or(first[d] == J, second[d] == J)) for d in range(5)])
solver.add(g_j_same_day)

# Now check each option
found_options = []

for letter, constr in [
    ("A", first[1] == G),  # Grecia works the first shift on Tuesday
    ("B", second[0] == H),  # Hakeem works the second shift on Monday
    ("C", second[2] == H),  # Hakeem works the second shift on Wednesday
    ("D", first[2] == J),   # Joe works the first shift on Wednesday
    ("E", first[3] == J),   # Joe works the first shift on Thursday
]:
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