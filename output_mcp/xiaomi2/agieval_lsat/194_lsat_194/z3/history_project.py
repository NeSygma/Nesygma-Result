from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# assign[s] = 0 means not assigned, 1=1921, 2=1922, 3=1923, 4=1924
L, M, O, R, T, Y = 0, 1, 2, 3, 4, 5
students = [L, M, O, R, T, Y]
names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

assign = [Int(f'assign_{names[s]}') for s in range(6)]

# Domain: each student assigned to 0 (not assigned) or 1-4 (a year)
for s in range(6):
    solver.add(Or(assign[s] == 0, assign[s] == 1, assign[s] == 2, assign[s] == 3, assign[s] == 4))

# Exactly 4 students are assigned (non-zero)
solver.add(Sum([If(assign[s] != 0, 1, 0) for s in range(6)]) == 4)

# Each year has exactly one student: all non-zero assignments are distinct
for i in range(6):
    for j in range(i+1, 6):
        solver.add(Implies(And(assign[i] != 0, assign[j] != 0), assign[i] != assign[j]))

# Condition 1: Only Louis or Tiffany can be assigned to 1923
for s in range(6):
    if s != L and s != T:
        solver.add(assign[s] != 3)

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assign[M] != 0, Or(assign[M] == 1, assign[M] == 2)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assign[T] != 0, assign[R] != 0))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
solver.add(Implies(assign[R] != 0, And(assign[O] != 0, assign[O] == assign[R] - 1)))

# Additional constraint: Yoshio is NOT assigned
solver.add(assign[Y] == 0)

# Now test each option
options = {
    "A": assign[L] == 0,           # Louis is not assigned
    "B": assign[R] == 0,           # Ryan is not assigned
    "C": assign[T] == 0,           # Tiffany is not assigned
    "D": assign[O] == 2,           # Onyx is assigned to 1922
    "E": assign[L] == 4,           # Louis is assigned to 1924
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: ", end="")
        for s in range(6):
            val = m[assign[s]]
            if val is not None and val.as_long() != 0:
                print(f"{names[s]}->{1920+val.as_long()}", end=" ")
        print()
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