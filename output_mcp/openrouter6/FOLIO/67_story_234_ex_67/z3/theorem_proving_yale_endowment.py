from z3 import *

# Define sorts
University = DeclareSort('University')
EndowmentValue = RealSort()

# Function: endowment of a university
Endowment = Function('Endowment', University, EndowmentValue)

# Constant for Yale
Yale = Const('Yale', University)

# Premises
premises = [
    Endowment(Yale) == RealVal(42300000000)  # $42.3 billion
]

# Conclusion: Yale has the largest endowment of any educational institution
# i.e., for all universities v, Endowment(v) <= Endowment(Yale)
v = Const('v', University)
conclusion = ForAll([v], Endowment(v) <= Endowment(Yale))

# Check positive goal (premises + conclusion)
s_pos = Solver()
s_pos.add(premises)
s_pos.add(conclusion)
pos_res = s_pos.check()

# Check negated goal (premises + not conclusion)
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(conclusion))
neg_res = s_neg.check()

# Interpret result
if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif neg_res == unsat and pos_res == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Unknown result")

# Additional debug info
print("Positive goal result:", pos_res)
print("Negated goal result:", neg_res)