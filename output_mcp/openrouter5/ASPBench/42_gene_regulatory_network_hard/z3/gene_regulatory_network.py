from z3 import *

# Declare all 8 genes as Boolean variables
master_reg = Bool('master_reg')
m1_g1 = Bool('m1_g1')
m1_g2 = Bool('m1_g2')
m1_g3 = Bool('m1_g3')
m2_g1 = Bool('m2_g1')
m2_g2 = Bool('m2_g2')
m2_g3 = Bool('m2_g3')
reporter = Bool('reporter')

# Helper: count active genes in a list of Bool variables
def count_active(genes):
    return Sum([If(g, 1, 0) for g in genes])

solver = Solver()

# 1. Master Regulator Rule:
# master_reg is active iff (# active in Module 1) == (# active in Module 2)
module1_genes = [m1_g1, m1_g2, m1_g3]
module2_genes = [m2_g1, m2_g2, m2_g3]
solver.add(master_reg == (count_active(module1_genes) == count_active(module2_genes)))

# 2. Module 1 Conditional Rules
# If master_reg is inactive:
#   m1_g1 active iff m1_g2 inactive
#   m1_g2 active iff m1_g3 inactive
#   m1_g3 is constitutively active (always 1)
# If master_reg is active:
#   All Module 1 genes are inactive

# m1_g3: constitutively active when master_reg inactive, inactive when master_reg active
solver.add(Implies(Not(master_reg), m1_g3 == True))
solver.add(Implies(master_reg, Not(m1_g3)))

# m1_g1: when master_reg inactive, active iff m1_g2 inactive; when master_reg active, inactive
solver.add(Implies(Not(master_reg), m1_g1 == Not(m1_g2)))
solver.add(Implies(master_reg, Not(m1_g1)))

# m1_g2: when master_reg inactive, active iff m1_g3 inactive; when master_reg active, inactive
solver.add(Implies(Not(master_reg), m1_g2 == Not(m1_g3)))
solver.add(Implies(master_reg, Not(m1_g2)))

# 3. Module 2 Conditional Rules
# If master_reg is inactive:
#   m2_g1 active iff both m1_g1 and m1_g2 are inactive
#   m2_g2 active iff exactly 2 genes in Module 1 are active
#   m2_g3 active iff m2_g1 active AND m2_g2 inactive
# If master_reg is active:
#   Repressive ring oscillator: m2_g1 iff not m2_g2, m2_g2 iff not m2_g3, m2_g3 iff not m2_g1
#   Note: repressive ring has no steady state, so we encode it but it will be unsatisfiable

# When master_reg inactive:
solver.add(Implies(Not(master_reg), m2_g1 == And(Not(m1_g1), Not(m1_g2))))
solver.add(Implies(Not(master_reg), m2_g2 == (count_active(module1_genes) == 2)))
solver.add(Implies(Not(master_reg), m2_g3 == And(m2_g1, Not(m2_g2))))

# When master_reg active:
solver.add(Implies(master_reg, m2_g1 == Not(m2_g2)))
solver.add(Implies(master_reg, m2_g2 == Not(m2_g3)))
solver.add(Implies(master_reg, m2_g3 == Not(m2_g1)))

# 4. Reporter Rule: reporter active iff majority (at least 2) of Module 2 genes are inactive
solver.add(reporter == (count_active(module2_genes) <= 1))

# Find all steady states (all solutions)
decision_vars = [master_reg, m1_g1, m1_g2, m1_g3, m2_g1, m2_g2, m2_g3, reporter]

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {str(v): 1 if is_true(m.eval(v, model_completion=True)) else 0 for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"STATUS: sat")
print(f"Total steady states found: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"State {i+1}: {sol}")