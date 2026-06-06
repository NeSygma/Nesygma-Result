from z3 import *

# Articles and their topics
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
topics = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Create position variables for each article
pos = {a: Int(f'pos_{a}') for a in articles}

solver = Solver()

# Each article gets a unique position from 1 to 7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[a] for a in articles]))

# Constraint 1: Consecutive articles cannot cover the same topic
# For each pair of positions i and i+1, the articles at those positions must have different topics
# We need to ensure that for any two articles with same topic, they are not in consecutive positions
for a1 in articles:
    for a2 in articles:
        if a1 < a2 and topics[a1] == topics[a2]:
            # They cannot be in consecutive positions
            solver.add(Or(pos[a1] != pos[a2] + 1, pos[a2] != pos[a1] + 1))

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q, then Q must be in position 3
# Equivalent: If Q != 3, then S > Q
solver.add(Implies(pos['Q'] != 3, pos['S'] > pos['Q']))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J < G < R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now evaluate each answer choice
# The skeleton requires checking satisfiability of each option
# But the question asks for which condition makes the order fully determined
# So we need to check for uniqueness, not just satisfiability

# We'll modify the skeleton to check uniqueness
# For each option, we'll check if adding it yields exactly one solution

def count_solutions(solver, decision_vars):
    """Count the number of solutions by enumerating all models"""
    s = Solver()
    s.add(solver.assertions())
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple((v, m.eval(v, model_completion=True)) for v in decision_vars)
        solutions.append(sol)
        # Add blocking clause to prevent this exact solution
        blocking = Or([v != m.eval(v, model_completion=True) for v in decision_vars])
        s.add(blocking)
    return len(solutions)

# Base decision variables
decision_vars = [pos[a] for a in articles]

# Answer choices
options = [
    ("A", pos['H'] == 4),
    ("B", pos['H'] == 6),
    ("C", pos['R'] == 4),
    ("D", pos['R'] == 7),
    ("E", pos['Y'] == 5)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    # Check if this option yields exactly one solution
    num_solutions = count_solutions(solver, decision_vars)
    if num_solutions == 1:
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