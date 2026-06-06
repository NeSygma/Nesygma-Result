from z3 import *

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bikes: 0=F, 1=G, 2=H, 3=J

solver = Solver()

assign = [[Int(f"assign_{r}_{d}") for d in range(2)] for r in range(4)]

for r in range(4):
    for d in range(2):
        solver.add(assign[r][d] >= 0, assign[r][d] <= 3)

# Each day, all four bikes are tested (each rider gets a different bike each day)
for d in range(2):
    solver.add(Distinct([assign[r][d] for r in range(4)]))

# Each rider tests a different bike on day 2 than on day 1
for r in range(4):
    solver.add(assign[r][0] != assign[r][1])

# Conditions:
# 1. Reynaldo cannot test F (bike 0)
solver.add(assign[0][0] != 0)
solver.add(assign[0][1] != 0)

# 2. Yuki cannot test J (bike 3)
solver.add(assign[3][0] != 3)
solver.add(assign[3][1] != 3)

# 3. Theresa must be one of the testers for H (bike 2)
solver.add(Or(assign[2][0] == 2, assign[2][1] == 2))

# 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
solver.add(assign[1][1] == assign[3][0])

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("SAT - here's a model:")
    for r in range(4):
        riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
        bikes = ["F", "G", "H", "J"]
        print(f"  {riders[r]}: Day1={bikes[m[assign[r][0]].as_long()]}, Day2={bikes[m[assign[r][1]].as_long()]}")
else:
    print("UNSAT")
solver.pop()

# Now test each option
found_options = []
for letter, constr in [
    ("A", assign[0][1] == 1),  # Reynaldo tests G on day 2
    ("B", assign[1][0] == 0),  # Seamus tests F on day 1
    ("C", assign[2][1] == 0),  # Theresa tests F on day 2
    ("D", assign[0][0] == 2),  # Reynaldo tests H on day 1
    ("E", assign[3][1] == 0)   # Yuki tests F on day 2
]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"\nOption {letter} is SAT:")
        for r in range(4):
            riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
            bikes = ["F", "G", "H", "J"]
            print(f"  {riders[r]}: Day1={bikes[m[assign[r][0]].as_long()]}, Day2={bikes[m[assign[r][1]].as_long()]}")
    else:
        print(f"\nOption {letter} is UNSAT")
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