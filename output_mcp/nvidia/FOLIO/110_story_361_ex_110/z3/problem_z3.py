from z3 import *

# Declare Boolean variables representing Peter's properties
spill = Bool('spill')
tidy = Bool('tidy')
clumsy = Bool('clumsy')
cleanly = Bool('cleanly')
valueOrderSpotlessness = Bool('valueOrderSpotlessness')
familyPrioritizes = Bool('familyPrioritizes')

# Premises
premises = [
    Implies(spill, Not(tidy)),           # If spill then not tidy
    Implies(clumsy, spill),              # All clumsy foodies spill
    Implies(cleanly, tidy),              # If cleanly then tidy
    Implies(valueOrderSpotlessness, cleanly),  # Value order/spotlessness -> cleanly
    Implies(familyPrioritizes, valueOrderSpotlessness),  # Family prioritizes -> value order/spotlessness
    Or(And(spill, cleanly), And(Not(spill), Not(cleanly)))  # Peter's dichotomy
]

# Conclusion to evaluate
conclusion = Or(And(clumsy, familyPrioritizes), And(Not(clumsy), Not(familyPrioritizes)))

# Check if the conclusion follows from the premises (premises ∧ conclusion)
s1 = Solver()
s1.add(premises)
s1.add(conclusion)
sat_concl = s1.check()

# Check if the negation of the conclusion is compatible with the premises (premises ∧ ¬conclusion)
s2 = Solver()
s2.add(premises)
s2.add(Not(conclusion))
unsat_concl = s2.check()

BENCHMARK_MODE = True  # Model‑finding mode

if sat_concl == sat and unsat_concl == unsat:
    # Conclusion is entailed (must be true)
    print("STATUS: proved")
    print("True")
elif sat_concl == unsat and unsat_concl == sat:
    # Conclusion is contradicted (must be false)
    print("STATUS: proved")
    print("False")
elif sat_concl == sat and unsat_concl == sat:
    # Both possible → uncertain
    print("STATUS: unknown")
    print("Uncertain")
else:
    # Inconsistent premises
    print("STATUS: unknown")
    print("Inconsistent")