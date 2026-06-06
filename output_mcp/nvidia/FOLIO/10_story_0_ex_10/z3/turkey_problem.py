from z3 import *

# Boolean variables representing each turkey type
eastern = Bool('eastern')
osceola = Bool('osceola')
gould = Bool('gould')
merriam = Bool('merriam')
rio_grande = Bool('rio_grande')
ocellated = Bool('ocellated')

# Premises
premises = [
    Or(eastern, osceola, gould, merriam, rio_grande, ocellated),  # Tom is a wild turkey
    Not(eastern),          # Not Eastern
    Not(osceola),          # Not Osceola
    Not(gould),            # Not Gould's
    Not(merriam),          # Not Merriam's
    Not(rio_grande)        # Not Rio Grande
]

# Conclusion: Tom is an Ocellated wild turkey
conclusion = ocellated

# Check if the premises entail the conclusion
# We test two things:
# 1. Is (premises ∧ conclusion) satisfiable? (i.e., can conclusion be true?)
# 2. Is (premises ∧ ¬conclusion) satisfiable? (i.e., can conclusion be false?)

solver_yes = Solver()
solver_yes.add(premises)
solver_yes.add(conclusion)
sat_yes = solver_yes.check()

solver_no = Solver()
solver_no.add(premises)
solver_no.add(Not(conclusion))
sat_no = solver_no.check()

# Determine the answer
if sat_yes == unsat and sat_no == sat:
    # Premises force conclusion to be true (entailed)
    print("STATUS: proved")
    print("True")
elif sat_yes == sat and sat_no == unsat:
    # Premises force conclusion to be false (contradiction)
    print("STATUS: proved")
    print("False")
elif sat_yes == sat and sat_no == sat:
    # Both possible: uncertain
    print("STATUS: proved")
    print("Uncertain")
else:
    # This case means premises are inconsistent; vacuously everything holds
    print("STATUS: proved")
    print("InconsistentPremises")