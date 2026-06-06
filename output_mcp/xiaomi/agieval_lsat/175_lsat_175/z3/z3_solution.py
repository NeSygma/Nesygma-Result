from z3 import *

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise
# Shifts: 0=first, 1=second

solver = Solver()

# Variables: shift[d][s] = student working day d, shift s
shift = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(5)]

# Each shift is assigned to exactly one student (0-4)
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)

# Each student works exactly two shifts total
for student in range(5):
    solver.add(Sum([If(shift[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# On two consecutive days, Louise (4) works the second shift
# There must exist at least one pair of consecutive days where Louise works second shift on both
solver.add(Or([And(shift[d][1] == 4, shift[d+1][1] == 4) for d in range(4)]))

# On two nonconsecutive days, Grecia (0) works the first shift
# Grecia works first shift on exactly 2 days, and those days are not consecutive
grecia_first = [Bool(f"grecia_first_{d}") for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (shift[d][0] == 0))
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(5)]) == 2)
# The two days must be nonconsecutive
for d in range(4):
    solver.add(Not(And(grecia_first[d], grecia_first[d+1])))

# Katya (3) works on Tuesday (1) and Friday (4)
# Katya works at least one shift on Tuesday and at least one shift on Friday
solver.add(Or(shift[1][0] == 3, shift[1][1] == 3))
solver.add(Or(shift[4][0] == 3, shift[4][1] == 3))

# Hakeem (1) and Joe (2) work on the same day as each other at least once
solver.add(Or([And(Or(shift[d][0] == 1, shift[d][1] == 1), Or(shift[d][0] == 2, shift[d][1] == 2)) for d in range(5)]))

# Grecia (0) and Louise (4) never work on the same day
for d in range(5):
    solver.add(Not(And(Or(shift[d][0] == 0, shift[d][1] == 0), Or(shift[d][0] == 4, shift[d][1] == 4))))

# Now test each option for second shifts (Mon-Fri)
# Option A: Hakeem(1), Louise(4), Louise(4), Hakeem(1), Katya(3)
opt_a_constr = And(shift[0][1] == 1, shift[1][1] == 4, shift[2][1] == 4, shift[3][1] == 1, shift[4][1] == 3)

# Option B: Joe(2), Hakeem(1), Grecia(0), Louise(4), Louise(4)
opt_b_constr = And(shift[0][1] == 2, shift[1][1] == 1, shift[2][1] == 0, shift[3][1] == 4, shift[4][1] == 4)

# Option C: Joe(2), Katya(3), Hakeem(1), Louise(4), Katya(3)
opt_c_constr = And(shift[0][1] == 2, shift[1][1] == 3, shift[2][1] == 1, shift[3][1] == 4, shift[4][1] == 3)

# Option D: Louise(4), Katya(3), Joe(2), Louise(4), Katya(3)
opt_d_constr = And(shift[0][1] == 4, shift[1][1] == 3, shift[2][1] == 2, shift[3][1] == 4, shift[4][1] == 3)

# Option E: Louise(4), Louise(4), Hakeem(1), Joe(2), Joe(2)
opt_e_constr = And(shift[0][1] == 4, shift[1][1] == 4, shift[2][1] == 1, shift[3][1] == 2, shift[4][1] == 2)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for d in range(5):
            first = m.evaluate(shift[d][0])
            second = m.evaluate(shift[d][1])
            print(f"  Day {d}: first={first}, second={second}")
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