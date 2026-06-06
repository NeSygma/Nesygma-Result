from z3 import *

pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_T = Int('pos_T')
pos_W = Int('pos_W')
pos_Y = Int('pos_Y')
pos_Z = Int('pos_Z')

base_constraints = [
    Distinct([pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]),
    pos_K >= 1, pos_K <= 6,
    pos_L >= 1, pos_L <= 6,
    pos_T >= 1, pos_T <= 6,
    pos_W >= 1, pos_W <= 6,
    pos_Y >= 1, pos_Y <= 6,
    pos_Z >= 1, pos_Z <= 6,
    pos_K != 4,
    pos_L != 4,
    Or(pos_K == 5, pos_L == 5),
    pos_K < pos_T,
    pos_Z < pos_Y,
]

original_condition = [
    pos_W < pos_K,
    pos_W < pos_L,
]

s = Solver()
s.add(base_constraints)
s.add(original_condition)
print("Checking base + original...")
res = s.check()
print(res)
if res == sat:
    m = s.model()
    print("Model:")
    for v in [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]:
        print(f"{v} = {m[v]}")
else:
    print("Unsatisfiable")