from z3 import *

# Witnesses: 0:F, 1:G, 2:H, 3:I, 4:J
# Days: 0:Mon, 1:Tue, 2:Wed

def solve():
    solver = Solver()
    
    # Variables: day each witness testifies
    day = [Int(f'day_{i}') for i in range(5)]
    for d in day:
        solver.add(d >= 0, d <= 2)
        
    # Condition 2: Iturbe (3) testifies on Wednesday (2)
    solver.add(day[3] == 2)
    
    # Condition 3: Exactly two witnesses testify on Tuesday (1)
    solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)
    
    # Condition 4: Hong (2) does not testify on Monday (0)
    solver.add(day[2] != 0)
    
    # Condition 5: At least one witness testifies on Monday (0)
    solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)
    
    # Condition 1: Franco (0) does not testify on the same day as Garcia (1)
    solver.add(day[0] != day[1])
    
    # Question condition: Franco (0) and Hong (2) testify on the same day
    base_cond = [day[0] == day[2]]
    
    # Options
    options = [
        ("A", day[0] == 2),
        ("B", day[1] == 0),
        ("C", day[1] == 2),
        ("D", day[2] == 1),
        ("E", Sum([If(day[i] == 2, 1, 0) for i in range(5)]) == 1)
    ]
    
    found_options = []
    for letter, opt_constr in options:
        # Check if option MUST be true:
        # (Base + Question) AND NOT(Option) should be UNSAT
        s = Solver()
        s.add(day[3] == 2)
        s.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)
        s.add(day[2] != 0)
        s.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)
        s.add(day[0] != day[1])
        s.add(day[0] == day[2])
        s.add(Not(opt_constr))
        
        if s.check() == unsat:
            found_options.append(letter)
            
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()