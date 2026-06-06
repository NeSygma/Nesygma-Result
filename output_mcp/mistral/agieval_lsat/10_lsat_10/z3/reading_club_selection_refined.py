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

# Now check which option is necessarily true (must hold in all valid selections)
necessarily_true = []

# Option A: one French novel and one French play (must hold in all valid selections)
solver.push()
# Negation of A: either no French novels OR no French plays
solver.add(Or(Sum(FN) == 0, Sum(FP) == 0))
if solver.check() == unsat:
    necessarily_true.append("A")
solver.pop()

# Option B: one French novel and one Russian play (must hold in all valid selections)
solver.push()
# Negation of B: either no French novels OR no Russian play
solver.add(Or(Sum(FN) == 0, Not(RP)))
if solver.check() == unsat:
    necessarily_true.append("B")
solver.pop()

# Option C: one Russian novel and one French play (must hold in all valid selections)
solver.push()
# Negation of C: either no Russian novels OR no French plays
solver.add(Or(Sum(RN) == 0, Sum(FP) == 0))
if solver.check() == unsat:
    necessarily_true.append("C")
solver.pop()

# Option D: two French novels (must hold in all valid selections)
solver.push()
# Negation of D: fewer than two French novels
solver.add(Sum(FN) < 2)
if solver.check() == unsat:
    necessarily_true.append("D")
solver.pop()

# Option E: two Russian novels (must hold in all valid selections)
solver.push()
# Negation of E: fewer than two Russian novels
solver.add(Sum(RN) < 2)
if solver.check() == unsat:
    necessarily_true.append("E")
solver.pop()

if len(necessarily_true) == 1:
    print("STATUS: sat")
    print(f"answer:{necessarily_true[0]}")
elif len(necessarily_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessarily true options found {necessarily_true}")
else:
    print("STATUS: unsat")
    print("Refine: No necessarily true options found")