from z3 import *

# Sorts
Person = DeclareSort('Person')
ETS = Const('ETS', Person)  # ETS is an entity that can provide financial aid

# Predicates
GREApplicant = Function('GREApplicant', Person, BoolSort())
ProvesEconomicHardship = Function('ProvesEconomicHardship', Person, BoolSort())
Taker = Function('Taker', Person, BoolSort())
Recipient = Function('Recipient', Person, Person, BoolSort())  # Recipient(provider, recipient)
SingleParentFamily = Function('SingleParentFamily', Person, BoolSort())
FewResources = Function('FewResources', Person, BoolSort())

# Constants
Tom = Const('Tom', Person)
x = Const('x', Person)
y = Const('y', Person)

# Premises
solver = Solver()

# Premise: ETS provides financial aid to those GRE applicants who prove economic hardship.
solver.add(ForAll([x], Implies(And(GREApplicant(x), ProvesEconomicHardship(x)), Recipient(ETS, x))))

# Premise: Those living in single-parent families or having few resources available to them can prove economic hardship.
solver.add(ForAll([x], Implies(Or(SingleParentFamily(x), FewResources(x)), ProvesEconomicHardship(x))))

# Premises about Tom
solver.add(SingleParentFamily(Tom))
solver.add(FewResources(Tom))
solver.add(GREApplicant(Tom))
solver.add(Taker(Tom))

# Check if premises are consistent
premises_consistent = solver.check()

# Check the conclusion: No one taking the GRE test has financial aid provided to them by something.
# To evaluate this, we check if there exists a taker who receives financial aid.
solver.push()
solver.add(Exists([x, y], And(Taker(x), Recipient(y, x))))
conclusion_check = solver.check()

if premises_consistent == unsat:
    print("STATUS: proved")
    print("CONCLUSION: Inconsistent premises")
elif conclusion_check == sat:
    print("STATUS: sat")
    print("Conclusion is False: There exists a taker who receives financial aid.")
    model = solver.model()
    taker = model[x]
    provider = model[y]
    print(f"Counterexample: {taker} is a taker and receives financial aid from {provider}")
    # Since Tom is a taker and ETS provides financial aid to Tom, this confirms the counterexample.
elif conclusion_check == unsat:
    print("STATUS: unsat")
    print("Conclusion is True: No taker receives financial aid.")
else:
    print("STATUS: unknown")
    print("Conclusion is Uncertain: Premises may be inconsistent or insufficient.")

solver.pop()

# Additional check: Is Tom a counterexample?
solver.push()
solver.add(Taker(Tom))
solver.add(Recipient(ETS, Tom))
tom_counterexample = solver.check()
if tom_counterexample == sat:
    print("\nTom is a counterexample:")
    print("Tom is a taker and receives financial aid from ETS.")
    print("STATUS: sat")
    print("CONCLUSION: The original conclusion is False.")
else:
    print("\nTom is not a counterexample.")

solver.pop()