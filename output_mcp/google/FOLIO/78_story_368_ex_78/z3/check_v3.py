from z3 import *

# Re-evaluating the premises:
# 8. Hannah works in student jobs on campus AND (if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition).
# H_S = True
# H_M -> (Not(H_P) AND Not(H_M))

# Let's re-examine the logic:
# H_M -> (Not(H_P) AND Not(H_M))
# This implies:
# If H_M is True:
#   Not(H_P) is True
#   Not(H_M) is True
#   So H_M is False.
#   Contradiction.
# Therefore, H_M must be False.

# Let's re-check the premises.
H_S, H_M, H_T, H_D, H_P, H_E = Bools('H_S H_M H_T H_D H_P H_E')

s = Solver()
s.add(Implies(H_S, H_M))
s.add(Implies(H_T, H_S))
s.add(Or(H_T, H_D))
s.add(Implies(H_D, Not(H_P)))
s.add(Implies(H_D, H_E))
s.add(H_S == True)
# The premise was: "Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition."
# This is: H_S AND (H_M -> (Not(H_P) AND Not(H_M)))
s.add(And(H_S, Implies(H_M, And(Not(H_P), Not(H_M)))))

print(f"Consistency check: {s.check()}")
if s.check() == sat:
    print(s.model())