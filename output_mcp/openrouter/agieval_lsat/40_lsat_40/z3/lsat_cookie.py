from z3 import *

# Days: 0 Mon,1 Tue,2 Wed,3 Thu,4 Fri
# Variables: O1,O2,O3, P1,P2,P3, S1,S2,S3
O = [Int(f'O{i}') for i in range(1,4)]
P = [Int(f'P{i}') for i in range(1,4)]
S = [Int(f'S{i}') for i in range(1,4)]

solver = Solver()
# domain 0-4
for v in O+P+S:
    solver.add(v >= 0, v <= 4)
# No two batches of same kind same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))
# At least one batch on Monday (day 0)
solver.add(Or([v == 0 for v in O+P+S]))
# O2 same day as P1
solver.add(O[1] == P[0])
# S2 is Thursday (3)
solver.add(S[1] == 3)
# No batch on Wednesday (2)
for v in O+P+S:
    solver.add(v != 2)

# Enumerate all models
models = []
while solver.check() == sat:
    m = solver.model()
    models.append({str(d): m[d].as_long() for d in O+P+S})
    # block this model
    block = []
    for d in O+P+S:
        block.append(d != m[d])
    solver.add(Or(block))

print('Total models:', len(models))
# evaluate options
def count_day(day):
    cnt = 0
    for model in models:
        cnt_day = sum(1 for v in model.values() if v == day)
        # store per model
        pass
    # not needed

# compute which options always hold
always = {'A':True,'B':True,'C':True,'D':True,'E':True}
for model in models:
    # counts per day
    cnt = {0:0,1:0,3:0,4:0}
    for v in model.values():
        cnt[v] = cnt.get(v,0)+1
    # Option A: exactly 3 on Tuesday (day1)
    if cnt[1] != 3:
        always['A'] = False
    # B: exactly 3 on Friday (day4)
    if cnt[4] != 3:
        always['B'] = False
    # C: at least 2 on Monday (day0)
    if cnt[0] < 2:
        always['C'] = False
    # D: at least 2 on Thursday (day3)
    if cnt[3] < 2:
        always['D'] = False
    # E: fewer on Monday than Tuesday
    if not (cnt[0] < cnt[1]):
        always['E'] = False
print('Always true options:', [k for k,v in always.items() if v])