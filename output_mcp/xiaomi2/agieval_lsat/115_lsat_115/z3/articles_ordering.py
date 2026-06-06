from z3 import *

# Articles: G, H, J (finance=0), Q, R, S (nutrition=1), Y (wildlife=2)
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
pos = {a: Int(f'pos_{a}') for a in articles}

# Topic mapping
topic = {'G': 0, 'H': 0, 'J': 0, 'Q': 1, 'R': 1, 'S': 1, 'Y': 2}

solver = Solver()

# Each article has a position 1-7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# All positions are distinct
solver.add(Distinct([pos[a] for a in articles]))

# Constraint 1: Consecutive articles cannot cover the same topic
# For every pair of articles, if they are in consecutive positions, they must have different topics
for a in articles:
    for b in articles:
        if a < b:  # avoid duplicates
            # If |pos[a] - pos[b]| == 1, then topics must differ
            solver.add(Implies(
                Or(pos[a] - pos[b] == 1, pos[b] - pos[a] == 1),
                topic[a] != topic[b]
            ))

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q, then Q == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J < G < R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Define option constraints
opt_a = (pos['H'] == 4)  # H is fourth
opt_b = (pos['H'] == 6)  # H is sixth
opt_c = (pos['R'] == 4)  # R is fourth
opt_d = (pos['R'] == 7)  # R is seventh
opt_e = (pos['Y'] == 5)  # Y is fifth

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

def count_solutions(base_solver, extra_constraint, max_count=2):
    """Count solutions up to max_count. Returns count and first solution."""
    s = Solver()
    # Copy base constraints
    for c in base_solver.assertions():
        s.add(c)
    s.add(extra_constraint)
    
    count = 0
    first_model = None
    decision_vars = [pos[a] for a in articles]
    
    while s.check() == sat and count < max_count:
        m = s.model()
        if count == 0:
            first_model = {a: m[pos[a]] for a in articles}
        count += 1
        # Block this solution
        s.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    
    return count, first_model

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    count, model = count_solutions(solver, True, max_count=2)
    solver.pop()
    
    if count == 1:
        found_options.append(letter)
        print(f"Option {letter}: UNIQUE solution - {model}")
    elif count == 0:
        print(f"Option {letter}: NO solution")
    else:
        print(f"Option {letter}: MULTIPLE solutions (not unique)")

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