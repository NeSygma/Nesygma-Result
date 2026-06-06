from z3 import *

# Variables representing properties of the mixture
hydrocarbon = Bool('hydrocarbon')
alkane = Bool('alkane')
organic = Bool('organic')
chemical = Bool('chemical')
containsCarbon = Bool('containsCarbon')
containsOnlyOneElement = Bool('containsOnlyOneElement')

solver = Solver()

# Premises
solver.add(Implies(hydrocarbon, organic))
solver.add(Implies(alkane, hydrocarbon))
solver.add(Implies(organic, chemical))
solver.add(Implies(organic, containsCarbon))
solver.add(Implies(chemical, Not(containsOnlyOneElement)))
# The mixture either both is a chemical compound and contains only one element, or neither.
# This is equivalent to chemical <-> containsOnlyOneElement
solver.add(Implies(chemical, containsOnlyOneElement))
solver.add(Implies(containsOnlyOneElement, chemical))

# Conclusion to evaluate
# If the mixture contains only one element or contains carbon, then the mixture is neither a chemical compound nor an alkane.
# Represented as: (containsOnlyOneElement ∨ containsCarbon) → (¬chemical ∧ ¬alkane)
conclusion = Implies(Or(containsOnlyOneElement, containsCarbon), And(Not(chemical), Not(alkane)))

# Check if premises entail the conclusion
# We test unsatisfiability of premises ∧ ¬conclusion
solver2 = Solver()
solver2.add(solver.assertions())
solver2.add(Not(conclusion))
res = solver2.check()
if res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif res == sat:
    # Provide a counterexample if needed
    m = solver2.model()
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
    print("Counterexample:")
    print("hydrocarbon =", m[hydrocarbon])
    print("alkane =", m[alkane])
    print("organic =", m[organic])
    print("chemical =", m[chemical])
    print("containsCarbon =", m[containsCarbon])
    print("containsOnlyOneElement =", m[containsOnlyOneElement])
else:
    print("STATUS: unknown")