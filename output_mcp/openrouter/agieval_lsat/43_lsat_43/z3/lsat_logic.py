from z3 import *

# Students list
students = ['J', 'K', 'L', 'M', 'O']
plays = ['S', 'T', 'U']

# Create Bool variables for each student and play
vars = {}
for stu in students:
    for pl in plays:
        vars[(stu, pl)] = Bool(f"{stu}_{pl}")

# Helper to get variable
def v(stu, pl):
    return vars[(stu, pl)]

solver = Solver()

# Each student reviews at least one play
for stu in students:
    solver.add(Or(v(stu, 'S'), v(stu, 'T'), v(stu, 'U')))

# Kramer and O'Neill both review Tamerlane
solver.add(v('K', 'T') == True)
solver.add(v('O', 'T') == True)

# Kramer and Lopez each review fewer plays than Megregian
def count(stu):
    return Sum([If(v(stu, pl), 1, 0) for pl in plays])
solver.add(count('K') < count('M'))
solver.add(count('L') < count('M'))

# Neither Lopez nor Megregian reviews any play Jiang reviews
for pl in plays:
    solver.add(Not(And(v('J', pl), v('L', pl))))
    solver.add(Not(And(v('J', pl), v('M', pl))))

# Exactly one pair of students have identical review sets
pairs = []
pair_exprs = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        si = students[i]
        sj = students[j]
        eq = And(v(si, 'S') == v(sj, 'S'), v(si, 'T') == v(sj, 'T'), v(si, 'U') == v(sj, 'U'))
        pair_exprs.append(eq)
        pairs.append((si, sj, eq))
# Exactly one equality true
solver.add(Sum([If(eq, 1, 0) for eq in pair_exprs]) == 1)

# Define onlySunset predicate for each student
onlySunset = {stu: And(v(stu, 'S'), Not(v(stu, 'T')), Not(v(stu, 'U'))) for stu in students}

# Option constraints
options = {}
# A: Lopez only Sunset
options['A'] = And(onlySunset['L'],
                   And([Not(onlySunset[stu]) for stu in students if stu != 'L']))
# B: O'Neill only Sunset
options['B'] = And(onlySunset['O'],
                   And([Not(onlySunset[stu]) for stu in students if stu != 'O']))
# C: Jiang, Lopez only Sunset
options['C'] = And(onlySunset['J'], onlySunset['L'],
                   And([Not(onlySunset[stu]) for stu in students if stu not in ('J','L')]))
# D: Kramer, O'Neill only Sunset
options['D'] = And(onlySunset['K'], onlySunset['O'],
                   And([Not(onlySunset[stu]) for stu in students if stu not in ('K','O')]))
# E: Lopez, Megregian only Sunset
options['E'] = And(onlySunset['L'], onlySunset['M'],
                   And([Not(onlySunset[stu]) for stu in students if stu not in ('L','M')]))

found_options = []
for letter, constr in [('A', options['A']), ('B', options['B']), ('C', options['C']), ('D', options['D']), ('E', options['E'])]:
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