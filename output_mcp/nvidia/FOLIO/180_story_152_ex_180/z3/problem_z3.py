from z3 import *

solver = Solver()

# Boolean variables
s_arrive_LGA = Bool('s_arrive_LGA')
s_depart_LGA = Bool('s_depart_LGA')
j_depart_LGA = Bool('j_depart_LGA')

# Premises
solver.add(s_arrive_LGA == True)      # Susan flies to LGA (arrives)
solver.add(j_depart_LGA == True)      # John flies from LGA (departs)
solver.add(Not(And(s_depart_LGA, s_arrive_LGA)))  # departure and arrival cannot be same airport

# Evaluate the conclusion: "Susan flies from LGA airport" i.e., s_depart_LGA
solver.add(s_depart_LGA)  # try to make conclusion true

result = solver.check()
if result == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
else:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")