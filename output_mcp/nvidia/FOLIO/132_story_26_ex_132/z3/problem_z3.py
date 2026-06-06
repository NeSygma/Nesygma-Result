from z3 import *

solver = Solver()

# Constants
p = Int('p')  # platypus
m = Int('m')  # some mammal with teeth
h = Int('h')  # human

# Predicates
M = Function('M', IntSort(), BoolSort())
T = Function('T', IntSort(), BoolSort())

# Premises
# 1. Some mammals have teeth
solver.add(M(m))
solver.add(T(m))

# 2. Platypus has no teeth
solver.add(Not(T(p)))

# 3. Platypus is a mammal
solver.add(M(p))

# 4. Humans have teeth
solver.add(T(h))

# Conclusion: Platypus is a mammal with no teeth
concl = And(M(p), Not(T(p)))

# Check if the conclusion is entailed by adding its negation
neg_concl = Not(concl)  # Or(Not(M(p)), T(p))
solver.add(neg_concl)

result = solver.check()
if result == unsat:
    print("STATUS: proved")
    print("Conclusion: True")
else:
    # Check if the conclusion is false (i.e., its negation is entailed)
    solver2 = Solver()
    solver2.add(M(m))
    solver2.add(T(m))
    solver2.add(Not(T(p)))
    solver2.add(M(p))
    solver2.add(T(h))
    solver2.add(concl)
    result2 = solver2.check()
    if result2 == unsat:
        print("STATUS: proved")
        print("Conclusion: False")
    else:
        print("STATUS: unknown")
        print("Conclusion: Uncertain")