from z3 import *

solver = Solver()
# variables
pos = {b: Int(b) for b in ['oyst','pet','rail','sand','tern']}
for v in pos.values():
    solver.add(v >=1, v <=5)
solver.add(Distinct(list(pos.values())))
# locations per position
G = [Bool(f'G{i}') for i in range(1,6)]  # G1..G5
# constraints
solver.add(G[0] == True)  # first Gladwyn
solver.add(G[3] == False) # fourth Howard
solver.add(Sum([If(g,1,0) for g in G]) == 3)
# sandpipers location Howard
for i in range(1,6):
    solver.add(Implies(pos['sand']==i, G[i-1] == False))
# sand earlier than oyst
solver.add(pos['sand'] < pos['oyst'])
# petrels in Gladwyn
for i in range(1,6):
    solver.add(Implies(pos['pet']==i, G[i-1] == True))
# terns earlier than petrels
solver.add(pos['tern'] < pos['pet'])

# options definitions as functions of G list
opt = {
    'A': And(G[0]==True, G[1]==True),
    'B': And(G[1]==False, G[2]==False),
    'C': And(G[1]==True, G[4]==True),
    'D': And(G[2]==False, G[3]==False),
    'E': And(G[2]==True, G[4]==True)
}

solutions = []
while solver.check() == sat:
    m = solver.model()
    # record G values
    gvals = [is_true(m.eval(g, model_completion=True)) for g in G]
    # record positions mapping bird->pos
    pvals = {b: m.eval(v).as_long() for b,v in pos.items()}
    solutions.append((gvals, pvals))
    # block this solution
    block = []
    for g,val in zip(G,gvals):
        block.append(g == val)
    for b,v in pos.items():
        block.append(v == pvals[b])
    solver.add(Not(And(block)))

print('total solutions', len(solutions))
# evaluate each option across solutions
for letter, expr in opt.items():
    any_true = False
    for gvals,_ in solutions:
        # evaluate expr manually using gvals
        # create a temporary solver to evaluate? easier: substitute
        # We'll just evaluate using python logic
        # expr uses Bool objects; we can evaluate by checking model
        # Instead, we can evaluate by building a small solver with constraints G[i]==gvals[i]
        s = Solver()
        for i,g in enumerate(G):
            s.add(g == gvals[i])
        s.add(expr)
        if s.check() == sat:
            any_true = True
            break
    print(letter, any_true)