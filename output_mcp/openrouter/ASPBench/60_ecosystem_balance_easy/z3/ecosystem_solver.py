from z3 import *

# Declare variables
grass = Real('grass')
rabbits = Real('rabbits')
foxes = Real('foxes')
hawks = Real('hawks')

# Consumption rates for each predator-prey link
r_rg = Real('r_rg')   # rabbits eat grass
r_fR = Real('r_fR')   # foxes eat rabbits
r_hR = Real('r_hR')   # hawks eat rabbits
r_hF = Real('r_hF')   # hawks eat foxes

solver = Solver()

# Population constraints
solver.add(grass > 0, grass <= 100)
solver.add(rabbits > 0, rabbits <= 30)
solver.add(foxes > 0, foxes <= 10)
solver.add(hawks > 0, hawks <= 5)

# Sustainability constraints
solver.add(rabbits <= 0.5 * grass)
solver.add(foxes <= 0.3 * rabbits)
# (No explicit constraint for hawks relative to prey, but consumption rates will limit)

# Consumption rate bounds
for rate in [r_rg, r_fR, r_hR, r_hF]:
    solver.add(rate >= 0.1, rate <= 0.5)

# Consumption cannot exceed available prey
solver.add(r_rg * rabbits <= grass)   # total grass consumed by rabbits
solver.add(r_fR * foxes <= rabbits)   # total rabbits consumed by foxes
solver.add(r_hR * hawks <= rabbits)   # total rabbits consumed by hawks
solver.add(r_hF * hawks <= foxes)    # total foxes consumed by hawks

# Check satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"grass = {m.eval(grass).as_decimal(5)}")
    print(f"rabbits = {m.eval(rabbits).as_decimal(5)}")
    print(f"foxes = {m.eval(foxes).as_decimal(5)}")
    print(f"hawks = {m.eval(hawks).as_decimal(5)}")
    print(f"r_rg (rabbit->grass) = {m.eval(r_rg).as_decimal(5)}")
    print(f"r_fR (fox->rabbit) = {m.eval(r_fR).as_decimal(5)}")
    print(f"r_hR (hawk->rabbit) = {m.eval(r_hR).as_decimal(5)}")
    print(f"r_hF (hawk->fox) = {m.eval(r_hF).as_decimal(5)}")
else:
    print("STATUS: unsat")