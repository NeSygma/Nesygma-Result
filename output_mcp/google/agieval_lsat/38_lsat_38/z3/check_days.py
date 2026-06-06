from z3 import *

# Re-reading the question: "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# This phrasing is ambiguous.
# "How many of the days... are such that at most two batches of cookies could be made on that day?"
# This could mean:
# 1. For which days d is it possible that N[d] <= 2?
# 2. How many such days are there? (If it's a fixed number)
# 3. Maybe it means: "For how many days is it *necessarily* true that at most two batches are made?"
# 4. Maybe it means: "For how many days is it *possible* that at most two batches are made?" (But this would be a set of days, not a number)

# Let's re-read: "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# This sounds like: "Count the number of days d such that it is possible that N[d] <= 2."
# But if it's possible for all 5 days, the answer would be 5.
# Let's check if it's possible for all 5 days to have <= 2 batches.
# My previous code said the count of days with <= 2 batches can be 2, 3, 4, or 5.
# This means in some scenarios, 5 days have <= 2 batches.
# In some scenarios, 4 days have <= 2 batches.
# In some scenarios, 3 days have <= 2 batches.
# In some scenarios, 2 days have <= 2 batches.

# Wait, if the question is "How many of the days... are such that at most two batches of cookies could be made on that day?",
# it might mean: "For how many days d is it possible that N[d] <= 2?"
# Let's check for each day d, is it possible that N[d] <= 2?

def check_days():
    solver = Solver()
    O = [Int(f'O_{i}') for i in range(3)]
    P = [Int(f'P_{i}') for i in range(3)]
    S = [Int(f'S_{i}') for i in range(3)]
    for var in O + P + S:
        solver.add(var >= 0, var <= 4)
    solver.add(Distinct(O))
    solver.add(Distinct(P))
    solver.add(Distinct(S))
    N_0 = Sum([If(O[i] == 0, 1, 0) for i in range(3)] + 
              [If(P[i] == 0, 1, 0) for i in range(3)] + 
              [If(S[i] == 0, 1, 0) for i in range(3)])
    solver.add(N_0 >= 1)
    solver.add(O[1] == P[0])
    solver.add(S[1] == 3)
    
    possible_days = []
    for d in range(5):
        solver.push()
        # N[d] is the number of batches on day d
        N_d = Sum([If(O[i] == d, 1, 0) for i in range(3)] + 
                  [If(P[i] == d, 1, 0) for i in range(3)] + 
                  [If(S[i] == d, 1, 0) for i in range(3)])
        solver.add(N_d <= 2)
        if solver.check() == sat:
            possible_days.append(d)
        solver.pop()
    print(f"Days where it's possible to have <= 2 batches: {possible_days}")

check_days()