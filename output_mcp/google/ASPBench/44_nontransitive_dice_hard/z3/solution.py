from z3 import *

def solve():
    solver = Solver()
    
    # 1. Dice variables
    A = [Int(f'A_{i}') for i in range(4)]
    B = [Int(f'B_{i}') for i in range(4)]
    C = [Int(f'C_{i}') for i in range(4)]
    D = [Int(f'D_{i}') for i in range(4)]
    
    all_dice = [A, B, C, D]
    
    # 2. Value range and sorting
    for die in all_dice:
        for face in die:
            solver.add(face >= 1, face <= 8)
        for i in range(3):
            solver.add(die[i] <= die[i+1])
            
    # 3. Equal sum
    S = Int('S')
    for die in all_dice:
        solver.add(Sum(die) == S)
        
    # 4. Nontransitive cycle
    def count_wins(die1, die2):
        return Sum([If(die1[i] > die2[j], 1, 0) for i in range(4) for j in range(4)])
    
    solver.add(count_wins(A, B) > 8)
    solver.add(count_wins(B, C) > 8)
    solver.add(count_wins(C, D) > 8)
    solver.add(count_wins(D, A) > 8)
    
    # 5. Unique value sets
    # is_in_die[die_idx][val_idx] is true if val_idx+1 is in die_idx
    is_in_die = [[Bool(f'in_{d}_{v}') for v in range(1, 9)] for d in range(4)]
    
    for d_idx in range(4):
        for v in range(1, 9):
            solver.add(is_in_die[d_idx][v-1] == Or([all_dice[d_idx][i] == v for i in range(4)]))
            
    # Distinct sets
    for i in range(4):
        for j in range(i + 1, 4):
            # Sets are distinct if there exists at least one value v such that v is in one but not the other
            solver.add(Or([is_in_die[i][v-1] != is_in_die[j][v-1] for v in range(1, 9)]))
            
    # 6. Solve
    if solver.check() == sat:
        m = solver.model()
        print("STATUS: sat")
        res = {}
        for name, die in zip(['A', 'B', 'C', 'D'], all_dice):
            res[name] = [m.eval(f).as_long() for f in die]
            print(f"{name}: {res[name]}")
        
        print(f"common_sum: {m.eval(S)}")
        
        def get_wins(d1, d2):
            count = 0
            d1_vals = [m.eval(f).as_long() for f in d1]
            d2_vals = [m.eval(f).as_long() for f in d2]
            for v1 in d1_vals:
                for v2 in d2_vals:
                    if v1 > v2:
                        count += 1
            return count
            
        print(f"win_counts: A_beats_B={get_wins(A, B)}, B_beats_C={get_wins(B, C)}, C_beats_D={get_wins(C, D)}, D_beats_A={get_wins(D, A)}")
    else:
        print("STATUS: unsat")

solve()