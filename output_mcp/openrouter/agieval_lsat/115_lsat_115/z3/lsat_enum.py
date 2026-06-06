from z3 import *

# Articles
articles = ['G','H','J','Q','R','S','Y']
# Topics mapping
finance = {'G','H','J'}
nutrition = {'Q','R','S'}
# Y is wildlife

# Position variables 1..7
pos = {a: Int(f'pos_{a}') for a in articles}
solver = Solver()
# domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
# all different
solver.add(Distinct([pos[a] for a in articles]))
# consecutive topic constraint
for i in range(1,7):
    # find which article is at position i and i+1
    # Use Or over possibilities
    # For each pair of articles a,b, if pos[a]==i and pos[b]==i+1 then topics must differ
    # We'll encode as: for any a,b with same topic, cannot be consecutive
    for a in articles:
        for b in articles:
            if a==b: continue
            # same topic?
            same = (a in finance and b in finance) or (a in nutrition and b in nutrition)
            if same:
                solver.add(Not(And(pos[a]==i, pos[b]==i+1)))
# S earlier than Q only if Q is third: (pos[S] < pos[Q]) -> (pos[Q]==3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
solver.add(pos['S'] < pos['Y'])
# J earlier than G, G earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Function to count solutions (up to a limit)
def all_solutions(limit=1000):
    sols = []
    s = Solver()
    s.append(solver.assertions())
    while s.check() == sat and len(sols) < limit:
        m = s.model()
        sol = {a: m[pos[a]].as_long() for a in articles}
        sols.append(sol)
        # block this solution
        s.add(Or([pos[a] != m[pos[a]] for a in articles]))
    return sols

solutions = all_solutions(2000)
print('Total solutions:', len(solutions))
# Determine uniqueness per option
options = {
    'A': lambda sol: sol['H'] == 4,
    'B': lambda sol: sol['H'] == 6,
    'C': lambda sol: sol['R'] == 4,
    'D': lambda sol: sol['R'] == 7,
    'E': lambda sol: sol['Y'] == 5,
}
unique_options = []
for opt, pred in options.items():
    filtered = [sol for sol in solutions if pred(sol)]
    if len(filtered) == 1:
        unique_options.append(opt)
    # print counts
    print(f'Option {opt}: {len(filtered)} solutions')
print('Unique options:', unique_options)