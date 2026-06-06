from z3 import *

# Riders: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Bikes: 0:F, 1:G, 2:H, 3:J

def solve():
    solver = Solver()
    
    # day1[rider] = bike
    day1 = [Int(f'day1_{r}') for r in range(4)]
    # day2[rider] = bike
    day2 = [Int(f'day2_{r}') for r in range(4)]
    
    # Domains
    for r in range(4):
        solver.add(day1[r] >= 0, day1[r] <= 3)
        solver.add(day2[r] >= 0, day2[r] <= 3)
        
    # All bikes tested each day
    solver.add(Distinct(day1))
    solver.add(Distinct(day2))
    
    # Each rider tests a different bike on day 2
    for r in range(4):
        solver.add(day1[r] != day2[r])
        
    # Reynaldo (0) cannot test F (0)
    solver.add(day1[0] != 0)
    solver.add(day2[0] != 0)
    
    # Yuki (3) cannot test J (3)
    solver.add(day1[3] != 3)
    solver.add(day2[3] != 3)
    
    # Theresa (2) must test H (2)
    solver.add(Or(day1[2] == 2, day2[2] == 2))
    
    # Yuki's Day 1 bike is Seamus's Day 2 bike
    solver.add(day2[1] == day1[3])
    
    # Define options
    # F: (Rider1, Rider2), G: (Rider1, Rider2), H: (Rider1, Rider2), J: (Rider1, Rider2)
    # Rider mapping: R=0, S=1, T=2, Y=3
    # Bike mapping: F=0, G=1, H=2, J=3
    
    # Option A: F: S, R; G: Y, S; H: T, Y; J: R, T
    # day1[1]=0, day2[0]=0; day1[3]=1, day2[1]=1; day1[2]=2, day2[3]=2; day1[0]=3, day2[2]=3
    opt_a = And(day1[1]==0, day2[0]==0, day1[3]==1, day2[1]==1, day1[2]==2, day2[3]==2, day1[0]==3, day2[2]==3)
    
    # Option B: F: S, Y; G: R, T; H: Y, S; J: T, R
    # day1[1]=0, day2[3]=0; day1[0]=1, day2[2]=1; day1[3]=2, day2[1]=2; day1[2]=3, day2[0]=3
    opt_b = And(day1[1]==0, day2[3]==0, day1[0]==1, day2[2]==1, day1[3]==2, day2[1]==2, day1[2]==3, day2[0]==3)
    
    # Option C: F: Y, S; G: S, R; H: T, Y; J: R, T
    # day1[3]=0, day2[1]=0; day1[1]=1, day2[0]=1; day1[2]=2, day2[3]=2; day1[0]=3, day2[2]=3
    opt_c = And(day1[3]==0, day2[1]==0, day1[1]==1, day2[0]==1, day1[2]==2, day2[3]==2, day1[0]==3, day2[2]==3)
    
    # Option D: F: Y, S; G: T, R; H: R, T; J: S, Y
    # day1[3]=0, day2[1]=0; day1[2]=1, day2[0]=1; day1[0]=2, day2[2]=2; day1[1]=3, day2[3]=3
    opt_d = And(day1[3]==0, day2[1]==0, day1[2]==1, day2[0]==1, day1[0]==2, day2[2]==2, day1[1]==3, day2[3]==3)
    
    # Option E: F: Y, T; G: S, Y; H: T, R; J: R, S
    # day1[3]=0, day2[2]=0; day1[1]=1, day2[3]=1; day1[2]=2, day2[0]=2; day1[0]=3, day2[1]=3
    opt_e = And(day1[3]==0, day2[2]==0, day1[1]==1, day2[3]==1, day1[2]==2, day2[0]==2, day1[0]==3, day2[1]==3)
    
    options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
    
    found = []
    for name, constr in options:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            found.append(name)
        solver.pop()
        
    if len(found) == 1:
        print("STATUS: sat")
        print(f"answer:{found[0]}")
    elif len(found) > 1:
        print("STATUS: unsat")
        print(f"Multiple options: {found}")
    else:
        print("STATUS: unsat")
        print("No options found")

solve()