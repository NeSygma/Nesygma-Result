from z3 import *

# Define boolean variables for the state of the mountain range
inNM = Bool('inNM')  # Picuris Mountains in New Mexico
inTX = Bool('inTX')  # Picuris Mountains in Texas

solver = Solver()
# Premise: Picuris Mountains are in New Mexico or Texas
solver.add(Or(inNM, inTX))
# Premise: The mine is donated and located in the Picuris Mountains
# This implies the mountain range cannot be in Texas
solver.add(Not(inTX))

# Check if the conclusion "The mine is not located in a mountain range in New Mexico"
# i.e., Not(inNM) is unsatisfiable with the premises
solver.push()
solver.add(Not(inNM))
res_conclusion = solver.check()
solver.pop()

# Check if the negation of the conclusion (i.e., inNM) is satisfiable
solver.push()
solver.add(inNM)
res_neg_conclusion = solver.check()
solver.pop()

# Interpret results
if res_conclusion == unsat and res_neg_conclusion == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif res_conclusion == sat and res_neg_conclusion == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif res_conclusion == sat and res_neg_conclusion == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: proved")
    print("CONCLUSION: Inconsistent")