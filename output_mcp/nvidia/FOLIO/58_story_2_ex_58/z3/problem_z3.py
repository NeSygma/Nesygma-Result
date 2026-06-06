from z3 import *

# Declare state variables for each relevant city
state_Billings = Int('state_Billings')
state_Butte = Int('state_Butte')
state_Helena = Int('state_Helena')
state_Missoula = Int('state_Missoula')
state_WhiteSulphurSprings = Int('state_WhiteSulphurSprings')
state_StPierre = Int('state_StPierre')

# Constants: Montana = 0 (arbitrary but distinct)
MT = 0

# Premises
solver = Solver()
solver.add(state_Butte == MT)
solver.add(state_Helena == MT)
solver.add(state_Missoula == MT)
solver.add(state_WhiteSulphurSprings == MT)  # same state as Butte
solver.add(state_Billings == MT)             # Billings in Montana
solver.add(state_StPierre != MT)             # St Pierre not in Montana

# Goal: Butte and St Pierre are in the same state
goal = (state_Butte == state_StPierre)

# Check the goal with premises
solver.add(goal)
result_goal = solver.check()

# Check the negation of the goal with premises
solver2 = Solver()
solver2.add(state_Butte == MT)
solver2.add(state_Helena == MT)
solver2.add(state_Missoula == MT)
solver2.add(state_WhiteSulphurSprings == MT)
solver2.add(state_Billings == MT)
solver2.add(state_StPierre != MT)
solver2.add(Not(goal))
result_not_goal = solver2.check()

# Determine outcome
if result_goal == unsat and result_not_goal == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result_goal == sat and result_not_goal == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result_goal == sat and result_not_goal == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: unknown")