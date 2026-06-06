from z3 import *

# Students: G=0, H=1, J=2, K=3, L=4
G, H, J, K, L = 0, 1, 2, 3, 4

solver = Solver()

# first[i] = student working first shift on day i (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri)
# second[i] = student working second shift on day i
first = [Int(f'first_{i}') for i in range(5)]
second = [Int(f'second_{i}') for i in range(5)]

# Domain: each shift is assigned to one of the 5 students
for i in range(5):
    solver.add(Or([first[i] == s for s in [G, H, J, K, L]]))
    solver.add(Or([second[i] == s for s in [G, H, J, K, L]]))

# Each student works exactly 2 shifts total
for s in [G, H, J, K, L]:
    total_shifts = Sum([If(first[i] == s, 1, 0) for i in range(5)]) + \
                   Sum([If(second[i] == s, 1, 0) for i in range(5)])
    solver.add(total_shifts == 2)

# Constraint 1: No student works both shifts of any day
for i in range(5):
    solver.add(first[i] != second[i])

# Constraint 2: On two consecutive days, Louise works the second shift.
# There exist i, i+1 where second[i]==L and second[i+1]==L
solver.add(Or([And(second[i] == L, second[i+1] == L) for i in range(4)]))

# Constraint 3: On two nonconsecutive days, Grecia works the first shift.
# There exist i, j with |i-j| > 1 where first[i]==G and first[j]==G
# Since each student works exactly 2 shifts, and Grecia works first on two nonconsecutive days,
# those are her two shifts.
nonconsec_pairs = [(i, j) for i in range(5) for j in range(5) if abs(i-j) > 1]
solver.add(Or([And(first[i] == G, first[j] == G) for (i, j) in nonconsec_pairs]))

# Also, since Grecia works exactly 2 shifts and both are first shifts,
# she never works second shift.
solver.add(And([second[i] != G for i in range(5)]))

# Constraint 4: Katya works on Tuesday (day 1) and Friday (day 4).
solver.add(Or(first[1] == K, second[1] == K))
solver.add(Or(first[4] == K, second[4] == K))

# Constraint 5: Hakeem and Joe work on the same day as each other at least once.
# There exists a day i where both H and J are on that day.
solver.add(Or([And(Or(first[i] == H, second[i] == H),
                   Or(first[i] == J, second[i] == J)) for i in range(5)]))

# Constraint 6: Grecia and Louise never work on the same day as each other.
for i in range(5):
    solver.add(Not(And(Or(first[i] == G, second[i] == G),
                       Or(first[i] == L, second[i] == L))))

# Now check the options
# Each option gives the list of second shift workers Mon-Fri

# Map student names to integers
name_to_int = {"Grecia": G, "Hakeem": H, "Joe": J, "Katya": K, "Louise": L}

options = {
    "A": ["Hakeem", "Louise", "Louise", "Hakeem", "Katya"],
    "B": ["Joe", "Hakeem", "Grecia", "Louise", "Louise"],
    "C": ["Joe", "Katya", "Hakeem", "Louise", "Katya"],
    "D": ["Louise", "Katya", "Joe", "Louise", "Katya"],
    "E": ["Louise", "Louise", "Hakeem", "Joe", "Joe"]
}

found_options = []
for letter, opt_list in options.items():
    solver.push()
    # Add constraint that second shifts match this option
    for i in range(5):
        solver.add(second[i] == name_to_int[opt_list[i]])
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