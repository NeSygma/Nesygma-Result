from z3 import *

BENCHMARK_MODE = True

gates = ['h_q0', 'h_q1', 'x_q2', 'cnot_q0_q1', 'cnot_q1_q2', 'cnot_q0_q3']

conflicts = [
    ('h_q0', 'cnot_q0_q1'),
    ('h_q0', 'cnot_q0_q3'),
    ('h_q1', 'cnot_q0_q1'),
    ('h_q1', 'cnot_q1_q2'),
    ('x_q2', 'cnot_q1_q2'),
    ('cnot_q0_q1', 'cnot_q1_q2'),
    ('cnot_q0_q1', 'cnot_q0_q3')
]

opt = Optimize()

t = {}
for g in gates:
    t[g] = Int(f't_{g}')
    opt.add(t[g] >= 1, t[g] <= 6)

for (g1, g2) in conflicts:
    opt.add(t[g1] != t[g2])

D = Int('D')
for g in gates:
    opt.add(D >= t[g])

opt.minimize(D)

result = opt.check()

if result == sat:
    model = opt.model()
    print('STATUS: sat')
    D_val = model[D].as_long()
    print(f'circuit_depth = {D_val}')
    schedule = {}
    for g in gates:
        ti = model[t[g]].as_long()
        schedule.setdefault(ti, []).append(g)
    for ti in range(1, D_val+1):
        gates_at_ti = schedule.get(ti, [])
        print(f'time = {ti}, gates = {gates_at_ti}')
elif result == unsat:
    print('STATUS: unsat')
    if BENCHMARK_MODE:
        print('RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)')
else:
    print('STATUS: unknown')