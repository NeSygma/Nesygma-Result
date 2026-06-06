from z3 import *

solver = Solver()

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
n = 8
gives = [Bool(f'gives_{i}') for i in range(n)]
day = [Int(f'day_{i}') for i in range(n)]
time = [Int(f'time_{i}') for i in range(n)]

# Exactly 6 give reports
solver.add(Sum([If(gives[i], 1, 0) for i in range(n)]) == 6)

# Domain constraints for those who give
for i in range(n):
    solver.add(Implies(gives[i], And(day[i] >= 0, day[i] <= 2)))
    solver.add(Implies(gives[i], And(time[i] >= 0, time[i] <= 1)))

# Exactly 2 reports per day (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([If(And(gives[i], day[i] == d), 1, 0) for i in range(n)]) == 2)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Constraint 1: George can only give on Tuesday (day=1)
solver.add(Implies(gives[0], day[0] == 1))

# Constraint 2: Olivia and Robert cannot give afternoon reports
solver.add(Implies(gives[6], time[6] == 0))  # Olivia
solver.add(Implies(gives[7], time[7] == 0))  # Robert

# Constraint 3: If Nina gives on day d (0=Mon, 1=Tue), then on day d+1 Helen and Irving both give reports
# (unless Nina gives on Wednesday (day=2), which has no next-day condition)
for d in [0, 1]:
    solver.add(Implies(And(gives[5], day[5] == d),
                       And(gives[1], day[1] == d+1, gives[2], day[2] == d+1)))

# Given condition: Helen, Kyle, Lenore give the three morning reports
solver.add(gives[1])  # Helen gives
solver.add(gives[3])  # Kyle gives
solver.add(gives[4])  # Lenore gives

solver.add(time[1] == 0)  # Helen morning
solver.add(time[3] == 0)  # Kyle morning
solver.add(time[4] == 0)  # Lenore morning

# They are on different days
solver.add(Distinct([day[1], day[3], day[4]]))

# No other student gives a morning report (enforced by count constraints above)

# Let's check if the base model is satisfiable
result = solver.check()
print(f"Base model check: {result}")

if result == sat:
    m = solver.model()
    # Print the full assignment
    for i, name in enumerate(["George","Helen","Irving","Kyle","Lenore","Nina","Olivia","Robert"]):
        g = m.eval(gives[i])
        if g:
            d = m.eval(day[i])
            t = m.eval(time[i])
            print(f"{name}: day={d}, time={'morning' if t==0 else 'afternoon'}")
        else:
            print(f"{name}: no report")
    
    # Now evaluate each option
    # Option A: Helen gives a report on Monday (day=0)
    opt_a = And(day[1] == 0)
    # Option B: Irving gives a report on Monday (day=0)
    opt_b = And(gives[2], day[2] == 0)
    # Option C: Irving gives a report on Wednesday (day=2)
    opt_c = And(gives[2], day[2] == 2)
    # Option D: Kyle gives a report on Tuesday (day=1)
    opt_d = And(day[3] == 1)
    # Option E: Kyle gives a report on Wednesday (day=2)
    opt_e = And(day[4] == 2)  # Wait, option E is "Kyle gives on Wednesday" - that's student 3, not 4
    
    # Correcting: Lenore is index 4, Kyle is index 3
    opt_d = And(day[3] == 1)  # Kyle on Tuesday
    opt_e = And(day[3] == 2)  # Kyle on Wednesday
    
    found_options = []
    for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            found_options.append(letter)
        solver.pop()
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    print("Refine: Base model is unsatisfiable")