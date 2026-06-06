from z3 import *

# Define variables
# People at Mary's school (general)
# WorkStudentJob, NeedMoney, OrderTakeout, EnjoyDiningHall, NotPicky, SpendTimeDiningHall
# Hannah (specific)
# HannahWorksStudentJob, HannahNeedsMoney, HannahOrderTakeout, HannahEnjoyDiningHall, HannahNotPicky, HannahSpendTimeDiningHall

# Premises
# 1. If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
# 2. If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
# 3. People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
# 4. If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
# 5. If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
# 6. Hannah is at Mary's school.
# 7. Hannah works in student jobs on campus.
# 8. If she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.

# Conclusion: Hannah is at Mary's school and she is not a picky eater and spends a lot of her time eating and catching up with friends in the campus dining halls.

# Let's model Hannah's properties
HannahWorksStudentJob = Bool('HannahWorksStudentJob')
HannahNeedsMoney = Bool('HannahNeedsMoney')
HannahOrderTakeout = Bool('HannahOrderTakeout')
HannahEnjoyDiningHall = Bool('HannahEnjoyDiningHall')
HannahNotPicky = Bool('HannahNotPicky')
HannahSpendTimeDiningHall = Bool('HannahSpendTimeDiningHall')

solver = Solver()

# Premises for Hannah (assuming she follows the school's general rules)
# P1: WorkStudentJob -> NeedMoney
solver.add(Implies(HannahWorksStudentJob, HannahNeedsMoney))
# P2: OrderTakeout -> WorkStudentJob
solver.add(Implies(HannahOrderTakeout, HannahWorksStudentJob))
# P3: OrderTakeout OR EnjoyDiningHall
solver.add(Or(HannahOrderTakeout, HannahEnjoyDiningHall))
# P4: EnjoyDiningHall -> NotPicky
solver.add(Implies(HannahEnjoyDiningHall, HannahNotPicky))
# P5: EnjoyDiningHall -> SpendTimeDiningHall
solver.add(Implies(HannahEnjoyDiningHall, HannahSpendTimeDiningHall))
# P7: Hannah works in student jobs on campus
solver.add(HannahWorksStudentJob == True)
# P8: HannahNeedsMoney -> (NotPicky AND NotNeedMoney)
solver.add(Implies(HannahNeedsMoney, And(HannahNotPicky, Not(HannahNeedsMoney))))

# Conclusion to evaluate
conclusion = And(HannahNotPicky, HannahSpendTimeDiningHall)

# Check if conclusion is True, False, or Uncertain
# 1. Check if premises imply conclusion
s_pos = Solver()
s_pos.add(solver.assertions())
s_pos.add(Not(conclusion))
res_pos = s_pos.check()

# 2. Check if premises imply NOT conclusion
s_neg = Solver()
s_neg.add(solver.assertions())
s_neg.add(conclusion)
res_neg = s_neg.check()

print(f"Premises consistent: {solver.check()}")
print(f"Negated conclusion satisfiable: {res_pos}")
print(f"Conclusion satisfiable: {res_neg}")