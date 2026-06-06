from z3 import *

def check_condition():
    solver = Solver()
    O = [Int(f'O{i}') for i in range(1, 4)]
    P = [Int(f'P{i}') for i in range(1, 4)]
    S = [Int(f'S{i}') for i in range(1, 4)]
    all_batches = O + P + S
    for b in all_batches: solver.add(b >= 0, b <= 4)
    solver.add(Distinct(O), Distinct(P), Distinct(S))
    solver.add(Or([b == 0 for b in all_batches]))
    solver.add(O[1] == P[0])
    solver.add(S[1] == 3)
    
    I = Or(O[0] == P[2], O[0] == S[2], P[0] == O[2], P[0] == S[2], S[0] == O[2], S[0] == P[2])
    
    # Check if I is always true
    solver.push()
    solver.add(Not(I))
    res = solver.check()
    print(f"Not(I) is {res}")
    solver.pop()

check_condition()