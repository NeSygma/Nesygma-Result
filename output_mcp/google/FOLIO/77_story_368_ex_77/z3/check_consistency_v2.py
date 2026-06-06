from z3 import *

# Let's re-read the premise:
# "Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition."
# This is:
# HannahWorksStudentJob == True
# AND
# Implies(HannahNeedsMoney, And(Not(HannahPicky), Not(HannahNeedsMoney)))

# Wait, "neither picky nor needs to earn money" means:
# Not(HannahPicky) AND Not(HannahNeedsMoney)

# Let's re-check the logic:
# Implies(HannahNeedsMoney, And(Not(HannahPicky), Not(HannahNeedsMoney)))
# If HannahNeedsMoney is True, then (Not(HannahPicky) AND Not(HannahNeedsMoney)) must be True.
# This implies Not(HannahNeedsMoney) must be True.
# So if HannahNeedsMoney is True, then HannahNeedsMoney is False.
# This means HannahNeedsMoney MUST be False.

# Let's re-run the consistency check with this understanding.
HannahWorksStudentJob = Bool('HannahWorksStudentJob')
HannahNeedsMoney = Bool('HannahNeedsMoney')
HannahOrderTakeout = Bool('HannahOrderTakeout')
HannahEnjoyDiningHall = Bool('HannahEnjoyDiningHall')
HannahPicky = Bool('HannahPicky')
HannahSpendTimeDiningHall = Bool('HannahSpendTimeDiningHall')

solver = Solver()
# 1. If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
solver.add(Implies(HannahWorksStudentJob, HannahNeedsMoney))
# 2. If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
solver.add(Implies(HannahOrderTakeout, HannahWorksStudentJob))
# 3. People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
solver.add(Or(HannahOrderTakeout, HannahEnjoyDiningHall))
# 4. If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
solver.add(Implies(HannahEnjoyDiningHall, Not(HannahPicky)))
# 5. If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
solver.add(Implies(HannahEnjoyDiningHall, HannahSpendTimeDiningHall))
# 6. Hannah is at Mary's school. (Implicitly, she follows the rules)
# 7. Hannah works in student jobs on campus
solver.add(HannahWorksStudentJob == True)
# 8. and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.
solver.add(Implies(HannahNeedsMoney, And(Not(HannahPicky), Not(HannahNeedsMoney))))

print(f"Are premises consistent? {solver.check()}")
if solver.check() == sat:
    print(solver.model())
else:
    print("Inconsistent")