from z3 import *

solver = Solver()

# Variables: each person assigned to a zone (1, 2, or 3)
Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall = Ints('Kim Mahr Parra Quinn Stuckey Tiao Udall')
people = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]
names = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']

for p in people:
    solver.add(Or(p == 1, p == 2, p == 3))

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(Parra == 1, Tiao != 1), And(Parra != 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(Tiao == 2, Udall != 2), And(Tiao != 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Constraint 5: More reps in Zone 3 than in Zone 2
zone2_count = Sum([If(p == 2, 1, 0) for p in people])
zone3_count = Sum([If(p == 3, 1, 0) for p in people])
solver.add(zone3_count > zone2_count)

# Define options - each is a conjunction that we test for satisfiability
options = [
    ("A", And(Kim == 1, Stuckey == 1)),
    ("B", And(Kim == 3, Stuckey == 3)),
    ("C", And(Mahr == 3, Stuckey == 3)),
    ("D", And(Mahr == 3, Udall == 3)),
    ("E", And(Parra == 1, Stuckey == 1)),
]

# For "must be false" question: the correct answer is the option that is UNSAT
# (impossible given the constraints)
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        found_options.append(letter)
        print(f"Option {letter}: UNSAT (must be false)")
    elif result == sat:
        m = solver.model()
        print(f"Option {letter}: SAT (could be true)")
        for n, p in zip(names, people):
            print(f"  {n} -> Zone {m[p]}")
    else:
        print(f"Option {letter}: unknown")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that must be false")