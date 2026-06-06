from z3 import *

# Problem parameters
n_nurses = 4
n_days = 7
n_shifts = 3  # 0: morning, 1: evening, 2: night
shift_names = ["morning", "evening", "night"]
coverage = [2, 1, 1]  # required nurses per shift

# Create solver
opt = Optimize()

# Decision variables: work[nurse][day][shift] = True if nurse works that shift
work = {}
for nurse in range(n_nurses):
    for day in range(n_days):
        for shift in range(n_shifts):
            work[(nurse, day, shift)] = Bool(f"work_{nurse}_{day}_{shift}")

# Helper functions
def get_work(nurse, day, shift):
    return work[(nurse, day, shift)]

# HARD CONSTRAINTS

# 1. Coverage requirement: exactly required nurses per shift each day
for day in range(n_days):
    for shift in range(n_shifts):
        nurses_working = [get_work(nurse, day, shift) for nurse in range(n_nurses)]
        opt.add(Sum([If(nurse_work, 1, 0) for nurse_work in nurses_working]) == coverage[shift])

# 2. Single assignment: at most one shift per nurse per day
for nurse in range(n_nurses):
    for day in range(n_days):
        shifts_worked = [get_work(nurse, day, shift) for shift in range(n_shifts)]
        opt.add(Sum([If(shift_work, 1, 0) for shift_work in shifts_worked]) <= 1)

# 3. Rest period: cannot work night shift then morning shift next day
for nurse in range(n_nurses):
    for day in range(1, n_days):  # day 1 to 6 (0-indexed)
        # If worked night on day-1, cannot work morning on day
        night_prev = get_work(nurse, day-1, 2)  # night shift
        morning_curr = get_work(nurse, day, 0)  # morning shift
        opt.add(Implies(night_prev, Not(morning_curr)))

# SOFT CONSTRAINTS (to minimize)

# 4. Max consecutive days: should not work >3 consecutive days
# Each day beyond 3 consecutive adds 1 violation
# We'll count violations per nurse
consecutive_violations = []
for nurse in range(n_nurses):
    # For each possible start of a consecutive sequence
    for start in range(n_days):
        # Count consecutive days worked from start
        consecutive_days = []
        for offset in range(n_days - start):
            day = start + offset
            # Check if nurse works any shift on this day
            works_any_shift = Or([get_work(nurse, day, shift) for shift in range(n_shifts)])
            consecutive_days.append(works_any_shift)
        
        # For each possible length > 3, add violation if all days worked
        for length in range(4, n_days - start + 1):
            # All first 'length' days must be worked
            all_worked = And(consecutive_days[:length])
            # Each day beyond 3 adds 1 violation: for length L, violations = L - 3
            violations_for_this_seq = length - 3
            # Create a variable to track if this violation applies
            v = Int(f"consec_viol_{nurse}_{start}_{length}")
            opt.add(v >= 0)
            opt.add(v <= violations_for_this_seq)
            # If all_worked, then v = violations_for_this_seq, else v = 0
            opt.add(If(all_worked, v == violations_for_this_seq, v == 0))
            consecutive_violations.append(v)

# 5. Fair distribution: each nurse should work 6-8 shifts total
# Violations = max(0, 6 - total) + max(0, total - 8)
fair_violations = []
for nurse in range(n_nurses):
    total_shifts = Sum([If(get_work(nurse, day, shift), 1, 0) 
                        for day in range(n_days) for shift in range(n_shifts)])
    
    # Below 6: violations = 6 - total
    below = Int(f"fair_below_{nurse}")
    opt.add(below >= 0)
    opt.add(below <= 6)
    opt.add(If(total_shifts < 6, below == 6 - total_shifts, below == 0))
    
    # Above 8: violations = total - 8
    above = Int(f"fair_above_{nurse}")
    opt.add(above >= 0)
    opt.add(above <= 8)  # max possible is 21 shifts, but we'll bound reasonably
    opt.add(If(total_shifts > 8, above == total_shifts - 8, above == 0))
    
    fair_violations.append(below)
    fair_violations.append(above)

# 6. Weekend coverage: at least 2 different nurses must work weekend shifts (days 6-7)
# Days 6-7 are indices 5 and 6 (0-indexed)
weekend_nurses = []
for nurse in range(n_nurses):
    # Check if nurse works any shift on weekend days
    works_weekend = Or([
        get_work(nurse, 5, shift) for shift in range(n_shifts)] + 
        [get_work(nurse, 6, shift) for shift in range(n_shifts)])
    weekend_nurses.append(works_weekend)

# Count distinct nurses working weekend
weekend_count = Sum([If(works, 1, 0) for works in weekend_nurses])
weekend_violation = Int("weekend_violation")
opt.add(weekend_violation >= 0)
opt.add(weekend_violation <= 1)  # 0 or 1 violation
opt.add(If(weekend_count < 2, weekend_violation == 1, weekend_violation == 0))

# Total violations to minimize
total_violations = Sum(consecutive_violations + fair_violations + [weekend_violation])
opt.minimize(total_violations)

# Check
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Build roster output
    roster = []
    for day in range(n_days):
        day_roster = {"morning": [], "evening": [], "night": []}
        for nurse in range(n_nurses):
            nurse_id = nurse + 1  # IDs are 1-4
            if is_true(model[get_work(nurse, day, 0)]):
                day_roster["morning"].append(nurse_id)
            if is_true(model[get_work(nurse, day, 1)]):
                day_roster["evening"].append(nurse_id)
            if is_true(model[get_work(nurse, day, 2)]):
                day_roster["night"].append(nurse_id)
        roster.append(day_roster)
    
    # Print roster
    print("roster:")
    for day_idx, day_roster in enumerate(roster):
        print(f"  Day {day_idx + 1}:")
        print(f"    Morning: {day_roster['morning']}")
        print(f"    Evening: {day_roster['evening']}")
        print(f"    Night: {day_roster['night']}")
    
    # Calculate violations from model
    violations_val = model.eval(total_violations)
    print(f"violations: {violations_val}")
    
    # Coverage met (should be true by hard constraints)
    coverage_met = True
    print(f"coverage_met: {coverage_met}")
    
    # Additional verification
    print("\nVerification:")
    # Check each nurse's total shifts
    for nurse in range(n_nurses):
        total = sum(1 for day in range(n_days) for shift in range(n_shifts) 
                   if is_true(model[get_work(nurse, day, shift)]))
        print(f"Nurse {nurse + 1}: {total} shifts")
    
    # Check consecutive days
    for nurse in range(n_nurses):
        consecutive = 0
        max_consecutive = 0
        for day in range(n_days):
            works = any(is_true(model[get_work(nurse, day, shift)]) for shift in range(n_shifts))
            if works:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0
        print(f"Nurse {nurse + 1}: max consecutive days = {max_consecutive}")
    
    # Check weekend coverage
    weekend_nurses_set = set()
    for nurse in range(n_nurses):
        for day in [5, 6]:  # days 6-7 (0-indexed)
            for shift in range(n_shifts):
                if is_true(model[get_work(nurse, day, shift)]):
                    weekend_nurses_set.add(nurse + 1)
    print(f"Weekend nurses: {sorted(weekend_nurses_set)}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")