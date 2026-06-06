from z3 import *

# Declare symbolic variables for Bonnie's properties
performs_often = Bool('performs_often')
engaged = Bool('engaged')
inactive = Bool('inactive')
chaperones = Bool('chaperones')
attends_school = Bool('attends_school')
young_or_teen = Bool('young_or_teen')

# Premises as constraints
premises = []

# P1: People who perform in school talent shows often attend and are very engaged with school events.
premises.append(Implies(performs_often, engaged))

# P2: People in this club either perform in school talent shows often or are inactive and disinterested community members.
premises.append(Or(performs_often, inactive))

# P3: People in this club who chaperone high school dances are not students who attend the school.
premises.append(Implies(chaperones, Not(attends_school)))

# P4: All people in this club who are inactive and disinterested members of their community chaperone high school dances.
premises.append(Implies(inactive, chaperones))

# P5: All young children and teenagers in this club who wish to further their academic careers and educational opportunities are students who attend the school.
premises.append(Implies(young_or_teen, attends_school))

# P6: Bonnie is in this club and she either both attends and is very engaged with school events and is a student who attends the school
# or is not someone who both attends and is very engaged with school events and is not a student who attends the school.
# This simplifies to: (engaged ∧ attends_school) ∨ (¬attends_school)
premises.append(Or(And(engaged, attends_school), Not(attends_school)))

# Define the conclusion
# C: If Bonnie is either (young_or_teen ∧ chaperones) or (¬young_or_teen ∧ ¬chaperones), then Bonnie is either attends_school or inactive
conclusion = Implies(
    Or(And(young_or_teen, chaperones), And(Not(young_or_teen), Not(chaperones))),
    Or(attends_school, inactive)
)

# Theorem proving: Check if premises entail the conclusion
# We check both: premises + ¬conclusion (should be unsat if entailed)
# and premises + conclusion (should be sat if consistent)

# Check 1: premises + ¬conclusion
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(conclusion))
neg_result = s_neg.check()

# Check 2: premises + conclusion
s_pos = Solver()
s_pos.add(premises)
s_pos.add(conclusion)
pos_result = s_pos.check()

# Interpret results
print("=== Theorem Proving Results ===")
print(f"Premises + ¬Conclusion satisfiable: {neg_result == sat}")
print(f"Premises + Conclusion satisfiable: {pos_result == sat}")

if neg_result == unsat and pos_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: True (the conclusion is entailed by the premises)")
elif neg_result == sat and pos_result == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False (the conclusion contradicts the premises)")
elif neg_result == sat and pos_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain (the premises do not determine the conclusion)")
elif neg_result == unsat and pos_result == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent (premises are contradictory)")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconclusive solver result")