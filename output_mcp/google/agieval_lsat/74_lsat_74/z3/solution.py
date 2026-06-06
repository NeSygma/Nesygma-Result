from z3 import *

# Assistants: 0:J, 1:K, 2:L, 3:N, 4:O, 5:R
# Slots: 0:Wed-M, 1:Wed-A, 2:Thu-M, 3:Thu-A, 4:Fri-M, 5:Fri-A
# day = slot // 2, time = slot % 2

def solve():
    solver = Solver()
    
    # Variables: slot for each assistant
    s = [Int(f's_{i}') for i in range(6)]
    for i in range(6):
        solver.add(s[i] >= 0, s[i] <= 5)
    
    # Each assistant in a different slot
    solver.add(Distinct(s))
    
    # Constraints
    # 1. K and R same day: day(K) == day(R)
    # day(i) = s[i] // 2. In Z3, use s[i] / 2 for integer division
    solver.add(s[1] / 2 == s[5] / 2)
    # 2. L and O different day
    solver.add(s[2] / 2 != s[4] / 2)
    # 3. N is afternoon: time(N) == 1
    # time(i) = s[i] % 2
    solver.add(s[3] % 2 == 1)
    # 4. J day < O day
    solver.add(s[0] / 2 < s[4] / 2)
    # 5. J and K are morning: time(J) == 0, time(K) == 0
    solver.add(s[0] % 2 == 0)
    solver.add(s[1] % 2 == 0)
    
    # Options
    # (A) Lan's session meets Wednesday morning (s[2] == 0)
    # (B) Lan's session meets Thursday afternoon (s[2] == 3)
    # (C) Nessa's session meets Friday afternoon (s[3] == 5)
    # (D) Olivia's session meets Thursday morning (s[4] == 2)
    # (E) Olivia's session meets Friday morning (s[4] == 4)
    
    options = [
        ("A", s[2] == 0),
        ("B", s[2] == 3),
        ("C", s[3] == 5),
        ("D", s[4] == 2),
        ("E", s[4] == 4)
    ]
    
    # We want to find which one is NOT possible.
    # So we check each one. If it's unsat, that's the answer.
    
    for label, constr in options:
        solver.push()
        solver.add(constr)
        res = solver.check()
        print(f"Option {label}: {res}")
        solver.pop()

solve()