from z3 import *

solver = Solver()

# Students: G=0, H=1, J=2, K=3, L=4
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]
student_names = {0: 'Grecia', 1: 'Hakeem', 2: 'Joe', 3: 'Katya', 4: 'Louise'}

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
days = 5

# first[i] = student working first shift on day i
# second[i] = student working second shift on day i
first = [Int(f'first_{i}') for i in range(days)]
second = [Int(f'second_{i}') for i in range(days)]

# Domain: each shift is worked by one of the 5 students
for i in range(days):
    solver.add(And(first[i] >= 0, first[i] <= 4))
    solver.add(And(second[i] >= 0, second[i] <= 4))

# Constraint 1: No student works both shifts of any day
for i in range(days):
    solver.add(first[i] != second[i])

# Constraint 2: Each student works exactly 2 shifts total
for s in students:
    total = Sum([If(first[i] == s, 1, 0) for i in range(days)] +
                [If(second[i] == s, 1, 0) for i in range(days)])
    solver.add(total == 2)

# Constraint 3: On two consecutive days, Louise works the second shift
# There exist consecutive days i, i+1 where second[i]==L and second[i+1]==L
solver.add(Or([And(second[i] == L, second[i+1] == L) for i in range(days-1)]))

# Constraint 4: On two nonconsecutive days, Grecia works the first shift
# There exist days i, j with |i-j| >= 2 where first[i]==G and first[j]==G
nonconsecutive_pairs = []
for i in range(days):
    for j in range(days):
        if abs(i - j) >= 2:
            nonconsecutive_pairs.append(And(first[i] == G, first[j] == G))
solver.add(Or(nonconsecutive_pairs))

# Constraint 5: Katya works on Tuesday (day 1) and Friday (day 4)
solver.add(Or(first[1] == K, second[1] == K))
solver.add(Or(first[4] == K, second[4] == K))

# Constraint 6: Hakeem and Joe work on the same day at least once
solver.add(Or([And(
    Or(first[i] == H, second[i] == H),
    Or(first[i] == J, second[i] == J)
) for i in range(days)]))

# Constraint 7: Grecia and Louise never work on the same day
for i in range(days):
    solver.add(Not(And(
        Or(first[i] == G, second[i] == G),
        Or(first[i] == L, second[i] == L)
    )))

# Now evaluate each answer choice for second shifts
# (A) Hakeem, Louise, Louise, Hakeem, Katya
# (B) Joe, Hakeem, Grecia, Louise, Louise
# (C) Joe, Katya, Hakeem, Louise, Katya
# (D) Louise, Katya, Joe, Louise, Katya
# (E) Louise, Louise, Hakeem, Joe, Joe

options = {
    "A": [H, L, L, H, K],
    "B": [J, H, G, L, L],
    "C": [J, K, H, L, K],
    "D": [L, K, J, L, K],
    "E": [L, L, H, J, J],
}

found_options = []
for letter, second_vals in options.items():
    solver.push()
    for i in range(days):
        solver.add(second[i] == second_vals[i])
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(days):
            print(f"  Day {i}: first={student_names[m[first[i]].as_long()]}, second={student_names[m[second[i]].as_long()]}")
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