from z3 import *

solver = Solver()

# Declare variables
team_juana = Int('team_juana')
team_kelly = Int('team_kelly')
team_lateefah = Int('team_lateefah')
team_mei = Int('team_mei')
team_olga = Int('team_olga')

facilitator_juana = Bool('facilitator_juana')
facilitator_kelly = Bool('facilitator_kelly')
facilitator_lateefah = Bool('facilitator_lateefah')
facilitator_mei = Bool('facilitator_mei')
facilitator_olga = Bool('facilitator_olga')

# Base constraints
# Team assignments: 0 = green, 1 = red
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
solver.add(Not(facilitator_kelly))

# Condition 4: Olga is a facilitator
solver.add(facilitator_olga == True)

# Team sizes: one team has 2, the other has 3
count_green = Sum([If(team_juana == 0, 1, 0),
                   If(team_kelly == 0, 1, 0),
                   If(team_lateefah == 0, 1, 0),
                   If(team_mei == 0, 1, 0),
                   If(team_olga == 0, 1, 0)])
count_red = 5 - count_green
solver.add(Or(And(count_green == 2, count_red == 3),
              And(count_green == 3, count_red == 2)))

# Exactly one facilitator per team
# Green team facilitator count
green_fac_count = Sum([If(And(facilitator_juana, team_juana == 0), 1, 0),
                       If(And(facilitator_kelly, team_kelly == 0), 1, 0),
                       If(And(facilitator_lateefah, team_lateefah == 0), 1, 0),
                       If(And(facilitator_mei, team_mei == 0), 1, 0),
                       If(And(facilitator_olga, team_olga == 0), 1, 0)])
red_fac_count = Sum([If(And(facilitator_juana, team_juana == 1), 1, 0),
                     If(And(facilitator_kelly, team_kelly == 1), 1, 0),
                     If(And(facilitator_lateefah, team_lateefah == 1), 1, 0),
                     If(And(facilitator_mei, team_mei == 1), 1, 0),
                     If(And(facilitator_olga, team_olga == 1), 1, 0)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Option constraints
opt_a_constr = And(facilitator_lateefah == True, team_lateefah == team_kelly)
opt_b_constr = And(facilitator_mei == True, team_mei == team_kelly)
opt_c_constr = And(facilitator_olga == True, team_olga == team_mei)  # facilitator_olga already true
opt_d_constr = And(facilitator_lateefah == True, team_lateefah != team_juana)
opt_e_constr = And(facilitator_mei == True, team_mei != team_olga)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # We are looking for options that must be false (unsat)
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