from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

solver = Solver()

# Each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct
solver.add(Distinct([pos[c] for c in compositions]))

# Condition 1: T is performed either immediately before F or immediately after R.
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# |pos[F] - pos[R]| >= 3
solver.add(Or(pos['F'] + 3 <= pos['R'], pos['R'] + 3 <= pos['F']))

# Condition 3: O is performed either first or fifth.
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 5: P is performed at some time before S.
solver.add(pos['P'] < pos['S'])

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# |pos[O] - pos[S]| >= 2
solver.add(Or(pos['O'] + 2 <= pos['S'], pos['S'] + 2 <= pos['O']))

# Given: P is performed third and S is performed sixth.
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Now evaluate each answer choice for what must be fifth.
# The question asks: "the composition performed fifth must be"
# So we need to find which option(s) are forced to be the fifth position.

# Let's first find what position 5 can be
print("All solutions for position 5:")
solver.push()
solutions = []
while solver.check() == sat:
    m = solver.model()
    fifth = None
    for c in compositions:
        if m[pos[c]].as_long() == 5:
            fifth = c
            break
    solutions.append(fifth)
    # Block this solution
    solver.add(Or([pos[c] != m.eval(pos[c], model_completion=True).as_long() for c in compositions]))
solver.pop()
print(f"Possible values for position 5: {set(solutions)}")

# Now evaluate each answer choice
# Each choice says the fifth must be one of two options
# We need to check if the fifth MUST be one of those two (i.e., it's forced)

# Option A: F or H
# Option B: F or O
# Option C: F or T
# Option D: H or L
# Option E: O or R

# For each option, we check: is it possible that the fifth is NOT in that set?
# If it's impossible (unsat), then the fifth MUST be in that set.

found_options = []

# Option A: F or H
solver.push()
solver.add(Not(Or(pos['F'] == 5, pos['H'] == 5)))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: F or O
solver.push()
solver.add(Not(Or(pos['F'] == 5, pos['O'] == 5)))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: F or T
solver.push()
solver.add(Not(Or(pos['F'] == 5, pos['T'] == 5)))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: H or L
solver.push()
solver.add(Not(Or(pos['H'] == 5, pos['L'] == 5)))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: O or R
solver.push()
solver.add(Not(Or(pos['O'] == 5, pos['R'] == 5)))
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")