from z3 import *

# Define solver
solver = Solver()

# Number of positions
N = 6
# Types: 0=A, 1=B, 2=C
positions = [Int(f'p{i}') for i in range(N)]
for p in positions:
    solver.add(p >= 0, p <= 2)

# Count constraints
cntA = Sum([If(p == 0, 1, 0) for p in positions])
cntB = Sum([If(p == 1, 1, 0) for p in positions])
cntC = Sum([If(p == 2, 1, 0) for p in positions])
solver.add(cntA == 1)
solver.add(cntB == 2)
solver.add(cntC == 3)

# Option 1 (sunroof): types A(0) or C(2)
# sliding window of size 3, at most 2
for i in range(N-3+1):
    window = positions[i:i+3]
    opt1_cnt = Sum([If(p == 0, 1, 0) + If(p == 2, 1, 0) for p in window])
    solver.add(opt1_cnt <= 2)

# Option 2 (leather): type A only, window size 2, at most 1
for i in range(N-2+1):
    window = positions[i:i+2]
    opt2_cnt = Sum([If(p == 0, 1, 0) for p in window])
    solver.add(opt2_cnt <= 1)

# Option 3 (GPS): type B only, window size 2, at most 1
for i in range(N-2+1):
    window = positions[i:i+2]
    opt3_cnt = Sum([If(p == 1, 1, 0) for p in window])
    solver.add(opt3_cnt <= 1)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    seq = [m.eval(p).as_long() for p in positions]
    # map to letters
    mapping = {0:'A',1:'B',2:'C'}
    seq_str = [mapping[v] for v in seq]
    print('STATUS: sat')
    print('sequence =', seq_str)
else:
    print('STATUS: unsat')