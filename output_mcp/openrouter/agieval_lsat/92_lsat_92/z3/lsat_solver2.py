from z3 import *

solver = Solver()
# Variables
isWayne = [Bool(f"W_{i+1}") for i in range(5)]
isTrad = [Bool(f"T_{i+1}") for i in range(5)]

# 1. third solo traditional
solver.add(isTrad[2] == True)

# 2. Exactly two of the traditional pieces are performed consecutively (interpretation: there is exactly one adjacent pair of trad pieces, and no other adjacency)
# At least two trad pieces total
solver.add(Sum([If(t,1,0) for t in isTrad]) >= 2)
# Exactly one consecutive pair
pair = [And(isTrad[i], isTrad[i+1]) for i in range(4)]
solver.add(Sum([If(p,1,0) for p in pair]) == 1)
# Ensure not three in a row (optional but covered by exactly one pair)
for i in range(3):
    solver.add(Not(And(isTrad[i], isTrad[i+1], isTrad[i+2])))

# 3. Fourth solo condition: (Wayne & trad) OR (Zara & modern)
cond4 = Or(And(isWayne[3], isTrad[3]), And(Not(isWayne[3]), Not(isTrad[3])))
solver.add(cond4)

# 4. Pianist of second != pianist of fifth
solver.add(isWayne[1] != isWayne[4])

# 5. No traditional piece until Wayne performs at least one modern piece
for i in range(5):
    earlier = []
    for j in range(i):
        earlier.append(And(isWayne[j], Not(isTrad[j])))
    if earlier:
        solver.add(Implies(isTrad[i], Or(earlier)))
    else:
        solver.add(isTrad[i] == False)

# Question condition: fifth solo Wayne traditional
solver.add(isWayne[4] == True)
solver.add(isTrad[4] == True)

# Options
options = []
options.append(("A", isWayne[0] == False))
options.append(("B", isWayne[1] == True))
options.append(("C", isWayne[2] == False))
options.append(("D", isTrad[1] == False))
options.append(("E", isTrad[3] == True))

found = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")