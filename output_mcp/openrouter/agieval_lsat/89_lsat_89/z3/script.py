from z3 import *

# Define variables for 5 solos (indices 0..4)
isWayne = [Bool(f'W{i}') for i in range(5)]  # True if Wayne, False if Zara
isTrad = [Bool(f'T{i}') for i in range(5)]   # True if Traditional, False if Modern

solver = Solver()

# Domain constraints are implicit for Bool

# Base constraints list
base = []

# 1. Solo 3 (index 2) is Traditional
base.append(isTrad[2] == True)

# 2. Exactly two of the traditional pieces are performed consecutively
# Define consecutive pairs
consec = [And(isTrad[i], isTrad[i+1]) for i in range(4)]
base.append(Sum([If(c, 1, 0) for c in consec]) == 1)
# Also ensure no three consecutive Trad (already covered by sum==1)
# (If there were three consecutive, there would be two consecutive pairs, violating sum==1)

# 3. In solo4 (index3), either Wayne performs a traditional piece OR Zara performs a modern piece.
cond3 = Or(And(isWayne[3], isTrad[3]), And(Not(isWayne[3]), Not(isTrad[3])))
base.append(cond3)

# 4. Pianist of solo2 (index1) != pianist of solo5 (index4)
base.append(isWayne[1] != isWayne[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece.
# For each position i, if there is no prior Wayne Modern, then this position cannot be Traditional.
for i in range(5):
    # prior positions j < i
    prior = []
    for j in range(i):
        prior.append(And(isWayne[j], Not(isTrad[j])))  # Wayne Modern
    if prior:
        no_prior = Not(Or(prior))
        base.append(Implies(no_prior, Not(isTrad[i])))
    else:
        # i == 0, no prior positions, so cannot be Traditional
        base.append(Not(isTrad[i]))

# Add all base constraints to solver
solver.add(base)

# Define count of Wayne Traditional pieces
wayne_trad_count = Sum([If(And(isWayne[i], isTrad[i]), 1, 0) for i in range(5)])

# Prepare universal quantifier to enforce minimal count >= X
vars_all = isWayne + isTrad
base_conj = And(*base)

found_options = []
options = [("A", 0), ("B", 1), ("C", 2), ("D", 3), ("E", 4)]
for letter, val in options:
    solver.push()
    # Existence of a schedule with count == val
    solver.add(wayne_trad_count == val)
    # Enforce that any schedule satisfying base constraints has count >= val
    # i.e., minimal count is at least val
    solver.add(ForAll(vars_all, Implies(base_conj, wayne_trad_count >= val)))
    if solver.check() == sat:
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