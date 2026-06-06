from z3 import *

# Students: J, K, L, M, O
plays = ['S', 'T', 'U']
# Create Bool variables for each student-play
J = {p: Bool('J_' + p) for p in plays}
K = {p: Bool('K_' + p) for p in plays}
L = {p: Bool('L_' + p) for p in plays}
M = {p: Bool('M_' + p) for p in plays}
O = {p: Bool('O_' + p) for p in plays}

solver = Solver()

# Each student reviews at least one play
for student in [J, K, L, M, O]:
    solver.add(Or([student[p] for p in plays]))

# Constraint 1: Kramer and Lopez each review fewer plays than Megregian
def count(student):
    return Sum([If(student[p], 1, 0) for p in plays])
solver.add(count(K) < count(M))
solver.add(count(L) < count(M))

# Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(J[p], Not(L[p])))
    solver.add(Implies(J[p], Not(M[p])))

# Constraint 3: Kramer and O'Neill both review Tamerlane
solver.add(K['T'] == True)
solver.add(O['T'] == True)

# Constraint 4: Exactly one pair of students have identical review sets
students = {'J': J, 'K': K, 'L': L, 'M': M, 'O': O}
pair_eq = []
student_names = list(students.keys())
for i in range(len(student_names)):
    for j in range(i+1, len(student_names)):
        si = students[student_names[i]]
        sj = students[student_names[j]]
        eq = And([si[p] == sj[p] for p in plays])
        pair_eq.append(If(eq, 1, 0))
solver.add(Sum(pair_eq) == 1)

# Define option constraints
opt_a = count(J) > count(L)  # A
opt_b = count(M) > count(J)  # B
opt_c = count(M) > count(O)  # C
opt_d = count(O) > count(J)  # D
opt_e = count(O) > count(K)  # E

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")