from z3 import *

# Define boolean variables for each employee
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

# The question asks: which pair CANNOT be on the team together?
# We need to find the pair that is IMPOSSIBLE (unsat) to have both on the team.
# So we test each pair for satisfiability. The one that is unsat is the answer.

# Let's also print models for the sat ones to debug
options = [
    ("A", And(M, T)),  # Myers and Thomson
    ("B", And(O, Y)),  # Ortega and Yoder
    ("C", And(P, Z)),  # Paine and Zayre
    ("D", And(S, W)),  # Schmidt and Wong
    ("E", And(W, Y))   # Wong and Yoder
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter} ({constr}): {result}")
    if result == sat:
        m = solver.model()
        # Print which employees are on the team in this model
        team = [name for name, var in [("M",M),("O",O),("P",P),("S",S),("T",T),("W",W),("Y",Y),("Z",Z)] if m.eval(var, model_completion=True)]
        print(f"  Team: {team}")
        found_options.append(letter)
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