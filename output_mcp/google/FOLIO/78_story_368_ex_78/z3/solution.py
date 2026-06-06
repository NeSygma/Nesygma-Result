from z3 import *

# Define variables
# H_at_Mary: Hannah is at Mary's school
# H_S: Hannah works in student jobs
# H_M: Hannah needs to earn money
# H_T: Hannah orders takeout frequently
# H_D: Hannah enjoys dining hall meals
# H_P: Hannah is a picky eater
# H_C: Hannah spends a lot of time eating/catching up

H_at_Mary = Bool('H_at_Mary')
H_S = Bool('H_S')
H_M = Bool('H_M')
H_T = Bool('H_T')
H_D = Bool('H_D')
H_P = Bool('H_P')
H_C = Bool('H_C')

# Premises
# P1: If people at Mary's school work in student jobs, then they need to earn money.
# (Assuming this applies to Hannah as she is at Mary's school)
p1 = Implies(H_S, H_M)

# P2: If people at Mary's school order takeout frequently, then they work in student jobs.
p2 = Implies(H_T, H_S)

# P3: People at Mary's school order takeout frequently or enjoy the dining hall meals.
p3 = Or(H_T, H_D)

# P4: If people at Mary's school enjoy the dining hall meals, then they are not picky eaters.
p4 = Implies(H_D, Not(H_P))

# P5: If people at Mary's school enjoy the dining hall meals, then they spend a lot of their time eating and catching up.
p5 = Implies(H_D, H_C)

# P6: Hannah is at Mary's school.
p6 = H_at_Mary

# P7: Hannah works in student jobs on campus.
p7 = H_S

# P8: Hannah works in student jobs on campus AND (if she needs to earn money, then she is neither picky nor needs to earn money).
p8 = And(H_S, Implies(H_M, And(Not(H_P), Not(H_M))))

premises = [p1, p2, p3, p4, p5, p6, p7, p8]

# Conclusion: Hannah is at Mary's school and she either is not a picky eater or, if she is, then she spends a lot of her time eating and catching up.
# Conclusion: H_at_Mary AND (~H_P OR (H_P -> H_C))
conclusion = And(H_at_Mary, Or(Not(H_P), Implies(H_P, H_C)))

# Theorem Proving
s_pos = Solver()
s_pos.add(premises)
s_pos.add(conclusion)

s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(conclusion))

res_pos = s_pos.check()
res_neg = s_neg.check()

print(f"Positive check: {res_pos}")
print(f"Negative check: {res_neg}")

if res_pos == sat and res_neg == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif res_pos == unsat and res_neg == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif res_pos == sat and res_neg == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif res_pos == unsat and res_neg == unsat:
    print("STATUS: proved")
    print("CONCLUSION: Inconsistent")
else:
    print("STATUS: unknown")