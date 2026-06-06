from z3 import *

# 5 solos, 0-indexed
# Pianist: 0=Wayne, 1=Zara
# Type: 0=Modern, 1=Traditional

def solve():
    solver = Solver()
    
    P = [Int(f'P_{i}') for i in range(5)]
    T = [Int(f'T_{i}') for i in range(5)]
    
    for i in range(5):
        solver.add(P[i] >= 0, P[i] <= 1)
        solver.add(T[i] >= 0, T[i] <= 1)
        
    # 1. The third solo is a traditional piece.
    solver.add(T[2] == 1)
    
    # 2. Exactly two of the traditional pieces are performed consecutively.
    # Let C_i = (T_i == 1 and T_{i+1} == 1)
    C = [And(T[i] == 1, T[i+1] == 1) for i in range(4)]
    solver.add(Sum([If(C[i], 1, 0) for i in range(4)]) == 1)
    
    # 3. In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
    # (P[3] == 0 and T[3] == 1) or (P[3] == 1 and T[3] == 0)
    solver.add(Or(And(P[3] == 0, T[3] == 1), And(P[3] == 1, T[3] == 0)))
    
    # 4. The pianist who performs the second solo does not perform the fifth solo.
    solver.add(P[1] != P[4])
    
    # 5. No traditional piece is performed until Wayne performs at least one modern piece.
    # If T[i] == 1, then there exists j < i such that P[j] == 0 and T[j] == 0.
    for i in range(5):
        solver.add(Implies(T[i] == 1, Or([And(P[j] == 0, T[j] == 0) for j in range(i)])))
        
    # Question condition: The fifth solo is a traditional piece.
    solver.add(T[4] == 1)
    
    # Find all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {
            'P': [m.eval(P[i]).as_long() for i in range(5)],
            'T': [m.eval(T[i]).as_long() for i in range(5)]
        }
        solutions.append(sol)
        # Block this solution
        solver.add(Or([P[i] != m.eval(P[i]) for i in range(5)] + [T[i] != m.eval(T[i]) for i in range(5)]))
        
    return solutions

solutions = solve()
print(f"Total solutions: {len(solutions)}")

# For each solo, check if the pianist is completely determined
# Pianist is determined if P[i] is the same in all solutions
determined_pianists = 0
for i in range(5):
    vals = set(sol['P'][i] for sol in solutions)
    if len(vals) == 1:
        determined_pianists += 1
        print(f"Pianist {i} is determined: {list(vals)[0]}")
    else:
        print(f"Pianist {i} is NOT determined: {vals}")

print(f"Number of determined pianists: {determined_pianists}")