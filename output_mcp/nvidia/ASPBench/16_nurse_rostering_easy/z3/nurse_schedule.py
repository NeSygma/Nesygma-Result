from z3 import *

days = 7
nurses = range(1, 5)  # 1..4

opt = Optimize()

# Variables
m1 = [Int(f'm1_{d}') for d in range(days)]
m2 = [Int(f'm2_{d}') for d in range(days)]
e  = [Int(f'e_{d}')  for d in range(days)]
n  = [Int(f'n_{d}')  for d in range(days)]

# Domain constraints
for d in range(days):
    for var in [m1[d], m2[d], e[d], n[d]]:
        opt.add(var >= 1, var <= 4)

# AllDifferent per day
for d in range(days):
    opt.add(Distinct([m1[d], m2[d], e[d], n[d]]))

# Rest period: no night then next morning
for d in range(days-1):
    for k in nurses:
        opt.add(Or(n[d] != k, m1[d+1] != k))
        opt.add(Or(n[d] != k, m2[d+1] != k))

# Boolean worked[k][d]
w = {}
for k in nurses:
    for d in range(days):
        w[(k,d)] = Bool(f'w_{k}_{d}')
        opt.add(w[(k,d)] == Or(m1[d] == k, m2[d] == k, e[d] == k, n[d] == k))

# Soft constraints
# Fair distribution violations
for k in nurses:
    shifts = Sum([If(w[(k,d)], 1, 0) for d in range(days)])
    low_violation = (shifts < 6)
    high_violation = (shifts > 8)
    opt.add_soft(low_violation, 1)
    opt.add_soft(high_violation, 1)

# Consecutive days violations
for k in nurses:
    for d in range(3, days):
        run4 = And(w[(k,d-3)], w[(k,d-2)], w[(k,d-1)], w[(k,d)])
        opt.add_soft(Not(run4), 1)

# Weekend coverage violation (days 5 and 6)
weekend_distinct = Sum([Or(w[(k,5)], w[(k,6)]) for k in nurses])
weekend_violation = (weekend_distinct < 2)
opt.add_soft(weekend_violation, 1)

# Check and print
result = opt.check()
if result == sat:
    print('STATUS: sat')
    m = opt.model()
    # Print schedule
    for d in range(days):
        print(f'Day {d+1} morning {m[m1[d]]} {m[m2[d]]}, evening {m[e[d]]} , night {m[n[d]]}')
    # Count total violations (only consecutive day violations matter)
    total_violations = 0
    for k in nurses:
        for d in range(3, days):
            if m.eval(And(w[(k,d-3)], w[(k,d-2)], w[(k,d-1)], w[(k,d)])):
                total_violations += 1
    print('violations:', total_violations)
else:
    print('STATUS: unsat')