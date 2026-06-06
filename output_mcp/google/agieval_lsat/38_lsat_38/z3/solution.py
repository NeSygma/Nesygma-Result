from z3 import *

# Re-reading the question: "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# Wait, maybe it means: "In all valid scenarios, how many days have at most two batches?"
# No, that doesn't make sense.
# Let's re-read: "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# This usually means: "For how many days is it possible that the number of batches is <= 2?"
# My previous code found that for all 5 days, it is possible to have <= 2 batches.
# Let's re-check the constraints.
# "Exactly three batches of each kind of cookie are made each week (Monday through Friday)"
# Total batches = 3 * 3 = 9.
# Days = 5.
# Average batches per day = 9 / 5 = 1.8.
# So it is very likely that most days have 1 or 2 batches.
# Let's check if it's possible to have 3 batches on a day.
# If a day has 3 batches, then 9 - 3 = 6 batches left for 4 days.
# 6 / 4 = 1.5.
# So it is possible to have 3 batches on a day.
# Let's check if it's possible to have 4 batches on a day.
# If a day has 4 batches, then 9 - 4 = 5 batches left for 4 days.
# 5 / 4 = 1.25.
# So it is possible to have 4 batches on a day.

# Let's re-read the question again.
# "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# Maybe it means: "In every valid scenario, how many days have at most two batches?"
# Let's check if the number of days with <= 2 batches is constant across all valid scenarios.

def solve():
    solver = Solver()
    
    O = [Int(f'O_{i}') for i in range(3)]
    P = [Int(f'P_{i}') for i in range(3)]
    S = [Int(f'S_{i}') for i in range(3)]
    
    for var in O + P + S:
        solver.add(var >= 0, var <= 4)
        
    solver.add(Distinct(O))
    solver.add(Distinct(P))
    solver.add(Distinct(S))
    
    # "At least one batch of cookies is made on Monday."
    # Monday is day 0.
    # N_0 >= 1
    N_0 = Sum([If(O[i] == 0, 1, 0) for i in range(3)] + 
              [If(P[i] == 0, 1, 0) for i in range(3)] + 
              [If(S[i] == 0, 1, 0) for i in range(3)])
    solver.add(N_0 >= 1)
    
    solver.add(O[1] == P[0])
    solver.add(S[1] == 3) # Thursday is day 3
    
    # Let's find all possible counts of days with <= 2 batches.
    possible_counts = set()
    
    # We need to iterate over all solutions or at least check if the count is constant.
    # Since the number of solutions might be large, let's just find all possible values for the count.
    
    # Actually, let's just find one solution and see how many days have <= 2 batches.
    # Then try to find another solution with a different count.
    
    count_var = Int('count_var')
    
    # N_d is the number of batches on day d
    N = [Sum([If(O[i] == d, 1, 0) for i in range(3)] + 
             [If(P[i] == d, 1, 0) for i in range(3)] + 
             [If(S[i] == d, 1, 0) for i in range(3)]) for d in range(5)]
    
    # count_var = number of days d such that N[d] <= 2
    solver.add(count_var == Sum([If(N[d] <= 2, 1, 0) for d in range(5)]))
    
    while solver.check() == sat:
        m = solver.model()
        c = m[count_var].as_long()
        possible_counts.add(c)
        solver.add(count_var != c)
        
    print(f"Possible counts: {possible_counts}")

solve()