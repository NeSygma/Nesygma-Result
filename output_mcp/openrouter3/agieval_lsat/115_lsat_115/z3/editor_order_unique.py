from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Position variables for each article
pos = {article: Int(f'pos_{article}') for article in finance + nutrition + wildlife}

def count_solutions(base_constraints, extra_constraint=None):
    """Count number of solutions given base constraints and optional extra constraint"""
    s = Solver()
    # Add base constraints
    for constraint in base_constraints:
        s.add(constraint)
    # Add extra constraint if provided
    if extra_constraint:
        s.add(extra_constraint)
    
    # Count solutions by enumerating all possibilities
    solutions = []
    decision_vars = list(pos.values())
    
    while s.check() == sat:
        m = s.model()
        # Get the current solution
        sol = tuple((var, m[var]) for var in decision_vars)
        solutions.append(sol)
        # Block this solution
        s.add(Or([var != m[var] for var in decision_vars]))
    
    return len(solutions)

# Build base constraints
base_constraints = []

# Positions between 1 and 7
for article in pos:
    base_constraints.append(pos[article] >= 1)
    base_constraints.append(pos[article] <= 7)

# All positions distinct
base_constraints.append(Distinct(list(pos.values())))

# Topic constraints: consecutive articles cannot have same topic
for topic in [finance, nutrition, wildlife]:
    for i in range(len(topic)):
        for j in range(i+1, len(topic)):
            a1, a2 = topic[i], topic[j]
            base_constraints.append(Or(pos[a1] - pos[a2] != 1, pos[a2] - pos[a1] != 1))

# Constraint 2: S can be earlier than Q only if Q is third
base_constraints.append(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
base_constraints.append(pos['S'] < pos['Y'])

# Constraint 4: J must be earlier than G, and G must be earlier than R
base_constraints.append(pos['J'] < pos['G'])
base_constraints.append(pos['G'] < pos['R'])

# Test each option
found_options = []

# Option A: H is fourth
count_A = count_solutions(base_constraints, pos['H'] == 4)
if count_A == 1:
    found_options.append('A')

# Option B: H is sixth
count_B = count_solutions(base_constraints, pos['H'] == 6)
if count_B == 1:
    found_options.append('B')

# Option C: R is fourth
count_C = count_solutions(base_constraints, pos['R'] == 4)
if count_C == 1:
    found_options.append('C')

# Option D: R is seventh
count_D = count_solutions(base_constraints, pos['R'] == 7)
if count_D == 1:
    found_options.append('D')

# Option E: Y is fifth
count_E = count_solutions(base_constraints, pos['Y'] == 5)
if count_E == 1:
    found_options.append('E')

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")