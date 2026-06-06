from z3 import *

solver = Solver()

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=first, 1=second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

G, H, J, K, L = 0, 1, 2, 3, 4
NUM_DAYS = 5

# assignment[d][s] = student working day d, shift s
assignment = [[Int(f"assign_{d}_{s}") for s in range(2)] for d in range(NUM_DAYS)]

# Each assignment is a valid student (0-4)
for d in range(NUM_DAYS):
    for s in range(2):
        solver.add(assignment[d][s] >= 0, assignment[d][s] <= 4)

# Each student works exactly 2 shifts
for student in range(5):
    solver.add(Sum([If(assignment[d][s] == student, 1, 0)
                     for d in range(NUM_DAYS) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(NUM_DAYS):
    solver.add(assignment[d][0] != assignment[d][1])

# Louise works second shift on two consecutive days (her only 2 shifts)
solver.add(Or(
    And(assignment[0][1] == L, assignment[1][1] == L),
    And(assignment[1][1] == L, assignment[2][1] == L),
    And(assignment[2][1] == L, assignment[3][1] == L),
    And(assignment[3][1] == L, assignment[4][1] == L)
))

# Grecia works first shift on two nonconsecutive days (her only 2 shifts)
solver.add(Sum([If(assignment[d][0] == G, 1, 0) for d in range(NUM_DAYS)]) == 2)
nonconsecutive_pairs = [(d1, d2) for d1 in range(NUM_DAYS)
                                 for d2 in range(d1+1, NUM_DAYS) if d2 - d1 > 1]
solver.add(Or([And(assignment[d1][0] == G, assignment[d2][0] == G)
               for d1, d2 in nonconsecutive_pairs]))

# Katya works on Tuesday and Friday only (exactly one shift each day)
solver.add(Sum([If(assignment[1][s] == K, 1, 0) for s in range(2)]) == 1)  # Tuesday
solver.add(Sum([If(assignment[4][s] == K, 1, 0) for s in range(2)]) == 1)  # Friday
for d in [0, 2, 3]:  # Mon, Wed, Thu - Katya doesn't work
    for s in range(2):
        solver.add(assignment[d][s] != K)

# Hakeem and Joe work on the same day at least once
solver.add(Or([Or(
    And(assignment[d][0] == H, assignment[d][1] == J),
    And(assignment[d][0] == J, assignment[d][1] == H)
) for d in range(NUM_DAYS)]))

# Grecia and Louise never work on the same day
for d in range(NUM_DAYS):
    solver.add(Not(Or(
        And(assignment[d][0] == G, assignment[d][1] == L),
        And(assignment[d][0] == L, assignment[d][1] == G)
    )))

# Additional condition: Katya works second shift on Tuesday
solver.add(assignment[1][1] == K)

# Define answer options
opt_a = (assignment[0][0] == G)  # Grecia works first shift on Monday
opt_b = (assignment[0][0] == H)  # Hakeem works first shift on Monday
opt_c = (assignment[2][1] == H)  # Hakeem works second shift on Wednesday
opt_d = (assignment[3][1] == J)  # Joe works second shift on Thursday
opt_e = (assignment[0][1] == L)  # Louise works second shift on Monday

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for d in range(NUM_DAYS):
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
            student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
            for s in range(2):
                shift_name = "1st" if s == 0 else "2nd"
                val = m.evaluate(assignment[d][s], model_completion=True)
                print(f"  {day_names[d]} {shift_name}: {student_names[int(str(val))]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")