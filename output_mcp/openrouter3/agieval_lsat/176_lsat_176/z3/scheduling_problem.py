from z3 import *

# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise
students = [0, 1, 2, 3, 4]
days = [0, 1, 2, 3, 4]  # Monday to Friday
shifts = [0, 1]  # First and second

# Create solver
solver = Solver()

# work[day][shift] = student working that shift
work = [[Int(f"work_{d}_{s}") for s in shifts] for d in days]

# Domain constraints: each work variable must be one of the students
for d in days:
    for s in shifts:
        solver.add(Or([work[d][s] == student for student in students]))

# Constraint 1: Each shift has exactly one student (already enforced by domain)
# Constraint 2: No student works both shifts of any day
for d in days:
    solver.add(work[d][0] != work[d][1])

# Constraint 3: Each student works exactly 2 shifts total
for student in students:
    total_shifts = Sum([If(work[d][s] == student, 1, 0) for d in days for s in shifts])
    solver.add(total_shifts == 2)

# Constraint 4: Louise works second shift on two consecutive days
# Louise is student 4
louise_second_days = [If(work[d][1] == 4, 1, 0) for d in days]
# At least two consecutive days where Louise works second shift
consecutive_found = False
for i in range(len(days)-1):
    # Check if Louise works second shift on day i and i+1
    solver.add(Or(work[i][1] != 4, work[i+1][1] != 4, 
                  Sum([If(work[d][1] == 4, 1, 0) for d in days]) >= 2))
# Actually, let's be more precise: there must exist at least one pair of consecutive days
# where Louise works second shift on both
has_consecutive = False
for i in range(len(days)-1):
    has_consecutive = Or(has_consecutive, And(work[i][1] == 4, work[i+1][1] == 4))
solver.add(has_consecutive)

# Constraint 5: Grecia works first shift on two nonconsecutive days
# Grecia is student 0
grecia_first_days = [If(work[d][0] == 0, 1, 0) for d in days]
# Exactly two days where Grecia works first shift
solver.add(Sum(grecia_first_days) == 2)
# These two days must not be consecutive
for i in range(len(days)-1):
    # If day i and i+1 are both Grecia first shift, that's invalid
    solver.add(Not(And(work[i][0] == 0, work[i+1][0] == 0)))

# Constraint 6: Katya works on Tuesday and Friday
# Katya is student 3
# She must work at least one shift on Tuesday (day 1) and Friday (day 4)
solver.add(Or(work[1][0] == 3, work[1][1] == 3))  # Tuesday
solver.add(Or(work[4][0] == 3, work[4][1] == 3))  # Friday

# Constraint 7: Hakeem and Joe work on the same day at least once
# Hakeem is student 1, Joe is student 2
same_day = False
for d in days:
    # Check if both work on day d (in any shift)
    hakeem_works = Or(work[d][0] == 1, work[d][1] == 1)
    joe_works = Or(work[d][0] == 2, work[d][1] == 2)
    same_day = Or(same_day, And(hakeem_works, joe_works))
solver.add(same_day)

# Constraint 8: Grecia and Louise never work on the same day
# Grecia is 0, Louise is 4
for d in days:
    grecia_works = Or(work[d][0] == 0, work[d][1] == 0)
    louise_works = Or(work[d][0] == 4, work[d][1] == 4)
    solver.add(Not(And(grecia_works, louise_works)))

# Now test the multiple choice options
# Options:
# (A) Grecia does not work at the gallery on Tuesday.
# (B) Hakeem does not work at the gallery on Wednesday.
# (C) Joe does not work at the gallery on Tuesday.
# (D) Joe does not work at the gallery on Thursday.
# (E) Louise does not work at the gallery on Tuesday.

# Define option constraints
opt_a = Or(work[1][0] != 0, work[1][1] != 0)  # Grecia not on Tuesday
opt_b = Or(work[2][0] != 1, work[2][1] != 1)  # Hakeem not on Wednesday
opt_c = Or(work[1][0] != 2, work[1][1] != 2)  # Joe not on Tuesday
opt_d = Or(work[3][0] != 2, work[3][1] != 2)  # Joe not on Thursday
opt_e = Or(work[1][0] != 4, work[1][1] != 4)  # Louise not on Tuesday

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