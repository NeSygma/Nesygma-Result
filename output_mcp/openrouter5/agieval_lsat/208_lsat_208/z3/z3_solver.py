from z3 import *

# Students: Juana, Kelly, Lateefah, Mei, Olga
# Teams: green (0), red (1)
# Facilitator: Bool per student

solver = Solver()

# Variables: team assignment (0=green, 1=red)
J, K, L, M, O = Ints('J K L M O')
students = [J, K, L, M, O]

# Domain: each student assigned to team 0 (green) or 1 (red)
for s in students:
    solver.add(Or(s == 0, s == 1))

# Facilitator variables
fac_J, fac_K, fac_L, fac_M, fac_O = Bools('fac_J fac_K fac_L fac_M fac_O')
fac = [fac_J, fac_K, fac_L, fac_M, fac_O]

# Exactly one facilitator per team
solver.add(Sum([If(And(students[i] == 0, fac[i]), 1, 0) for i in range(5)]) == 1)
solver.add(Sum([If(And(students[i] == 1, fac[i]), 1, 0) for i in range(5)]) == 1)

# Team sizes: one team has 2 members, the other has 3
green_count = Sum([If(students[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(students[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Condition 1: Juana and Olga are on different teams
solver.add(J != O)

# Condition 2: Lateefah is assigned to the green team
solver.add(L == 0)

# Condition 3: Kelly is not a facilitator
solver.add(fac_K == False)

# Condition 4: Olga is a facilitator
solver.add(fac_O == True)

names = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']

# Now evaluate each option

# Option A: green team: Juana, Lateefah, Olga (facilitator) -> green has 3, red has 2
# red team: Kelly, Mei (facilitator)
# So: J=0, L=0, O=0, K=1, M=1
# Green facilitator: Olga (fac_O=True), Red facilitator: Mei (fac_M=True)
# Others not facilitators: J=False, K=False, L=False
opt_a_constr = And(
    J == 0, L == 0, O == 0,
    K == 1, M == 1,
    fac_J == False, fac_K == False, fac_L == False, fac_O == True,
    fac_M == True
)

# Option B: green team: Kelly, Lateefah (facilitator), Olga -> green has 3, red has 2
# red team: Juana, Mei (facilitator)
# So: K=0, L=0, O=0, J=1, M=1
# Green facilitator: Lateefah (fac_L=True), Red facilitator: Mei (fac_M=True)
# Others not facilitators: J=False, K=False, O=False
opt_b_constr = And(
    K == 0, L == 0, O == 0,
    J == 1, M == 1,
    fac_J == False, fac_K == False, fac_L == True, fac_O == False,
    fac_M == True
)

# Option C: green team: Kelly, Lateefah, Olga (facilitator) -> green has 3, red has 2
# red team: Juana (facilitator), Mei
# So: K=0, L=0, O=0, J=1, M=1
# Green facilitator: Olga (fac_O=True), Red facilitator: Juana (fac_J=True)
# Others not facilitators: K=False, L=False, M=False
opt_c_constr = And(
    K == 0, L == 0, O == 0,
    J == 1, M == 1,
    fac_K == False, fac_L == False, fac_O == True,
    fac_J == True, fac_M == False
)

# Option D: green team: Kelly, Mei, Olga (facilitator) -> green has 3, red has 2
# red team: Juana (facilitator), Lateefah
# So: K=0, M=0, O=0, J=1, L=1
# Green facilitator: Olga (fac_O=True), Red facilitator: Juana (fac_J=True)
# Others not facilitators: K=False, M=False, L=False
opt_d_constr = And(
    K == 0, M == 0, O == 0,
    J == 1, L == 1,
    fac_K == False, fac_M == False, fac_O == True,
    fac_J == True, fac_L == False
)

# Option E: green team: Lateefah, Olga (facilitator) -> green has 2, red has 3
# red team: Juana, Kelly (facilitator), Mei
# So: L=0, O=0, J=1, K=1, M=1
# Green facilitator: Olga (fac_O=True), Red facilitator: Kelly (fac_K=True)
# But condition 3 says Kelly is not a facilitator! So this should be unsat.
opt_e_constr = And(
    L == 0, O == 0,
    J == 1, K == 1, M == 1,
    fac_L == False, fac_O == True,
    fac_J == False, fac_K == True, fac_M == False
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")