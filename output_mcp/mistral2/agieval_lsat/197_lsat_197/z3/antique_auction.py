from z3 import *

# Initialize solver
solver = Solver()

# Days: 1 (June 1) to 6 (June 6)
days = [1, 2, 3, 4, 5, 6]

# Antiques
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Assign each antique to a unique day
solver.add(Distinct(harmonica, lamp, mirror, sundial, table, vase))
for d in days:
    solver.add(Or(
        harmonica == d,
        lamp == d,
        mirror == d,
        sundial == d,
        table == d,
        vase == d
    ))

# Constraint 1: The sundial is not auctioned on June 1st.
solver.add(sundial != 1)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both.
solver.add(Or(
    And(table < harmonica, Not(table < vase)),
    And(table < vase, Not(table < harmonica))
))

# Define the options as constraints
options = {
    "A": And(table == 2, lamp == 3),
    "B": And(sundial == 2, vase == 3),
    "C": And(mirror == 3, sundial == 4),
    "D": And(vase == 4, sundial == 5),
    "E": And(sundial == 4, table == 5)
}

# Check each option
found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")