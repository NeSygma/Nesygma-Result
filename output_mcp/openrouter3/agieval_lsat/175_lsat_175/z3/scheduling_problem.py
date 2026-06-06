from z3 import *

# Student IDs
G, H, J, K, L = 0, 1, 2, 3, 4
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=first, 1=second

# For each day and shift, which student works?
# We'll use a 2D array of integers (student IDs)
shift_student = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Domain constraints: each shift_student[d][s] must be one of the student IDs
for d in range(5):
    for s in range(2):
        solver.add(Or([shift_student[d][s] == sid for sid in [G, H, J, K, L]]))

# Constraint 1: Each student works exactly 2 shifts total
for sid in [G, H, J, K, L]:
    solver.add(Sum([If(shift_student[d][s] == sid, 1, 0) for d in range(5) for s in range(2)]) == 2)

# Constraint 2: No student works both shifts of any day
for d in range(5):
    solver.add(shift_student[d][0] != shift_student[d][1])

# Constraint 3: On two consecutive days, Louise works the second shift
# There exists some day d (0-3) where Louise works second shift on days d and d+1
consecutive_louise = Or([And(shift_student[d][1] == L, shift_student[d+1][1] == L) for d in range(4)])
solver.add(consecutive_louise)

# Constraint 4: On two nonconsecutive days, Grecia works the first shift
# There exist days d1, d2 where |d1-d2| > 1 and Grecia works first shift on both
nonconsecutive_grecia = Or([And(shift_student[d1][0] == G, shift_student[d2][0] == G, d1 != d2, Abs(d1 - d2) > 1) for d1 in range(5) for d2 in range(5)])
solver.add(nonconsecutive_grecia)

# Constraint 5: Katya works on Tuesday and Friday
# On day 1 (Tue) and day 4 (Fri), Katya works at least one shift
solver.add(Or(shift_student[1][0] == K, shift_student[1][1] == K))
solver.add(Or(shift_student[4][0] == K, shift_student[4][1] == K))

# Constraint 6: Hakeem and Joe work on the same day as each other at least once
# There exists a day where both work some shift
same_day_hj = Or([Or(And(shift_student[d][0] == H, shift_student[d][1] == J),
                     And(shift_student[d][0] == J, shift_student[d][1] == H),
                     And(shift_student[d][0] == H, shift_student[d][0] == J),  # both first shift? impossible due to constraint 2
                     And(shift_student[d][1] == H, shift_student[d][1] == J))  # both second shift? impossible due to constraint 2
                  for d in range(5)])
# Actually, since no student works both shifts of a day, they must work different shifts on the same day
same_day_hj = Or([Or(And(shift_student[d][0] == H, shift_student[d][1] == J),
                     And(shift_student[d][0] == J, shift_student[d][1] == H))
                  for d in range(5)])
solver.add(same_day_hj)

# Constraint 7: Grecia and Louise never work on the same day as each other
for d in range(5):
    solver.add(Not(Or(shift_student[d][0] == G, shift_student[d][1] == G) & Or(shift_student[d][0] == L, shift_student[d][1] == L)))

# Now test each option
# Option A: Hakeem, Louise, Louise, Hakeem, Katya (second shifts Monday-Friday)
opt_a_second = [H, L, L, H, K]

# Option B: Joe, Hakeem, Grecia, Louise, Louise
opt_b_second = [J, H, G, L, L]

# Option C: Joe, Katya, Hakeem, Louise, Katya
opt_c_second = [J, K, H, L, K]

# Option D: Louise, Katya, Joe, Louise, Katya
opt_d_second = [L, K, J, L, K]

# Option E: Louise, Louise, Hakeem, Joe, Joe
opt_e_second = [L, L, H, J, J]

found_options = []

# Test Option A
solver.push()
for d in range(5):
    solver.add(shift_student[d][1] == opt_a_second[d])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test Option B
solver.push()
for d in range(5):
    solver.add(shift_student[d][1] == opt_b_second[d])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test Option C
solver.push()
for d in range(5):
    solver.add(shift_student[d][1] == opt_c_second[d])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test Option D
solver.push()
for d in range(5):
    solver.add(shift_student[d][1] == opt_d_second[d])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test Option E
solver.push()
for d in range(5):
    solver.add(shift_student[d][1] == opt_e_second[d])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")