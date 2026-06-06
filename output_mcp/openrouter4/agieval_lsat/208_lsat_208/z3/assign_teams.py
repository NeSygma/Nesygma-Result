from z3 import *

# Map students to indices
J, K, L, M, O = 0, 1, 2, 3, 4
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']

solver = Solver()

# Team variables: 0 = green, 1 = red
team = [Int(f'team_{s}') for s in students]
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# Facilitator variables
facil = [Bool(f'facil_{s}') for s in students]

# Constraint 1: Juana and Olga different teams
solver.add(team[J] != team[O])

# Constraint 2: Lateefah is green team
solver.add(team[L] == 0)

# Constraint 3: Kelly is not a facilitator
solver.add(facil[K] == False)

# Constraint 4: Olga is a facilitator
solver.add(facil[O] == True)

# Team sizes: one team has 2, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# Each team has exactly one facilitator
green_facil_count = Sum([If(And(team[i] == 0, facil[i]), 1, 0) for i in range(5)])
red_facil_count = Sum([If(And(team[i] == 1, facil[i]), 1, 0) for i in range(5)])
solver.add(green_facil_count == 1)
solver.add(red_facil_count == 1)

# Now evaluate each answer choice
# Each option provides a complete assignment: team membership and facilitator designation

# Option A: green: Juana, Lateefah, Olga (facilitator) | red: Kelly, Mei (facilitator)
opt_a_constr = And(
    team[J] == 0, team[L] == 0, team[O] == 0,
    team[K] == 1, team[M] == 1,
    # Facilitators: O is facilitator (already in base), M is facilitator
    facil[M] == True,
    # Non-facilitators: J, L, K are not facilitators
    facil[J] == False, facil[L] == False, facil[K] == False
)

# Option B: green: Kelly, Lateefah (facilitator), Olga | red: Juana, Mei (facilitator)
opt_b_constr = And(
    team[K] == 0, team[L] == 0, team[O] == 0,
    team[J] == 1, team[M] == 1,
    facil[L] == True,  # Lateefah is facilitator
    facil[M] == True,  # Mei is facilitator
    # Non-facilitators
    facil[K] == False, facil[O] == False, facil[J] == False
)

# Option C: green: Kelly, Lateefah, Olga (facilitator) | red: Juana (facilitator), Mei
opt_c_constr = And(
    team[K] == 0, team[L] == 0, team[O] == 0,
    team[J] == 1, team[M] == 1,
    facil[O] == True,
    facil[J] == True,
    facil[K] == False, facil[L] == False, facil[M] == False
)

# Option D: green: Kelly, Mei, Olga (facilitator) | red: Juana (facilitator), Lateefah
opt_d_constr = And(
    team[K] == 0, team[M] == 0, team[O] == 0,
    team[J] == 1, team[L] == 1,
    facil[O] == True,
    facil[J] == True,
    facil[K] == False, facil[M] == False, facil[L] == False
)

# Option E: green: Lateefah, Olga (facilitator) | red: Juana, Kelly (facilitator), Mei
opt_e_constr = And(
    team[L] == 0, team[O] == 0,
    team[J] == 1, team[K] == 1, team[M] == 1,
    facil[O] == True,
    facil[K] == True,
    facil[L] == False, facil[J] == False, facil[M] == False
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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