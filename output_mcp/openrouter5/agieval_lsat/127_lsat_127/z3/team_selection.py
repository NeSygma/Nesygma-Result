from z3 import *

# Variables: 8 employees, each is a Bool indicating if they are on the team
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

solver = Solver()

# At least 4 employees on the team
solver.add(Sum([If(v, 1, 0) for v in [M, O, P, S, T, W, Y, Z]]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))

# Now evaluate each option.
# Each option says "at least one of these two must be on the team".
# That means: for any valid team, at least one of the two is selected.
# So we test: is it possible to have a valid team where NEITHER is selected?
# If that's UNSAT, then at least one must be selected (the option is correct).
# If that's SAT, then it's possible to have neither, so the option is wrong.

options = [
    ("A", Or(O, S)),   # at least one of Ortega or Schmidt
    ("B", Or(O, W)),   # at least one of Ortega or Wong
    ("C", Or(P, S)),   # at least one of Paine or Schmidt
    ("D", Or(T, Y)),   # at least one of Thomson or Yoder
    ("E", Or(Y, Z))    # at least one of Yoder or Zayre
]

found_options = []
for letter, constr in options:
    solver.push()
    # Test: is there a valid team where NEITHER is selected?
    # i.e., Not(constr) means both are NOT on the team
    solver.add(Not(constr))
    if solver.check() == unsat:
        # It's impossible to have neither -> at least one must be on the team
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