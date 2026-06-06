from z3 import *

solver = Solver()

# Declare boolean variables
dd_bd = Bool('dd_bd')
lsr_bd = Bool('lsr_bd')
dd_cr = Bool('dd_cr')
lsr_cr = Bool('lsr_cr')
bd_cr = Bool('bd_cr')
cc_cr = Bool('cc_cr')
mf_cr = Bool('mf_cr')
severe_bd = Bool('severe_bd')

# Premises
solver.add(severe_bd)  # Bile duct cancer is a severe cancer
solver.add(Implies(severe_bd, dd_bd))  # Severe cancers are deadly diseases
solver.add(Implies(dd_bd, lsr_bd))  # If deadly disease then low survival rate
solver.add(Implies(dd_cr, lsr_cr))  # Universal deadly disease -> low survival
solver.add(Implies(cc_cr, bd_cr))  # All Cholangiocarcinoma is bile duct cancer
solver.add(Not(And(bd_cr, lsr_cr)))  # Colorectal is not both bile duct cancer and low survival

# Evaluate conclusion: colorectal is Cholangiocarcinoma and (Mild flu or Bile duct cancer)
conclusion = And(cc_cr, Or(mf_cr, bd_cr))

# Check satisfiability of premises + conclusion
solver.push()
solver.add(conclusion)
sat_concl = solver.check()
model_concl = solver.model() if sat_concl == sat else None
solver.pop()

# Check satisfiability of premises + not conclusion
solver.push()
solver.add(Not(conclusion))
sat_not_concl = solver.check()
model_not_concl = solver.model() if sat_not_concl == sat else None
solver.pop()

# Determine result
if sat_concl == sat and sat_not_concl == sat:
    print("STATUS: unknown")
    print("RESULT: Uncertain")
elif sat_concl == sat and sat_not_concl == unsat:
    print("STATUS: proved")
    print("RESULT: True")
elif sat_concl == unsat and sat_not_concl == sat:
    print("STATUS: proved")
    print("RESULT: False")
else:
    print("STATUS: unknown")
    print("RESULT: Unknown")