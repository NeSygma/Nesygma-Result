from z3 import *

solver = Solver()
books = ['F','G','H','I','K','L','M','O']
vars = {b: Int(b) for b in books}
for v in vars.values():
    solver.add(v >= 1, v <= 3)
# at least two per shelf
for s in [1,2,3]:
    solver.add(Sum([If(v == s, 1, 0) for v in vars.values()]) >= 2)
# more bottom than top
count_bottom = Sum([If(v == 3, 1, 0) for v in vars.values()])
count_top = Sum([If(v == 1, 1, 0) for v in vars.values()])
solver.add(count_bottom > count_top)
# specific constraints
solver.add(vars['I'] == 2)
solver.add(vars['K'] < vars['F'])
solver.add(vars['O'] < vars['L'])
solver.add(vars['F'] == vars['M'])

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {b: m[vars[b]].as_long() for b in books}
    solutions.append(sol)
    # block
    solver.add(Or([vars[b] != m[vars[b]] for b in books]))

print('total solutions', len(solutions))
# evaluate options
always = {opt: True for opt in ['A','B','C','D','E']}
for sol in solutions:
    # A: O higher than M => O < M
    if not (sol['O'] < sol['M']):
        always['A'] = False
    # B: K higher than G => K < G
    if not (sol['K'] < sol['G']):
        always['B'] = False
    # C: I higher than F => I < F
    if not (sol['I'] < sol['F']):
        always['C'] = False
    # D: G higher than O => G < O
    if not (sol['G'] < sol['O']):
        always['D'] = False
    # E: F higher than L => F < L
    if not (sol['F'] < sol['L']):
        always['E'] = False
print('always true:', always)