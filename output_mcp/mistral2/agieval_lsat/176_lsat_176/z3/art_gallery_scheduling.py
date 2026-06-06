from z3 import *

# Define days and shifts
days = ['M', 'T', 'W', 'Th', 'F']
shifts = [1, 2]

# Define students
students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']

# Create a solver
solver = Solver()

# Create a symbolic assignment: assignment[day][shift] = student
assignment = [[String(f'assignment_{d}_{s}') for s in shifts] for d in days]

# Helper function to get the student assigned to a shift
def get_assignment(day, shift):
    d_idx = days.index(day)
    s_idx = shifts.index(shift)
    return assignment[d_idx][s_idx]

# Constraint: Each student works exactly 2 shifts
for student in students:
    solver.add(Sum([If(get_assignment(day, shift) == student, 1, 0)
                    for day in days for shift in shifts]) == 2)

# Constraint: No student works both shifts of the same day
for day in days:
    solver.add(get_assignment(day, 1) != get_assignment(day, 2))

# Constraint: Louise works the second shift on two consecutive days
consecutive_pairs = [('M', 'T'), ('T', 'W'), ('W', 'Th'), ('Th', 'F')]
for d1, d2 in consecutive_pairs:
    solver.add(Or(And(get_assignment(d1, 2) == 'Louise', get_assignment(d2, 2) == 'Louise'),
                  And(get_assignment(d1, 2) != 'Louise', get_assignment(d2, 2) != 'Louise')))

# Constraint: Grecia works the first shift on two non-consecutive days
for i in range(len(days)):
    for j in range(i+2, len(days)):  # Ensure non-consecutive
        solver.add(Or(And(get_assignment(days[i], 1) == 'Grecia', get_assignment(days[j], 1) == 'Grecia'),
                      Or(get_assignment(days[i], 1) != 'Grecia', get_assignment(days[j], 1) != 'Grecia)))

# Constraint: Katya works on Tuesday and Friday
solver.add(Or([get_assignment('T', s) == 'Katya' for s in shifts]))
solver.add(Or([get_assignment('F', s) == 'Katya' for s in shifts]))

# Constraint: Hakeem and Joe work on the same day at least once
for day in days:
    solver.add(Or(And(Or([get_assignment(day, s) == 'Hakeem' for s in shifts]),
                      Or([get_assignment(day, s) == 'Joe' for s in shifts])),
                  And(Or([get_assignment(day, s) == 'Joe' for s in shifts]),
                      Or([get_assignment(day, s) == 'Hakeem' for s in shifts]))))

# Constraint: Grecia and Louise never work on the same day
for day in days:
    solver.add(Or(And([get_assignment(day, s) != 'Grecia' for s in shifts]),
                  And([get_assignment(day, s) != 'Louise' for s in shifts])))

# Now, evaluate each answer choice
BENCHMARK_MODE = True

# Define the options and their negations
options = {
    "A": lambda: Or(get_assignment('T', 1) == 'Grecia', get_assignment('T', 2) == 'Grecia'),
    "B": lambda: Or(get_assignment('W', 1) == 'Hakeem', get_assignment('W', 2) == 'Hakeem'),
    "C": lambda: Or(get_assignment('T', 1) == 'Joe', get_assignment('T', 2) == 'Joe'),
    "D": lambda: Or(get_assignment('Th', 1) == 'Joe', get_assignment('Th', 2) == 'Joe'),
    "E": lambda: Or(get_assignment('T', 1) == 'Louise', get_assignment('T', 2) == 'Louise'),
}

found_options = []
for letter, constr in options.items():
    solver.push()
    # Add the negation of the option
    solver.add(Not(constr()))
    if solver.check() == unsat:
        # If the negation is unsat, the option must be true
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