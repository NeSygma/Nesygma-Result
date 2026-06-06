from z3 import *

# Student constants
Grecia, Hakeem, Joe, Katya, Louise = 0, 1, 2, 3, 4

# Base constraints solver
solver = Solver()

# Decision variables: first_shift[i] and second_shift[i] for each day i (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri)
first_shift = [Int(f'first_shift_{i}') for i in range(5)]
second_shift = [Int(f'second_shift_{i}') for i in range(5)]

# Each shift is assigned to one of the five students
for i in range(5):
    solver.add(first_shift[i] >= Grecia, first_shift[i] <= Louise)
    solver.add(second_shift[i] >= Grecia, second_shift[i] <= Louise)

# No student works both shifts of any day
for i in range(5):
    solver.add(first_shift[i] != second_shift[i])

# Each student works exactly 2 shifts total
for s in [Grecia, Hakeem, Joe, Katya, Louise]:
    total_shifts = Sum([If(first_shift[i] == s, 1, 0) + If(second_shift[i] == s, 1, 0) for i in range(5)])
    solver.add(total_shifts == 2)

# On two consecutive days, Louise works the second shift
consecutive_louise = Sum([If(And(second_shift[i] == Louise, second_shift[i+1] == Louise), 1, 0) for i in range(4)])
solver.add(consecutive_louise == 2)

# Grecia works first shift on exactly two non-consecutive days
grecia_first_days = [If(first_shift[i] == Grecia, 1, 0) for i in range(5)]
solver.add(Sum(grecia_first_days) == 2)

# Ensure the two days Grecia works first shift are non-consecutive
# If Grecia works first shift on day i and day j (i < j), then j >= i+2
for i in range(5):
    for j in range(i+1, 5):
        solver.add(Implies(And(first_shift[i] == Grecia, first_shift[j] == Grecia), j >= i + 2))

# Katya works on Tuesday (day 1) and Friday (day 4)
solver.add(Or(first_shift[1] == Katya, second_shift[1] == Katya))
solver.add(Or(first_shift[4] == Katya, second_shift[4] == Katya))

# Hakeem and Joe work on the same day at least once
same_day_hj = Or([
    And(
        Or(first_shift[i] == Hakeem, second_shift[i] == Hakeem),
        Or(first_shift[i] == Joe, second_shift[i] == Joe)
    )
    for i in range(5)
])
solver.add(same_day_hj)

# Grecia and Louise never work on the same day
for i in range(5):
    solver.add(Not(And(
        Or(first_shift[i] == Grecia, second_shift[i] == Grecia),
        Or(first_shift[i] == Louise, second_shift[i] == Louise)
    )))

# Now test each multiple-choice option for the second shifts
# Options are lists of students for second shifts Monday through Friday
options = {
    "A": [Hakeem, Louise, Louise, Hakeem, Katya],
    "B": [Joe, Hakeem, Grecia, Louise, Louise],
    "C": [Joe, Katya, Hakeem, Louise, Katya],
    "D": [Louise, Katya, Joe, Louise, Katya],
    "E": [Louise, Louise, Hakeem, Joe, Joe]
}

found_options = []

for letter, second_shift_option in options.items():
    solver.push()
    
    # Set the second_shift values according to the option
    for i in range(5):
        solver.add(second_shift[i] == second_shift_option[i])
    
    # Check if the constraints are satisfiable with this option
    result = solver.check()
    
    if result == sat:
        found_options.append(letter)
    
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")