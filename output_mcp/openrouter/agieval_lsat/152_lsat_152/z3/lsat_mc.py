from z3 import *

# Colors abbreviations: F=forest, O=olive, P=peach, T=turquoise, W=white, Y=yellow
colors = ['F','O','P','T','W','Y']

# Boolean: whether a color is used
used = {c: Bool(f'used_{c}') for c in colors}
# Integer: which rug (1..3) the color is assigned to (if used)
rug = {c: Int(f'rug_{c}') for c in colors}

solver = Solver()

# Domain constraints for rug indices
for c in colors:
    solver.add(rug[c] >= 1, rug[c] <= 3)

# Exactly five colors are used
solver.add(Sum([If(used[c], 1, 0) for c in colors]) == 5)

# Helper: count of used colors in a given rug i
def count_in_rug(i):
    return Sum([If(And(used[c], rug[c] == i), 1, 0) for c in colors])

# Each rug must have either 1 or 3 colors
for i in [1,2,3]:
    solver.add(Or(count_in_rug(i) == 1, count_in_rug(i) == 3))

# Exactly two rugs are solid (count == 1) and one rug is multicolored (count == 3)
solver.add(Sum([If(count_in_rug(i) == 1, 1, 0) for i in [1,2,3]]) == 2)
solver.add(Sum([If(count_in_rug(i) == 3, 1, 0) for i in [1,2,3]]) == 1)

# Rules
# 1. If white is used, its rug must have exactly 3 colors
solver.add(Implies(used['W'], count_in_rug(rug['W']) == 3))
# 2. Olive rule: if olive used, peach also used, same rug, and that rug has 3 colors
solver.add(Implies(used['O'], And(used['P'], rug['P'] == rug['O'], count_in_rug(rug['O']) == 3)))
# 3. Forest and turquoise not together in same rug
solver.add(Not(And(used['F'], used['T'], rug['F'] == rug['T'])))
# 4. Peach and turquoise not together in same rug
solver.add(Not(And(used['P'], used['T'], rug['P'] == rug['T'])))
# 5. Peach and yellow not together in same rug
solver.add(Not(And(used['P'], used['Y'], rug['P'] == rug['Y'])))

# Helper: a color is solid (its rug count == 1)
def solid(col):
    return And(used[col], count_in_rug(rug[col]) == 1)

# Option constraints
option_constraints = {}
option_constraints['A'] = And(solid('F'), solid('P'))  # forest and peach solid
option_constraints['B'] = And(solid('F'), solid('Y'))  # forest and yellow solid
option_constraints['C'] = And(solid('P'), solid('T'))  # peach and turquoise solid
option_constraints['D'] = And(solid('P'), solid('Y'))  # peach and yellow solid
option_constraints['E'] = And(solid('T'), solid('Y'))  # turquoise and yellow solid

found_options = []
for letter, constr in option_constraints.items():
    solver.push()
    solver.add(constr)
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