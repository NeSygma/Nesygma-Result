from z3 import *

# Declare Boolean variables for all genes
master_reg = Bool('master_reg')
m1_g1 = Bool('m1_g1')
m1_g2 = Bool('m1_g2')
m1_g3 = Bool('m1_g3')
m2_g1 = Bool('m2_g1')
m2_g2 = Bool('m2_g2')
m2_g3 = Bool('m2_g3')
reporter = Bool('reporter')

# Helper function to convert Bool to Int (1 for True, 0 for False)
def bool_to_int(b):
    return If(b, 1, 0)

# Count active genes in Module 1
count_m1 = bool_to_int(m1_g1) + bool_to_int(m1_g2) + bool_to_int(m1_g3)

# Count active genes in Module 2
count_m2 = bool_to_int(m2_g1) + bool_to_int(m2_g2) + bool_to_int(m2_g3)

# Count inactive genes in Module 2 (for reporter rule)
inactive_m2 = 3 - count_m2

# Create solver
solver = Solver()

# 1. Master Regulator Rule: master_reg ↔ (count_m1 == count_m2)
solver.add(master_reg == (count_m1 == count_m2))

# 2. Module 1 Rules (conditional on master_reg)
# Case: master_reg is inactive (False)
m1_inactive_case = And(
    Not(master_reg),
    # m1_g1 ↔ not m1_g2
    m1_g1 == Not(m1_g2),
    # m1_g2 ↔ not m1_g3
    m1_g2 == Not(m1_g3),
    # m1_g3 is constitutively active (True)
    m1_g3 == True
)

# Case: master_reg is active (True)
m1_active_case = And(
    master_reg,
    # All Module 1 genes are inactive
    Not(m1_g1),
    Not(m1_g2),
    Not(m1_g3)
)

# Module 1 must satisfy one of the two cases
solver.add(Or(m1_inactive_case, m1_active_case))

# 3. Module 2 Rules (conditional on master_reg)
# Case: master_reg is inactive (False)
m2_inactive_case = And(
    Not(master_reg),
    # m2_g1 ↔ (m1_g1 is inactive AND m1_g2 is inactive)
    m2_g1 == And(Not(m1_g1), Not(m1_g2)),
    # m2_g2 ↔ exactly 2 genes in Module 1 are active
    m2_g2 == (count_m1 == 2),
    # m2_g3 ↔ (m2_g1 is active AND m2_g2 is inactive)
    m2_g3 == And(m2_g1, Not(m2_g2))
)

# Case: master_reg is active (True) - repressive ring oscillator
# Note: This case has no steady state, but we'll encode it anyway
m2_active_case = And(
    master_reg,
    # m2_g1 ↔ not m2_g2
    m2_g1 == Not(m2_g2),
    # m2_g2 ↔ not m2_g3
    m2_g2 == Not(m2_g3),
    # m2_g3 ↔ not m2_g1
    m2_g3 == Not(m2_g1)
)

# Module 2 must satisfy one of the two cases
solver.add(Or(m2_inactive_case, m2_active_case))

# 4. Reporter Rule: reporter ↔ (at least 2 of 3 Module2 genes are inactive)
# This means: inactive_m2 >= 2
solver.add(reporter == (inactive_m2 >= 2))

# Find all steady states
steady_states = []
decision_vars = [master_reg, m1_g1, m1_g2, m1_g3, m2_g1, m2_g2, m2_g3, reporter]

while solver.check() == sat:
    model = solver.model()
    # Extract the state
    state = {}
    for var in decision_vars:
        state[str(var)] = 1 if model[var] == True else 0
    steady_states.append(state)
    
    # Blocking clause to find next solution
    solver.add(Or([var != model[var] for var in decision_vars]))

# Output results
print("STATUS: sat")
print(f"Found {len(steady_states)} steady state(s):")
for i, state in enumerate(steady_states):
    print(f"\nSteady State {i+1}:")
    for gene, value in state.items():
        print(f"  {gene}: {value}")

# Also print in the required format
print("\nsteady_states =", steady_states)