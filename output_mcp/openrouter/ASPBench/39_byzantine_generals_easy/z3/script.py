from z3 import *

# Define constants for proposals of honest generals G1,G2,G3
p1 = IntVal(1)
p2 = IntVal(1)
p3 = IntVal(0)

# Consensus variable (0 or 1)
consensus = Int('consensus')

solver = Solver()
# consensus must be 0 or 1
solver.add(Or(consensus == 0, consensus == 1))

# Compute sum of honest proposals
sum_honest = p1 + p2 + p3
len_honest = 3

# Majority rule with tie-breaking to 0
# If sum*2 > len_honest => more 1s than 0s => consensus=1
# else consensus=0 (covers tie and majority 0)
solver.add(consensus == If(sum_honest * 2 > len_honest, 1, 0))

# Validity: if all honest have same value, consensus must equal that value
# all 0 case
solver.add(Implies(And(p1 == 0, p2 == 0, p3 == 0), consensus == 0))
# all 1 case
solver.add(Implies(And(p1 == 1, p2 == 1, p3 == 1), consensus == 1))

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("consensus =", m[consensus].as_long())
else:
    print("STATUS: unsat")