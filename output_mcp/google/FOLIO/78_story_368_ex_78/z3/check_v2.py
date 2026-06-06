from z3 import *

# Define variables
# People at Mary's school:
# S: Work in student jobs on campus
# M: Need to earn money to help pay for college tuition
# T: Order takeout frequently
# D: Enjoy dining hall meals and recipes
# P: Picky eaters
# E: Spend a lot of time eating/catching up with friends

# Hannah (H):
# H_S: Hannah works in student jobs on campus
# H_M: Hannah needs to earn money to help pay for her college tuition
# H_T: Hannah orders takeout frequently
# H_D: Hannah enjoys dining hall meals and recipes
# H_P: Hannah is a picky eater
# H_E: Hannah spends a lot of time eating/catching up with friends

# Premises:
# 1. For all x in Mary's school: S(x) -> M(x)
# 2. For all x in Mary's school: T(x) -> S(x)
# 3. For all x in Mary's school: T(x) OR D(x)
# 4. For all x in Mary's school: D(x) -> Not(P(x))
# 5. For all x in Mary's school: D(x) -> E(x)
# 6. Hannah is at Mary's school.
# 7. H_S
# 8. H_M -> (Not(H_P) AND Not(H_M))

# Conclusion:
# Hannah is at Mary's school (True) AND (Not(H_P) OR (H_P -> H_E))

# Let's check the consistency of the premises.
s = Solver()

# Hannah is at Mary's school
# Premises for Hannah:
# H_S -> H_M
# H_T -> H_S
# H_T OR H_D
# H_D -> Not(H_P)
# H_D -> H_E
# H_S = True
# H_M -> (Not(H_P) AND Not(H_M))

H_S, H_M, H_T, H_D, H_P, H_E = Bools('H_S H_M H_T H_D H_P H_E')

s.add(Implies(H_S, H_M))
s.add(Implies(H_T, H_S))
s.add(Or(H_T, H_D))
s.add(Implies(H_D, Not(H_P)))
s.add(Implies(H_D, H_E))
s.add(H_S == True)
s.add(Implies(H_M, And(Not(H_P), Not(H_M))))

# Check if premises are consistent
res = s.check()
print(f"Consistency check: {res}")

# If consistent, check the conclusion
# Conclusion: (Not(H_P) OR (H_P -> H_E))
conclusion = Or(Not(H_P), Implies(H_P, H_E))

# Check if conclusion is true given premises
s.push()
s.add(Not(conclusion))
res_neg = s.check()
s.pop()

s.push()
s.add(conclusion)
res_pos = s.check()
s.pop()

print(f"Negated conclusion check: {res_neg}")
print(f"Positive conclusion check: {res_pos}")