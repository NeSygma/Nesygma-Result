from z3 import *

solver = Solver()

# Deposit variable for Olive Garden
Deposit = Int('Deposit')

# Premise: security deposit can be either equal to the monthly rent (2000) or more
solver.add(Or(Deposit == 2000, Deposit > 2000))

# Additional factual premises (do not affect the core logical relation)
solver.add(2000 > 1500)  # $2000 is more than $1500

# Negate the conclusion: "Deposit is either $2000 or more"
# Conclusion is the same as the premise: Or(Deposit == 2000, Deposit > 2000)
# Its negation is: Deposit != 2000 AND Deposit <= 2000
neg_conclusion = And(Deposit != 2000, Deposit <= 2000)
solver.add(neg_conclusion)

# Check satisfiability
result = solver.check()

# Output according to required format
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Deposit =", model[Deposit])
elif result == unsat:
    print("STATUS: proved")
    print("The premises entail the conclusion.")
else:
    print("STATUS: unknown")