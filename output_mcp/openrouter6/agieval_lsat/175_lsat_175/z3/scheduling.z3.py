from z3 import *

# Student mapping
Grecia = 0
Hakeem = 1
Joe = 2
Katya = 3
Louise = 4

# Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
days = 5

# Variables for first and second shifts
first_shift = [Int(f'first_{d}') for d in range(days)]
second_shift = [Int(f'second_{d}') for d in range(days)]

solver = Solver()

# Base constraints

# 1. Each shift is a student (0..4)
for d in range(days):
    solver.add(first_shift[d] >= 0, first_shift[d] <= 4)
    solver.add(second_shift[d] >= 0, second_shift[d] <= 4)
    # No student works both shifts of any day
    solver.add(first_shift[d] != second_shift[d])

# 2. Each student works exactly two shifts total
for s in range(5):
    total_shifts = Sum([If(first_shift[d] == s, 1, 0) + If(second_shift[d] == s, 1, 0) for d in range(days)])
    solver.add(total_shifts == 2)

# 3. Louise works the second shift on two consecutive days
# There exists d in 0..3 such that second_shift[d] == Louise and second_shift[d+1] == Louise
consecutive_louise = Or([And(second_shift[d] == Louise, second_shift[d+1] == Louise) for d in range(4)])
solver.add(consecutive_louise)

# 4. Grecia works the first shift on two nonconsecutive days
# Count days where first_shift == Grecia
grecia_first_days = Sum([If(first_shift[d] == Grecia, 1, 0) for d in range(days)])
solver.add(grecia_first_days >= 2)
# No two consecutive days both have Grecia first shift
for d in range(4):
    solver.add(Not(And(first_shift[d] == Grecia, first_shift[d+1] == Grecia)))

# 5. Katya works on Tuesday and Friday (days 1 and 4)
# Exactly one shift each day
solver.add( (first_shift[1] == Katya) != (second_shift[1] == Katya) )
solver.add( (first_shift[4] == Katya) != (second_shift[4] == Katya) )

# 6. Hakeem and Joe work on the same day at least once
same_day_hj = Or([Or(And(first_shift[d] == Hakeem, second_shift[d] == Joe),
                     And(first_shift[d] == Joe, second_shift[d] == Hakeem)) for d in range(days)])
solver.add(same_day_hj)

# 7. Grecia and Louise never work on the same day
for d in range(days):
    solver.add(Not(Or(And(first_shift[d] == Grecia, second_shift[d] == Louise),
                      And(first_shift[d] == Louise, second_shift[d] == Grecia))))

# Now test each option
options = [
    ("A", [Hakeem, Louise, Louise, Hakeem, Katya]),
    ("B", [Joe, Hakeem, Grecia, Louise, Louise]),
    ("C", [Joe, Katya, Hakeem, Louise, Katya]),
    ("D", [Louise, Katya, Joe, Louise, Katya]),
    ("E", [Louise, Louise, Hakeem, Joe, Joe])
]

found_options = []
for letter, second_list in options:
    solver.push()
    # Add constraints for second shifts
    for d in range(days):
        solver.add(second_shift[d] == second_list[d])
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