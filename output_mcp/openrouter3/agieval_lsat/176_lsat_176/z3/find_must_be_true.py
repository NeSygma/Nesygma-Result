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

# Constraint: No student works both shifts of any day
for d in days:
    solver.add(work[d][0] != work[d][1])

# Constraint: Each student works exactly 2 shifts total
for student in students:
    total_shifts = Sum([If(work[d][s] == student, 1, 0) for d in days for s in shifts])
    solver.add(total_shifts == 2)

# Constraint: Louise works second shift on two consecutive days
# Louise is student 4
# There must be at least one pair of consecutive days where Louise works second shift
has_consecutive = False
for i in range(len(days)-1):
    has_consecutive = Or(has_consecutive, And(work[i][1] == 4, work[i+1][1] == 4))
solver.add(has_consecutive)

# Constraint: Grecia works first shift on two nonconsecutive days
# Grecia is student 0
grecia_first_days = [If(work[d][0] == 0, 1, 0) for d in days]
# Exactly two days where Grecia works first shift
solver.add(Sum(grecia_first_days) == 2)
# These two days must not be consecutive
for i in range(len(days)-1):
    # If day i and i+1 are both Grecia first shift, that's invalid
    solver.add(Not(And(work[i][0] == 0, work[i+1][0] == 0)))

# Constraint: Katya works on Tuesday and Friday
# Katya is student 3
# She must work at least one shift on Tuesday (day 1) and Friday (day 4)
solver.add(Or(work[1][0] == 3, work[1][1] == 3))  # Tuesday
solver.add(Or(work[4][0] == 3, work[4][1] == 3))  # Friday

# Constraint: Hakeem and Joe work on the same day at least once
# Hakeem is student 1, Joe is student 2
same_day = False
for d in days:
    # Check if both work on day d (in any shift)
    hakeem_works = Or(work[d][0] == 1, work[d][1] == 1)
    joe_works = Or(work[d][0] == 2, work[d][1] == 2)
    same_day = Or(same_day, And(hakeem_works, joe_works))
solver.add(same_day)

# Constraint: Grecia and Louise never work on the same day
# Grecia is 0, Louise is 4
for d in days:
    grecia_works = Or(work[d][0] == 0, work[d][1] == 0)
    louise_works = Or(work[d][0] == 4, work[d][1] == 4)
    solver.add(Not(And(grecia_works, louise_works)))

# Now test each option by checking if its NEGATION is satisfiable
# If negation is satisfiable, the option is NOT necessarily true
# If negation is unsatisfiable, the option MUST be true

options = [
    ("A", "Grecia does not work at gallery on Tuesday", 
     Or(work[1][0] != 0, work[1][1] != 0)),  # Grecia (0) doesn't work on Tuesday (day 1)
    ("B", "Hakeem does not work at gallery on Wednesday",
     Or(work[2][0] != 1, work[2][1] != 1)),  # Hakeem (1) doesn't work on Wednesday (day 2)
    ("C", "Joe does not work at gallery on Tuesday",
     Or(work[1][0] != 2, work[1][1] != 2)),  # Joe (2) doesn't work on Tuesday (day 1)
    ("D", "Joe does not work at gallery on Thursday",
     Or(work[3][0] != 2, work[3][1] != 2)),  # Joe (2) doesn't work on Thursday (day 3)
    ("E", "Louise does not work at gallery on Tuesday",
     Or(work[1][0] != 4, work[1][1] != 4)),  # Louise (4) doesn't work on Tuesday (day 1)
]

must_be_true_options = []

for letter, description, option_constraint in options:
    # Create a new solver for this test
    test_solver = Solver()
    
    # Add all base constraints
    for d in days:
        for s in shifts:
            test_solver.add(Or([work[d][s] == student for student in students]))
    
    for d in days:
        test_solver.add(work[d][0] != work[d][1])
    
    for student in students:
        total_shifts = Sum([If(work[d][s] == student, 1, 0) for d in days for s in shifts])
        test_solver.add(total_shifts == 2)
    
    has_consecutive = False
    for i in range(len(days)-1):
        has_consecutive = Or(has_consecutive, And(work[i][1] == 4, work[i+1][1] == 4))
    test_solver.add(has_consecutive)
    
    grecia_first_days = [If(work[d][0] == 0, 1, 0) for d in days]
    test_solver.add(Sum(grecia_first_days) == 2)
    for i in range(len(days)-1):
        test_solver.add(Not(And(work[i][0] == 0, work[i+1][0] == 0)))
    
    test_solver.add(Or(work[1][0] == 3, work[1][1] == 3))  # Tuesday
    test_solver.add(Or(work[4][0] == 3, work[4][1] == 3))  # Friday
    
    same_day = False
    for d in days:
        hakeem_works = Or(work[d][0] == 1, work[d][1] == 1)
        joe_works = Or(work[d][0] == 2, work[d][1] == 2)
        same_day = Or(same_day, And(hakeem_works, joe_works))
    test_solver.add(same_day)
    
    for d in days:
        grecia_works = Or(work[d][0] == 0, work[d][1] == 0)
        louise_works = Or(work[d][0] == 4, work[d][1] == 4)
        test_solver.add(Not(And(grecia_works, louise_works)))
    
    # Add the NEGATION of the option
    test_solver.add(Not(option_constraint))
    
    # Check if negation is satisfiable
    result = test_solver.check()
    
    if result == unsat:
        # Negation is unsatisfiable, so the option MUST be true
        must_be_true_options.append(letter)
        print(f"Option {letter} ({description}): MUST BE TRUE (negation unsatisfiable)")
    elif result == sat:
        # Negation is satisfiable, so the option is NOT necessarily true
        print(f"Option {letter} ({description}): NOT necessarily true (negation satisfiable)")
    else:
        print(f"Option {letter} ({description}): UNKNOWN")

print()
print(f"Options that must be true: {must_be_true_options}")

if len(must_be_true_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true_options[0]}")
elif len(must_be_true_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")