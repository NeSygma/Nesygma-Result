from z3 import *

# Problem data
jobs = {
    1: [(3, 1), (2, 2), (4, 3)],  # (duration, machine)
    2: [(2, 2), (5, 1), (1, 3)],
    3: [(4, 3), (1, 1), (3, 2)]
}

# Create solver
opt = Optimize()

# Variables: start times for each operation
start = {}
end = {}
for j, ops in jobs.items():
    for o, (dur, mach) in enumerate(ops, start=1):
        s = Int(f's_{j}_{o}')
        e = Int(f'e_{j}_{o}')
        start[(j, o)] = s
        end[(j, o)] = e
        # Non-negative start
        opt.add(s >= 0)
        # End time equals start + duration
        opt.add(e == s + dur)

# Precedence constraints within each job
for j, ops in jobs.items():
    for o in range(1, len(ops)):
        opt.add(end[(j, o)] <= start[(j, o+1)])

# Machine non-overlap constraints
# Gather operations per machine
ops_per_machine = {}
for j, ops in jobs.items():
    for o, (dur, mach) in enumerate(ops, start=1):
        ops_per_machine.setdefault(mach, []).append((j, o))

for mach, op_list in ops_per_machine.items():
    n = len(op_list)
    for i in range(n):
        for j in range(i+1, n):
            j1, o1 = op_list[i]
            j2, o2 = op_list[j]
            e1 = end[(j1, o1)]
            s1 = start[(j1, o1)]
            e2 = end[(j2, o2)]
            s2 = start[(j2, o2)]
            # Non-overlap: either e1 <= s2 or e2 <= s1
            opt.add(Or(e1 <= s2, e2 <= s1))

# Makespan variable
M = Int('makespan')
opt.add(M >= 0)
for key in end:
    opt.add(M >= end[key])

# Objective: minimize makespan
opt.minimize(M)

# Solve
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("feasible: True")
    makespan_val = model[M].as_long()
    print("makespan:", makespan_val)
    print("schedule:")
    # Print schedule entries sorted by job then operation
    for j in sorted(jobs.keys()):
        for o, (dur, mach) in enumerate(jobs[j], start=1):
            s_val = model[start[(j, o)]].as_long()
            print(f"job {j} operation {o} machine {mach} start {s_val} duration {dur}")
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE assumed ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")