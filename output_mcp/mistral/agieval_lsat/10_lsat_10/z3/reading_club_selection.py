from z3 import *

solver = Solver()

# Create selection variables
FN = [Bool(f'FN{i}') for i in range(1, 4)]  # French novels
RN = [Bool(f'RN{i}') for i in range(1, 4)]  # Russian novels
FP = [Bool(f'FP{i}') for i in range(1, 3)]  # French plays
RP = Bool('RP')  # Russian play

# Constraint 1: Total selected works: at least 5, at most 6
total_selected = Sum(FN) + Sum(RN) + Sum(FP) + If(RP, 1, 0)
solver.add(total_selected >= 5, total_selected <= 6)

# Constraint 2: No more than 4 French works (French novels + French plays)
french_works = Sum(FN) + Sum(FP)
solver.add(french_works <= 4)

# Constraint 3: At least 3 but no more than 4 novels (French + Russian)
novels = Sum(FN) + Sum(RN)
solver.add(novels >= 3, novels <= 4)

# Constraint 4: At least as many French novels as Russian novels
solver.add(Sum(FN) >= Sum(RN))

# Constraint 5: If both French plays are selected, then Russian play is not selected
solver.add(Implies(And(FP[0], FP[1]), Not(RP)))

# Now evaluate each option using the exact skeleton
found_options = []

# Option A: one French novel and one French play (at least one each)
solver.push()
solver.add(Sum(FN) >= 1, Sum(FP) >= 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: one French novel and one Russian play (at least one each)
solver.push()
solver.add(Sum(FN) >= 1, RP)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: one Russian novel and one French play (at least one each)
solver.push()
solver.add(Sum(RN) >= 1, Sum(FP) >= 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: two French novels (at least two)
solver.push()
solver.add(Sum(FN) >= 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: two Russian novels (at least two)
solver.push()
solver.add(Sum(RN) >= 2)
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