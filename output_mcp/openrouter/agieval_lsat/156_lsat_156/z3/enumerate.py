from z3 import *

S, T, N = 0,1,2
photogs = ['Frost','Gonzalez','Heideck','Knutson','Lai','Mays']
vars = {p: Int(p) for p in photogs}
solver = Solver()
for v in vars.values():
    solver.add(Or(v==S, v==T, v==N))
# constraints
cnt_S = Sum([If(v==S,1,0) for v in vars.values()])
cnt_T = Sum([If(v==T,1,0) for v in vars.values()])
solver.add(cnt_S>=2, cnt_T>=2)
solver.add(vars['Frost']==vars['Heideck'])
solver.add(vars['Frost']!=N)
solver.add(Implies(And(vars['Lai']!=N, vars['Mays']!=N), vars['Lai']!=vars['Mays']))
solver.add(Implies(vars['Gonzalez']==S, vars['Lai']==T))
solver.add(Implies(vars['Knutson']!=T, And(vars['Heideck']==T, vars['Mays']==T)))
# assumption
solver.add(vars['Heideck']==vars['Lai'])
solver.add(vars['Heideck']!=N)

options = {
    'A': lambda m: m[vars['Frost']].as_long()==T,
    'B': lambda m: m[vars['Gonzalez']].as_long()==S,
    'C': lambda m: m[vars['Gonzalez']].as_long()==N,
    'D': lambda m: m[vars['Knutson']].as_long()==T,
    'E': lambda m: m[vars['Lai']].as_long()==T,
}

all_models = []
while solver.check() == sat:
    m = solver.model()
    all_models.append({p: m[vars[p]].as_long() for p in photogs})
    # block
    solver.add(Or([vars[p] != m[vars[p]] for p in photogs]))

print('total models', len(all_models))
# compute which options always true
always = []
for opt,func in options.items():
    if all(func(m) for m in all_models):
        always.append(opt)
print('always true options', always)
# also which options sometimes true
sometimes = []
for opt,func in options.items():
    if any(func(m) for m in all_models):
        sometimes.append(opt)
print('sometimes true', sometimes)