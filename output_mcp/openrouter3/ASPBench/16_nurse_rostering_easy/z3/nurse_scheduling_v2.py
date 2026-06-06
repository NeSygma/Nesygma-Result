from z3 import *

# Problem parameters
N_NURSES = 4
N_DAYS = 7
N_SHIFTS = 3
SHIFT_NAMES = ["morning", "evening", "night"]
COVERAGE = [2, 1, 1]  # Required nurses per shift

# Create optimizer
opt = Optimize()

# Decision variables: work[nurse][day][shift] = 1 if nurse works that shift
work = {}
for n in range(N_NURSES):
    for d in range(N_DAYS):
        for s in range(N_SHIFTS):
            work[(n, d, s)] = Int(f"work_{n}_{d}_{s}")
            opt.add(Or(work[(n, d, s)] == 0, work[(n, d, s)] == 1))

# Soft constraint violation counters
violations_consecutive = Int("violations_consecutive")
violations_fair = Int("violations_fair")
violations_weekend = Int("violations_weekend")
total_violations = Int("total_violations")

# Initialize violation counters
opt.add(violations_consecutive >= 0)
opt.add(violations_fair >= 0)
opt.add(violations_weekend >= 0)

# HARD CONSTRAINTS

# 1. Coverage requirement
for d in range(N_DAYS):
    for s in range(N_SHIFTS):
        total_nurses = Sum([work[(n, d, s)] for n in range(N_NURSES)])
        opt.add(total_nurses == COVERAGE[s])

# 2. Single assignment per nurse per day
for n in range(N_NURSES):
    for d in range(N_DAYS):
        total_shifts = Sum([work[(n, d, s)] for s in range(N_SHIFTS)])
        opt.add(total_shifts <= 1)

# 3. Rest period: night shift (s=2) on day d prevents morning shift (s=0) on day d+1
for n in range(N_NURSES):
    for d in range(N_DAYS - 1):
        # If nurse works night shift on day d, cannot work morning shift on day d+1
        opt.add(Implies(work[(n, d, 2)] == 1, work[(n, d+1, 0)] == 0))

# SOFT CONSTRAINTS

# 4. Max consecutive days: no more than 3 consecutive days
# For each nurse, count consecutive days worked
for n in range(N_NURSES):
    # Track consecutive days worked
    for start in range(N_DAYS):
        # Check sequences of 4+ consecutive days
        for length in range(4, N_DAYS - start + 1):
            # All days from start to start+length-1 must be worked
            consecutive_days = []
            for d in range(start, start + length):
                # Nurse works at least one shift on day d
                day_worked = Or([work[(n, d, s)] == 1 for s in range(N_SHIFTS)])
                consecutive_days.append(day_worked)
            
            # If all days in sequence are worked, add violation
            if consecutive_days:
                opt.add(Implies(And(consecutive_days), violations_consecutive >= 1))

# 5. Fair distribution: each nurse works 6-8 shifts total
for n in range(N_NURSES):
    total_shifts_nurse = Sum([work[(n, d, s)] for d in range(N_DAYS) for s in range(N_SHIFTS)])
    # Violation if outside [6,8]
    below_6 = If(total_shifts_nurse < 6, 1, 0)
    above_8 = If(total_shifts_nurse > 8, 1, 0)
    opt.add(violations_fair >= below_6 + above_8)

# 6. Weekend coverage: at least 2 different nurses work weekend shifts (days 6-7, indices 5-6)
# Count nurses who work at least one shift on weekend
weekend_nurses = []
for n in range(N_NURSES):
    # Nurse works at least one shift on weekend
    weekend_work = Or([work[(n, d, s)] == 1 for d in [5, 6] for s in range(N_SHIFTS)])
    weekend_nurses.append(weekend_work)

# Count how many nurses work weekend
num_weekend_nurses = Sum([If(weekend_nurses[n], 1, 0) for n in range(N_NURSES)])
# Violation if fewer than 2
opt.add(violations_weekend >= If(num_weekend_nurses < 2, 1, 0))

# Total violations
opt.add(total_violations == violations_consecutive + violations_fair + violations_weekend)

# Objective: minimize total violations
opt.minimize(total_violations)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print(f"Total violations: {model[total_violations]}")
    print(f"Consecutive days violations: {model[violations_consecutive]}")
    print(f"Fair distribution violations: {model[violations_fair]}")
    print(f"Weekend coverage violations: {model[violations_weekend]}")
    print()
    
    # Print roster
    print("Roster:")
    for d in range(N_DAYS):
        print(f"Day {d+1}:")
        for s in range(N_SHIFTS):
            nurses_working = []
            for n in range(N_NURSES):
                if model[work[(n, d, s)]] == 1:
                    nurses_working.append(n+1)  # Convert to 1-based ID
            print(f"  {SHIFT_NAMES[s]}: {nurses_working}")
    
    # Check coverage met
    coverage_met = True
    for d in range(N_DAYS):
        for s in range(N_SHIFTS):
            total = sum(int(model[work[(n, d, s)]]) for n in range(N_NURSES))
            if total != COVERAGE[s]:
                coverage_met = False
                break
        if not coverage_met:
            break
    
    print(f"\nCoverage met: {coverage_met}")
    
    # Check if this matches expected optimal violations (16)
    if model[total_violations] == 16:
        print("Matches expected optimal violations: 16")
    else:
        print(f"Note: Found {model[total_violations]} violations, expected 16")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")