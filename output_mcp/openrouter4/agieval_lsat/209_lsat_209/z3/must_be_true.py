from z3 import *

students = ['J', 'K', 'L', 'M', 'O']

# Evaluate each option by checking if its negation is unsatisfiable
# If NOT(option) is unsat, then the option must be true in all valid configurations.

found_options = []

for letter, neg_constraint in [
    # A: Juana is assigned to the red team. Negation: Juana is on green team.
    ("A", [Int('team_J') == 0]),
    # B: Lateefah is a facilitator. Negation: Lateefah is not a facilitator.
    ("B", [Bool('fac_L') == False]),
    # C: Olga is assigned to the green team. Negation: Olga is on red team.
    ("C", [Int('team_O') == 1]),
    # D: Juana and Mei are not both facilitators. Negation: Both are facilitators.
    ("D", [And(Bool('fac_J') == True, Bool('fac_M') == True)]),
    # E: Neither Juana nor Kelly is a facilitator. Negation: Juana or Kelly is a facilitator.
    ("E", [Or(Bool('fac_J') == True, Bool('fac_K') == True)])
]:
    solver = Solver()

    # Team assignment: 0 = green, 1 = red
    team_J = Int('team_J')
    team_K = Int('team_K')
    team_L = Int('team_L')
    team_M = Int('team_M')
    team_O = Int('team_O')

    fac_J = Bool('fac_J')
    fac_K = Bool('fac_K')
    fac_L = Bool('fac_L')
    fac_M = Bool('fac_M')
    fac_O = Bool('fac_O')

    all_teams = [team_J, team_K, team_L, team_M, team_O]
    all_facs = [fac_J, fac_K, fac_L, fac_M, fac_O]
    all_students = list(zip('JKLMO', all_teams, all_facs))

    # Domain: each team is 0 or 1
    for t in all_teams:
        solver.add(Or(t == 0, t == 1))

    # Team sizes: green team (0) has either 2 or 3 members
    green_count = Sum([If(t == 0, 1, 0) for t in all_teams])
    solver.add(Or(green_count == 2, green_count == 3))

    # One facilitator per team
    green_fac = Sum([If(And(t == 0, f), 1, 0) for t, f in zip(all_teams, all_facs)])
    red_fac = Sum([If(And(t == 1, f), 1, 0) for t, f in zip(all_teams, all_facs)])
    solver.add(green_fac == 1)
    solver.add(red_fac == 1)

    # Constraints
    solver.add(team_J != team_O)  # Juana different team than Olga
    solver.add(team_L == 0)  # Lateefah is green
    solver.add(Not(fac_K))  # Kelly is not facilitator
    solver.add(fac_O)  # Olga is facilitator

    # Add the negation constraint for this option
    solver.add(neg_constraint)

    if solver.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")