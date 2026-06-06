from z3 import *

# Create solver
solver = Solver()

# Houses: J, K, L, M, N, O, P
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
# Position variables: position[house] = time slot (1-7)
position = {h: Int(f'pos_{h}') for h in houses}

# Domain constraints: each house gets a unique position 1-7
for h in houses:
    solver.add(position[h] >= 1, position[h] <= 7)

# All positions must be distinct
solver.add(Distinct([position[h] for h in houses]))

# Rule 1: J must be shown in the evening (slots 6 or 7)
solver.add(Or(position['J'] == 6, position['J'] == 7))

# Rule 2: K cannot be shown in the morning (slots 1-2)
solver.add(Or(position['K'] >= 3, position['K'] <= 2))  # Wait, this is wrong
# Correct: K cannot be in morning, so K must be in afternoon or evening
solver.add(Or(position['K'] >= 3, position['K'] <= 2))  # This is still wrong
# Let me fix: K cannot be 1 or 2
solver.add(Or(position['K'] >= 3, position['K'] <= 2))  # Still wrong
# Actually: K cannot be in morning means K != 1 and K != 2
solver.add(And(position['K'] != 1, position['K'] != 2))

# Rule 3: L must be shown after K and before M
solver.add(position['K'] < position['L'])
solver.add(position['L'] < position['M'])

# Now test each answer choice
# We need to check which one MUST be true (i.e., true in all valid models)
# For "must be true", we check if the negation leads to unsat

# Answer choices:
# (A) K is shown in the evening (position[K] = 6 or 7)
# (B) L is shown in the afternoon (position[L] = 3, 4, or 5)
# (C) L is shown in the evening (position[L] = 6 or 7)
# (D) M is shown in the morning (position[M] = 1 or 2)
# (E) M is shown in the afternoon (position[M] = 3, 4, or 5)

# We'll test each choice by checking if its negation is unsatisfiable
# If negation is unsat, then the choice must be true

found_options = []

# Test A: K is shown in the evening
solver.push()
solver.add(Not(Or(position['K'] == 6, position['K'] == 7)))  # Negation: K not in evening
if solver.check() == unsat:
    found_options.append('A')
solver.pop()

# Test B: L is shown in the afternoon
solver.push()
solver.add(Not(Or(position['L'] == 3, position['L'] == 4, position['L'] == 5)))  # Negation: L not in afternoon
if solver.check() == unsat:
    found_options.append('B')
solver.pop()

# Test C: L is shown in the evening
solver.push()
solver.add(Not(Or(position['L'] == 6, position['L'] == 7)))  # Negation: L not in evening
if solver.check() == unsat:
    found_options.append('C')
solver.pop()

# Test D: M is shown in the morning
solver.push()
solver.add(Not(Or(position['M'] == 1, position['M'] == 2)))  # Negation: M not in morning
if solver.check() == unsat:
    found_options.append('D')
solver.pop()

# Test E: M is shown in the afternoon
solver.push()
solver.add(Not(Or(position['M'] == 3, position['M'] == 4, position['M'] == 5)))  # Negation: M not in afternoon
if solver.check() == unsat:
    found_options.append('E')
solver.pop()

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