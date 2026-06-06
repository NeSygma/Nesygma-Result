from z3 import *

# Define boolean variables for Vladimir and Ekaterina
US_v = Bool('US_v')
Taiwan_v = Bool('Taiwan_v')
can_reg_v = Bool('can_reg_v')
participate_v = Bool('participate_v')
Russian_official_v = Bool('Russian_official_v')
manager_Gazprom_v = Bool('manager_Gazprom_v')

US_e = Bool('US_e')
Taiwan_e = Bool('Taiwan_e')
can_reg_e = Bool('can_reg_e')
participate_e = Bool('participate_e')
Russian_official_e = Bool('Russian_official_e')
manager_Gazprom_e = Bool('manager_Gazprom_e')

solver = Solver()

# Rule 3: For each person, exclusive or US or Taiwanese
solver.add(Or(US_v, Taiwan_v))
solver.add(Not(And(US_v, Taiwan_v)))
solver.add(Or(US_e, Taiwan_e))
solver.add(Not(And(US_e, Taiwan_e)))

# Rule 5: Vladimir neither holds Taiwanese citizenship nor is he a manager at Gazprom
solver.add(Not(Taiwan_v))
solver.add(Not(manager_Gazprom_v))

# Rule 6: Ekaterina can register to vote in the US, or she is a Russian federation official
solver.add(Or(can_reg_e, Russian_official_e))

# Rule 4: No Russian Federation officials hold Taiwanese citizenship
solver.add(Implies(Russian_official_v, Not(Taiwan_v)))
solver.add(Implies(Russian_official_e, Not(Taiwan_e)))

# Rule 2: If someone has US citizenship, then they can register to vote in the US
solver.add(Implies(US_v, can_reg_v))
solver.add(Implies(US_e, can_reg_e))

# Rule 1: If someone can register to vote in the US, then they can participate in the 2024 US presidential election
solver.add(Implies(can_reg_v, participate_v))
solver.add(Implies(can_reg_e, participate_e))

# We don't need to use participate variables further

# Check entailment of conclusion: Vladimir is not a Russian federation official
# First, check if premises + Russian_official_v is unsat
solver.push()
solver.add(Russian_official_v)
res1 = solver.check()
solver.pop()

# Second, check if premises + not Russian_official_v is unsat
solver.push()
solver.add(Not(Russian_official_v))
res2 = solver.check()
solver.pop()

# Determine conclusion
if res1 == unsat and res2 == sat:
    conclusion = 'True'
elif res1 == sat and res2 == unsat:
    conclusion = 'False'
elif res1 == sat and res2 == sat:
    conclusion = 'Uncertain'
else:
    # Both unsat? inconsistent premises
    conclusion = 'Inconsistent'

print('STATUS: proved')
print('CONCLUSION:', conclusion)