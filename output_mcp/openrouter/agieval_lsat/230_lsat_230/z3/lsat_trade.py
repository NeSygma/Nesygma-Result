from z3 import *

# Companies: 0=RealProp,1=Southco,2=Trustcorp
# Buildings with classes
buildings = ['G','F','Y','Z','L','K','M','O']
classes = {'G':1,'F':1,'Y':3,'Z':3,'L':2,'K':2,'M':2,'O':2}
# Owner variables: Int 0..2
owner = {b: Int(f'owner_{b}') for b in buildings}
solver = Solver()
for b in buildings:
    solver.add(And(owner[b] >= 0, owner[b] <= 2))

# Helper to compute counts per company
def count_expr(comp, cls):
    return Sum([If(And(owner[b] == comp, classes[b] == cls), 1, 0) for b in buildings])

# Initial invariants per company
# I1: 2*c1 + c2 = 2*I1_initial
# I2: 2*c2 + c3 = 2*I2_initial
# Compute initial values
# RealProp (0): c1=1,c2=0,c3=2 -> I1=1, I2=1
# Southco (1): c1=1,c2=1,c3=0 -> I1=1.5, I2=1
# Trustcorp (2): c1=0,c2=3,c3=0 -> I1=1.5, I2=3
# Add invariants
# RealProp
c1_0 = count_expr(0,1)
c2_0 = count_expr(0,2)
c3_0 = count_expr(0,3)
solver.add(2*c1_0 + c2_0 == 2)   # 2*I1=2
solver.add(2*c2_0 + c3_0 == 2)   # 2*I2=2
# Southco
c1_1 = count_expr(1,1)
c2_1 = count_expr(1,2)
c3_1 = count_expr(1,3)
solver.add(2*c1_1 + c2_1 == 3)   # 2*I1=3
solver.add(2*c2_1 + c3_1 == 2)   # 2*I2=2
# Trustcorp
c1_2 = count_expr(2,1)
c2_2 = count_expr(2,2)
c3_2 = count_expr(2,3)
solver.add(2*c1_2 + c2_2 == 3)   # 2*I1=3
solver.add(2*c2_2 + c3_2 == 6)   # 2*I2=6

# Define option constraints
opt_constraints = {}
# A: RP owns L,M,O (all class2)
opt_constraints['A'] = And(owner['L']==0, owner['M']==0, owner['O']==0)
# B: SC owns G and M
opt_constraints['B'] = And(owner['G']==1, owner['M']==1)
# C: SC owns K,M,O
opt_constraints['C'] = And(owner['K']==1, owner['M']==1, owner['O']==1)
# D: TC owns F and Y
opt_constraints['D'] = And(owner['F']==2, owner['Y']==2)
# E: TC owns G and L
opt_constraints['E'] = And(owner['G']==2, owner['L']==2)

found_options = []
for letter, constr in [('A',opt_constraints['A']),('B',opt_constraints['B']),('C',opt_constraints['C']),('D',opt_constraints['D']),('E',opt_constraints['E'])]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')