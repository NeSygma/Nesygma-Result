from z3 import *

solver = Solver()

# Positions are 1 to 7 (1-based indexing)
positions = range(1, 8)

# Articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Assign each article to a position
assignment = {art: Int(f'assignment_{art}') for art in articles}
for art in articles:
    solver.add(assignment[art] >= 1, assignment[art] <= 7)
    solver.add(Distinct(list(assignment.values())))

# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
topic = {
    'G': 'finance', 'H': 'finance', 'J': 'finance',
    'Q': 'nutrition', 'R': 'nutrition', 'S': 'nutrition',
    'Y': 'wildlife'
}

# Constraints
# 1. Consecutive articles cannot cover the same topic
for i in range(1, 7):
    for art1 in articles:
        for art2 in articles:
            solver.add(Implies(
                And(assignment[art1] == i, assignment[art2] == i + 1),
                topic[art1] != topic[art2]
            ))

# 2. S can be earlier than Q only if Q is third
solver.add(Implies(
    assignment['S'] < assignment['Q'],
    assignment['Q'] == 3
))

# 3. S must be earlier than Y
solver.add(assignment['S'] < assignment['Y'])

# 4. J must be earlier than G, and G must be earlier than R
solver.add(assignment['J'] < assignment['G'])
solver.add(assignment['G'] < assignment['R'])

# Additional constraint: Y is fourth
solver.add(assignment['Y'] == 4)

# Now evaluate the multiple choice options
found_options = []

# Option A: J is second
solver.push()
solver.add(assignment['J'] == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J is third
solver.push()
solver.add(assignment['J'] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q is first
solver.push()
solver.add(assignment['Q'] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Q is third
solver.push()
solver.add(assignment['Q'] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: R is seventh
solver.push()
solver.add(assignment['R'] == 7)
if solver.check() == sat:
    found_options.append("E")
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