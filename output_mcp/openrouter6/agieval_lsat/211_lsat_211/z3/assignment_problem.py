from z3 import *

solver = Solver()

# Declare variables
team_juana = Int('team_juana')
team_kelly = Int('team_kelly')
team_lateefah = Int('team_lateefah')
team_mei = Int('team_mei')
team_olga = Int('team_olga')

fac_juana = Bool('fac_juana')
fac_kelly = Bool('fac_kelly')
fac_lateefah = Bool('fac_lateefah')
fac_mei = Bool('fac_mei')
fac_olga = Bool('fac_olga')

# Base constraints
# Team bounds: 0 = green, 1 = red
solver.add(team_juana >= 0, team_juana <= 1)
solver.add(team_kelly >= 0, team_kelly <= 1)
solver.add(team_lateefah >= 0, team_lateefah <= 1)
solver.add(team_mei >= 0, team_mei <= 1)
solver.add(team_olga >= 0, team_olga <= 1)

# Condition 1: Juana and Olga on different teams
solver.add(team_juana != team_olga)

# Condition 2: Lateefah on green team
solver.add(team_lateefah == 0)

# Condition 3: Kelly is not a facilitator
solver.add(Not(fac_kelly))

# Condition 4: Olga is a facilitator
solver.add(fac_olga)

# Additional assumption for this question: Lateefah is a facilitator
solver.add(fac_lateefah)

# Team size constraint: exactly 2 or 3 members in green team
count_green = Sum([
    If(team_juana == 0, 1, 0),
    If(team_kelly == 0, 1, 0),
    If(team_lateefah == 0, 1, 0),
    If(team_mei == 0, 1, 0),
    If(team_olga == 0, 1, 0)
])
solver.add(Or(count_green == 2, count_green == 3))

# Exactly one facilitator per team
green_fac_count = Sum([
    If(team_juana == 0, If(fac_juana, 1, 0), 0),
    If(team_kelly == 0, If(fac_kelly, 1, 0), 0),
    If(team_lateefah == 0, If(fac_lateefah, 1, 0), 0),
    If(team_mei == 0, If(fac_mei, 1, 0), 0),
    If(team_olga == 0, If(fac_olga, 1, 0), 0)
])
red_fac_count = Sum([
    If(team_juana == 1, If(fac_juana, 1, 0), 0),
    If(team_kelly == 1, If(fac_kelly, 1, 0), 0),
    If(team_lateefah == 1, If(fac_lateefah, 1, 0), 0),
    If(team_mei == 1, If(fac_mei, 1, 0), 0),
    If(team_olga == 1, If(fac_olga, 1, 0), 0)
])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Define option constraints
opt_a_constr = And(team_juana == 1, team_kelly == 1)
opt_b_constr = And(team_juana == 1, team_mei == 1)
opt_c_constr = And(team_lateefah == 0, team_olga == 0)
opt_d_constr = And(team_mei == 0, team_olga == 0)
opt_e_constr = And(team_mei == 1, team_olga == 1)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")