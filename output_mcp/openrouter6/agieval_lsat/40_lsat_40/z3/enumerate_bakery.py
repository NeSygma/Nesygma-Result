from itertools import product

days = [0,1,3,4]  # Mon, Tue, Thu, Fri
all_vars = ['O1','O2','O3','P1','P2','P3','S1','S2','S3']

def check_constraints(assign):
    # assign is a tuple of 9 days
    O1,O2,O3,P1,P2,P3,S1,S2,S3 = assign
    # No two batches of same kind on same day
    if O1 == O2 or O1 == O3 or O2 == O3: return False
    if P1 == P2 or P1 == P3 or P2 == P3: return False
    if S1 == S2 or S1 == S3 or S2 == S3: return False
    # At least one batch on Monday
    if all(d != 0 for d in assign): return False
    # O2 == P1
    if O2 != P1: return False
    # S2 == Thu (3)
    if S2 != 3: return False
    return True

def count_batches_on_day(assign, day):
    return sum(1 for d in assign if d == day)

solutions = []
for assign in product(days, repeat=9):
    if check_constraints(assign):
        solutions.append(assign)

print(f"Total solutions: {len(solutions)}")
if len(solutions) == 0:
    print("No solutions found - modeling error")
else:
    # Check which options are always true
    always_A = all(count_batches_on_day(sol, 1) == 3 for sol in solutions)  # Tue = 1
    always_B = all(count_batches_on_day(sol, 4) == 3 for sol in solutions)  # Fri = 4
    always_C = all(count_batches_on_day(sol, 0) >= 2 for sol in solutions)  # Mon = 0
    always_D = all(count_batches_on_day(sol, 3) >= 2 for sol in solutions)  # Thu = 3
    always_E = all(count_batches_on_day(sol, 0) < count_batches_on_day(sol, 1) for sol in solutions)
    
    print(f"Option A always true: {always_A}")
    print(f"Option B always true: {always_B}")
    print(f"Option C always true: {always_C}")
    print(f"Option D always true: {always_D}")
    print(f"Option E always true: {always_E}")
    
    # Print a sample solution
    if solutions:
        sol = solutions[0]
        print("\nSample solution:")
        for var, day in zip(all_vars, sol):
            day_name = {0:'Mon',1:'Tue',3:'Thu',4:'Fri'}[day]
            print(f"{var} = {day_name}")