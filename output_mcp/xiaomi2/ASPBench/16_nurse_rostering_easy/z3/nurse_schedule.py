from z3 import *

opt = Optimize()
opt.set("priority", "lex")  # Lexicographic optimization

NURSES = 4
DAYS = 7
SHIFTS = 3  # 0=morning, 1=evening, 2=night

# ============================================================
# Decision Variables
# ============================================================
# assign[n][d][s] = True if nurse n (0..3) works shift s on day d (0..6)
assign = [[[Bool(f'assign_{n}_{d}_{s}') for s in range(SHIFTS)] for d in range(DAYS)] for n in range(NURSES)]

# works[n][d] = True if nurse n works ANY shift on day d
works = [[Or(assign[n][d][0], assign[n][d][1], assign[n][d][2]) 
          for d in range(DAYS)] for n in range(NURSES)]

# ============================================================
# Hard Constraint 1: Coverage Requirements
# ============================================================
for d in range(DAYS):
    # Morning shift: exactly 2 nurses
    opt.add(Sum([If(assign[n][d][0], 1, 0) for n in range(NURSES)]) == 2)
    # Evening shift: exactly 1 nurse
    opt.add(Sum([If(assign[n][d][1], 1, 0) for n in range(NURSES)]) == 1)
    # Night shift: exactly 1 nurse
    opt.add(Sum([If(assign[n][d][2], 1, 0) for n in range(NURSES)]) == 1)

# ============================================================
# Hard Constraint 2: Single Assignment (at most 1 shift per day)
# ============================================================
for n in range(NURSES):
    for d in range(DAYS):
        opt.add(Sum([If(assign[n][d][s], 1, 0) for s in range(SHIFTS)]) <= 1)

# ============================================================
# Hard Constraint 3: Rest Period (no night→morning next day)
# ============================================================
for n in range(NURSES):
    for d in range(DAYS - 1):
        # If nurse works night (shift 2) on day d, cannot work morning (shift 0) on day d+1
        opt.add(Implies(assign[n][d][2], Not(assign[n][d+1][0])))

# ============================================================
# Soft Constraint 4: Max Consecutive Days (penalty for >3 consecutive)
# ============================================================
# For each nurse, for each window of 4 consecutive days, if all worked → 1 violation
# This correctly counts: streak of length L → L-3 violations
consec_violations = []
for n in range(NURSES):
    for d in range(3, DAYS):  # d = 3,4,5,6 (0-indexed)
        window = And(works[n][d-3], works[n][d-2], works[n][d-1], works[n][d])
        consec_violations.append(If(window, 1, 0))

# ============================================================
# Soft Constraint 5: Fair Distribution (6-8 shifts per nurse)
# ============================================================
total_shifts = [Sum([If(works[n][d], 1, 0) for d in range(DAYS)]) for n in range(NURSES)]

fair_violations = []
for n in range(NURSES):
    # Violations for working fewer than 6 shifts
    fair_violations.append(If(total_shifts[n] < 6, 6 - total_shifts[n], 0))
    # Violations for working more than 8 shifts
    fair_violations.append(If(total_shifts[n] > 8, total_shifts[n] - 8, 0))

# ============================================================
# Soft Constraint 6: Weekend Coverage (at least 2 nurses on days 6-7)
# ============================================================
# Days 5,6 (0-indexed) = days 6,7 (1-indexed)
weekend_works = [Or(works[n][5], works[n][6]) for n in range(NURSES)]
weekend_count = Sum([If(weekend_works[n], 1, 0) for n in range(NURSES)])
weekend_violations = [If(weekend_count < 2, 1, 0)]

# ============================================================
# Objective: Minimize Total Violations
# ============================================================
all_violations = consec_violations + fair_violations + weekend_violations
total_violations = Sum(all_violations)

opt.minimize(total_violations)

# ============================================================
# Solve
# ============================================================
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Build and print roster
    shift_names = ["morning", "evening", "night"]
    roster = []
    for d in range(DAYS):
        day_shifts = []
        for s in range(SHIFTS):
            nurses_on = [n + 1 for n in range(NURSES) if is_true(m.evaluate(assign[n][d][s]))]
            day_shifts.append(nurses_on)
        roster.append(day_shifts)
    
    print("\n=== ROSTER ===")
    for d in range(DAYS):
        print(f"Day {d+1}:")
        for s in range(SHIFTS):
            print(f"  {shift_names[s]}: {roster[d][s]}")
    
    # Compute and print violations breakdown
    consec_v = sum(is_true(m.evaluate(c)) for c in consec_violations)
    fair_v = sum(is_true(m.evaluate(f)) for f in fair_violations)
    weekend_v = is_true(m.evaluate(weekend_violations[0]))
    
    total_v = m.evaluate(total_violations)
    
    print(f"\n=== VIOLATIONS ===")
    print(f"Consecutive day violations: {consec_v}")
    print(f"Fair distribution violations: {fair_v}")
    print(f"Weekend coverage violations: {1 if weekend_v else 0}")
    print(f"Total violations: {total_v}")
    
    # Per-nurse details
    print(f"\n=== PER-NURSE DETAILS ===")
    for n in range(NURSES):
        ts = m.evaluate(total_shifts[n])
        print(f"Nurse {n+1}: {ts} shifts total")
    
    # Coverage check
    print(f"\ncoverage_met: True")
    
    # Verify night→morning constraint
    print(f"\n=== REST PERIOD CHECK ===")
    rest_ok = True
    for n in range(NURSES):
        for d in range(DAYS - 1):
            if is_true(m.evaluate(assign[n][d][2])) and is_true(m.evaluate(assign[n][d+1][0])):
                rest_ok = False
                print(f"  VIOLATION: Nurse {n+1} night day {d+1} -> morning day {d+2}")
    if rest_ok:
        print("  All rest periods respected.")

elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")
    print(f"Solver returned: {result}")