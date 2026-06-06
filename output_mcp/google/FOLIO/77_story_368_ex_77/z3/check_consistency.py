from z3 import *

# Re-evaluating the premises.
# P8: "Hannah works in student jobs on campus AND if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition."
# This is:
# HannahWorksStudentJob == True
# Implies(HannahNeedsMoney, And(HannahNotPicky, Not(HannahNeedsMoney)))

# Let's check the consistency of the premises again.
HannahWorksStudentJob = Bool('HannahWorksStudentJob')
HannahNeedsMoney = Bool('HannahNeedsMoney')
HannahOrderTakeout = Bool('HannahOrderTakeout')
HannahEnjoyDiningHall = Bool('HannahEnjoyDiningHall')
HannahNotPicky = Bool('HannahNotPicky')
HannahSpendTimeDiningHall = Bool('HannahSpendTimeDiningHall')

solver = Solver()
solver.add(Implies(HannahWorksStudentJob, HannahNeedsMoney))
solver.add(Implies(HannahOrderTakeout, HannahWorksStudentJob))
solver.add(Or(HannahOrderTakeout, HannahEnjoyDiningHall))
solver.add(Implies(HannahEnjoyDiningHall, HannahNotPicky))
solver.add(Implies(HannahEnjoyDiningHall, HannahSpendTimeDiningHall))
solver.add(HannahWorksStudentJob == True)
solver.add(Implies(HannahNeedsMoney, And(HannahNotPicky, Not(HannahNeedsMoney))))

print(f"Are premises consistent? {solver.check()}")
if solver.check() == unsat:
    print(solver.unsat_core())