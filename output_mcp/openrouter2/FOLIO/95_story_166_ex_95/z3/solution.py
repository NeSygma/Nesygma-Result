from z3 import *

# Variables
# deposit at Olive Garden
D = Int('D')
# monthly rent at Olive Garden
R = Int('R')

# Premises
solver = Solver()
# Monthly rent at Olive Garden is 2000
solver.add(R == 2000)
# Deposit can be equal to monthly rent or more
solver.add(D >= R)
# (Other premises are irrelevant for this conclusion)

# Conclusion: The security deposit at the Olive Garden is either $2000 or more.
# That is D >= 2000
conclusion = D >= 2000

# Check entailment: premises + not(conclusion) should be unsat
solver.push()
solver.add(Not(conclusion))
res = solver.check()
solver.pop()

if res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif res == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: unknown")