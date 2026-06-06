from z3 import *

# Re-evaluating the logic:
# P3: SecurityDeposit(b) >= MonthlyRent(b)
# P7: MonthlyRent(OliveGarden) = 2000
# Therefore: SecurityDeposit(OliveGarden) >= 2000
# P9: Tom rents if (AllowedToMoveInWith(Tom, Fluffy, b) AND SecurityDeposit(b) <= 1500)
# We know SecurityDeposit(OliveGarden) >= 2000.
# So, SecurityDeposit(OliveGarden) <= 1500 is FALSE.
# P9 is an implication: (A AND B) -> C.
# If (A AND B) is False, the implication doesn't force C to be True.
# Does it force C to be False? No, an implication (False -> C) is True regardless of C.
# So, Rents(Tom, OliveGarden) is not forced to be True or False by P9.

# Let's check if there are any other ways Tom could rent.
# The premises don't say "Tom will rent ONLY IF...".
# So, Rents(Tom, OliveGarden) is indeed Uncertain.

# Let's double check the logic with Z3.
# We want to see if Rents(Tom, OliveGarden) is True in all models or False in all models.

# Variables
SecurityDeposit_OliveGarden = Int('SecurityDeposit_OliveGarden')
AllowsPets_OliveGarden = Bool('AllowsPets_OliveGarden')
AllowedToMoveInWith_Tom_Fluffy_OliveGarden = Bool('AllowedToMoveInWith_Tom_Fluffy_OliveGarden')
Rents_Tom_OliveGarden = Bool('Rents_Tom_OliveGarden')

# Constraints
constraints = [
    SecurityDeposit_OliveGarden >= 2000,
    # P9: (AllowedToMoveInWith(Tom, Fluffy, OG) AND SecurityDeposit(OG) <= 1500) -> Rents(Tom, OG)
    Implies(And(AllowedToMoveInWith_Tom_Fluffy_OliveGarden, SecurityDeposit_OliveGarden <= 1500), Rents_Tom_OliveGarden),
    # P10: AllowsPets(OG) -> AllowedToMoveInWith(Tom, Fluffy, OG)
    Implies(AllowsPets_OliveGarden, AllowedToMoveInWith_Tom_Fluffy_OliveGarden)
]

# Check if Rents_Tom_OliveGarden is True in all models
s_true = Solver()
s_true.add(constraints)
s_true.add(Not(Rents_Tom_OliveGarden))
res_true = s_true.check() # If unsat, then Rents is always True

# Check if Rents_Tom_OliveGarden is False in all models
s_false = Solver()
s_false.add(constraints)
s_false.add(Rents_Tom_OliveGarden)
res_false = s_false.check() # If unsat, then Rents is always False

print(f"Is Rents always True? {res_true == unsat}")
print(f"Is Rents always False? {res_false == unsat}")