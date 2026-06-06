from z3 import *

# Define variables
H_Work = Bool('H_Work')
H_Need = Bool('H_Need')
H_Order = Bool('H_Order')
H_Enjoy = Bool('H_Enjoy')
H_Picky = Bool('H_Picky')
H_Spend = Bool('H_Spend')

# Premises:
# 1. WorkStudentJob -> NeedMoney
# 2. OrderTakeout -> WorkStudentJob
# 3. OrderTakeout OR EnjoyDiningHall
# 4. EnjoyDiningHall -> Not(Picky)
# 5. EnjoyDiningHall -> SpendTimeDiningHall
# 6. Hannah is at Mary's school
# 7. Hannah works in student jobs on campus (H_Work = True)
# 8. If she needs to earn money to help pay for her college tuition, 
#    then she is neither picky nor needs to earn money to help pay for her college tuition.
#    (H_Need -> (Not(H_Picky) AND Not(H_Need)))

premises = [
    H_Work == True,
    Implies(H_Need, And(Not(H_Picky), Not(H_Need)))
]

# Conclusion: H_Need

# Theorem Proving Pattern:
# 1. Check if premises -> H_Need (Proved True)
# 2. Check if premises -> Not H_Need (Proved False)

s_pos = Solver()
s_pos.add(premises)
s_pos.add(H_Need)
res_pos = s_pos.check()

s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(H_Need))
res_neg = s_neg.check()

print(f"STATUS: proved")
if res_pos == unsat and res_neg == sat:
    print("CONCLUSION: False")
elif res_pos == sat and res_neg == unsat:
    print("CONCLUSION: True")
elif res_pos == sat and res_neg == sat:
    print("CONCLUSION: Uncertain")
else:
    print("CONCLUSION: Inconsistent")