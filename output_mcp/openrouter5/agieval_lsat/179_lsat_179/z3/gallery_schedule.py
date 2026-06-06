from z3 import *

# Students: Grecia(0), Hakeem(1), Joe(2), Katya(3), Louise(4)
# Days: Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4)
# Shifts: first(0), second(1)

students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Decision variable: shift[d][s] = student assigned to day d, shift s
shift = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Domain: each shift assigned to a student 0..4
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)

# Each student works exactly two shifts total
for stu in range(5):
    solver.add(Sum([If(shift[d][s] == stu, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# On two consecutive days, Louise works the second shift.
# Louise = 4, second shift = 1
# There exist two consecutive days d, d+1 such that shift[d][1] == 4 and shift[d+1][1] == 4
solver.add(Or([And(shift[d][1] == 4, shift[d+1][1] == 4) for d in range(4)]))

# On two nonconsecutive days, Grecia works the first shift.
# Grecia = 0, first shift = 0
# There exist two days d1, d2 with |d1-d2| > 1 such that shift[d1][0] == 0 and shift[d2][0] == 0
nonconsec_pairs = []
for d1 in range(5):
    for d2 in range(5):
        if abs(d1 - d2) > 1:
            nonconsec_pairs.append(And(shift[d1][0] == 0, shift[d2][0] == 0))
solver.add(Or(nonconsec_pairs))

# Katya works on Tuesday and Friday.
# Katya = 3. She works exactly one shift on Tuesday (day 1) and one on Friday (day 4).
solver.add(Or([shift[1][s] == 3 for s in range(2)]))
solver.add(Or([shift[4][s] == 3 for s in range(2)]))

# Hakeem and Joe work on the same day as each other at least once.
# Hakeem = 1, Joe = 2
solver.add(Or([And(Or([shift[d][0] == 1, shift[d][1] == 1]),
                   Or([shift[d][0] == 2, shift[d][1] == 2])) for d in range(5)]))

# Grecia and Louise never work on the same day as each other.
# Grecia = 0, Louise = 4
for d in range(5):
    solver.add(Not(And(Or([shift[d][s] == 0 for s in range(2)]),
                       Or([shift[d][s] == 4 for s in range(2)]))))

# Additional condition: Katya works the second shift on Tuesday.
solver.add(shift[1][1] == 3)

# Now evaluate each option
# Option A: Grecia works the first shift on Monday.
opt_a = (shift[0][0] == 0)

# Option B: Hakeem works the first shift on Monday.
opt_b = (shift[0][0] == 1)

# Option C: Hakeem works the second shift on Wednesday.
opt_c = (shift[2][1] == 1)

# Option D: Joe works the second shift on Thursday.
opt_d = (shift[3][1] == 2)

# Option E: Louise works the second shift on Monday.
opt_e = (shift[0][1] == 4)

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