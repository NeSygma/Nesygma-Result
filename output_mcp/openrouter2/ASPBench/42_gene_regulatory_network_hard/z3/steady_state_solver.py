from z3 import *

# Define genes as Int variables 0 or 1
master_reg = Int('master_reg')
m1_g1 = Int('m1_g1')
m1_g2 = Int('m1_g2')
m1_g3 = Int('m1_g3')
m2_g1 = Int('m2_g1')
m2_g2 = Int('m2_g2')
m2_g3 = Int('m2_g3')
reporter = Int('reporter')

solver = Solver()

# Domain constraints
vars = [master_reg, m1_g1, m1_g2, m1_g3, m2_g1, m2_g2, m2_g3, reporter]
for v in vars:
    solver.add(v >= 0, v <= 1)

# Helper sums
sum1 = m1_g1 + m1_g2 + m1_g3
sum2 = m2_g1 + m2_g2 + m2_g3

# Master Regulator Rule
solver.add(master_reg == If(sum1 == sum2, 1, 0))

# Module 1 Conditional Rules
# When master_reg is inactive (0)
solver.add(Implies(master_reg == 0, m1_g1 == 1 - m1_g2))
solver.add(Implies(master_reg == 0, m1_g2 == 1 - m1_g3))
solver.add(Implies(master_reg == 0, m1_g3 == 1))
# When master_reg is active (1)
solver.add(Implies(master_reg == 1, m1_g1 == 0))
solver.add(Implies(master_reg == 1, m1_g2 == 0))
solver.add(Implies(master_reg == 1, m1_g3 == 0))

# Module 2 Conditional Rules
# When master_reg is inactive (0)
solver.add(Implies(master_reg == 0, m2_g1 == If(And(m1_g1 == 0, m1_g2 == 0), 1, 0)))
solver.add(Implies(master_reg == 0, m2_g2 == If(sum1 == 2, 1, 0)))
solver.add(Implies(master_reg == 0, m2_g3 == If(And(m2_g1 == 1, m2_g2 == 0), 1, 0)))
# When master_reg is active (1) – repressive ring (unsatisfiable)
solver.add(Implies(master_reg == 1, m2_g1 == If(m2_g2 == 0, 1, 0)))
solver.add(Implies(master_reg == 1, m2_g2 == If(m2_g3 == 0, 1, 0)))
solver.add(Implies(master_reg == 1, m2_g3 == If(m2_g1 == 0, 1, 0)))

# Reporter Rule
solver.add(reporter == If(sum2 <= 1, 1, 0))

# Enumerate all solutions
states = []
while solver.check() == sat:
    m = solver.model()
    state = {
        'master_reg': m[master_reg].as_long(),
        'm1_g1': m[m1_g1].as_long(),
        'm1_g2': m[m1_g2].as_long(),
        'm1_g3': m[m1_g3].as_long(),
        'm2_g1': m[m2_g1].as_long(),
        'm2_g2': m[m2_g2].as_long(),
        'm2_g3': m[m2_g3].as_long(),
        'reporter': m[reporter].as_long()
    }
    states.append(state)
    # Block this solution
    solver.add(Or([v != m[v] for v in vars]))

# Output results
if states:
    print("STATUS: sat")
    for idx, st in enumerate(states, 1):
        print(f"state{idx}: {st}")
else:
    print("STATUS: unsat")