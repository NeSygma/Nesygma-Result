from z3 import *

# Initialize solver
solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = [0, 1, 2]

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
witnesses = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']
witness_vars = {w: Int(w) for w in witnesses}

# Assign each witness to a day
for w in witnesses:
    solver.add(witness_vars[w] >= 0, witness_vars[w] <= 2)

# Constraints:
# 1. Franco does not testify on the same day as Garcia
solver.add(witness_vars['Franco'] != witness_vars['Garcia'])

# 2. Iturbe testifies on Wednesday (day 2)
solver.add(witness_vars['Iturbe'] == 2)

# 3. Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([witness_vars[w] == 1 for w in witnesses]) == 2)

# 4. Hong does not testify on Monday (day 0)
solver.add(witness_vars['Hong'] != 0)

# 5. At least one witness testifies on Monday (day 0)
solver.add(Sum([witness_vars[w] == 0 for w in witnesses]) >= 1)

# Additional condition: Franco is scheduled to testify on the same day as Hong
solver.add(witness_vars['Franco'] == witness_vars['Hong'])

# Now evaluate the options (A-E) to see which MUST be true
# We will check if the negation of each option leads to a contradiction
necessary_options = []

# Option A: Franco is scheduled to testify on Wednesday.
# Negation: Franco is not scheduled to testify on Wednesday.
neg_a = (witness_vars['Franco'] != 2)
solver.push()
solver.add(neg_a)
if solver.check() == unsat:
    necessary_options.append("A")
solver.pop()

# Option B: Garcia is scheduled to testify on Monday.
# Negation: Garcia is not scheduled to testify on Monday.
neg_b = (witness_vars['Garcia'] != 0)
solver.push()
solver.add(neg_b)
if solver.check() == unsat:
    necessary_options.append("B")
solver.pop()

# Option C: Garcia is scheduled to testify on Wednesday.
# Negation: Garcia is not scheduled to testify on Wednesday.
neg_c = (witness_vars['Garcia'] != 2)
solver.push()
solver.add(neg_c)
if solver.check() == unsat:
    necessary_options.append("C")
solver.pop()

# Option D: Hong is scheduled to testify on Tuesday.
# Negation: Hong is not scheduled to testify on Tuesday.
neg_d = (witness_vars['Hong'] != 1)
solver.push()
solver.add(neg_d)
if solver.check() == unsat:
    necessary_options.append("D")
solver.pop()

# Option E: Iturbe is the only witness scheduled to testify on Wednesday.
# Negation: Iturbe is not the only witness scheduled to testify on Wednesday.
neg_e = Or(
    witness_vars['Iturbe'] != 2,
    Sum([witness_vars[w] == 2 for w in witnesses]) > 1
)
solver.push()
solver.add(neg_e)
if solver.check() == unsat:
    necessary_options.append("E")
solver.pop()

# Output the result
if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")