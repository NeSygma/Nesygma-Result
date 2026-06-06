from z3 import *

# Define boolean variables for Hannah's properties
H_W = Bool('H_W')  # Hannah works in student jobs on campus
H_E = Bool('H_E')  # Hannah needs to earn money to help pay for college tuition
H_P = Bool('H_P')  # Hannah is a picky eater

# Premise 7: Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, 
# then she is neither picky nor needs to earn money to help pay for her college tuition.
premise7 = And(H_W, Implies(H_E, And(Not(H_P), Not(H_E))))

# The premises imply that H_E leads to a contradiction, so H_E must be false.
# Let's verify this by checking consistency

# Check if premises + H_E is satisfiable
s1 = Solver()
s1.add(premise7)
s1.add(H_E)
result1 = s1.check()

# Check if premises + Not(H_E) is satisfiable
s2 = Solver()
s2.add(premise7)
s2.add(Not(H_E))
result2 = s2.check()

# Output results
print("Premises + H_E satisfiable?", result1)
print("Premises + Not(H_E) satisfiable?", result2)

# Since premise7 implies Not(H_E) (to avoid contradiction), the conclusion H_E is false
if result1 == unsat and result2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result1 == sat and result2 == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result1 == sat and result2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")