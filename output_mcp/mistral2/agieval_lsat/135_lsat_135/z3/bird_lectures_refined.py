from z3 import *

# Base constraints
solver = Solver()

# Locations: 0 = Gladwyn Hall, 1 = Howard Auditorium
location = [Int(f'location_{i}') for i in range(5)]

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
bird_type = [Int(f'bird_type_{i}') for i in range(5)]

# Order of lectures (1st to 5th)
order = [Int(f'order_{i}') for i in range(5)]

# Each lecture has a unique bird type
solver.add(Distinct(bird_type))

# Each lecture has a unique order (1-5)
solver.add(Distinct(order))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(location[0] == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(location[3] == 1)

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([location[i] == 0 for i in range(5)]) == 3)

# Constraint 4: Sandpipers (3) is in Howard Auditorium and earlier than oystercatchers (0)
# Use Or-Loop pattern to avoid indexing with symbolic variables
solver.add(Or([And(bird_type[i] == 3, location[i] == 1) for i in range(5)]))
solver.add(Or([And(bird_type[i] == 0, bird_type[j] == 3, order[i] > order[j]) for i in range(5) for j in range(5) if i != j]))

# Constraint 5: Terns (4) is earlier than petrels (1), and petrels is in Gladwyn Hall
solver.add(Or([And(bird_type[i] == 4, bird_type[j] == 1, order[i] < order[j]) for i in range(5) for j in range(5) if i != j]))
solver.add(Or([And(bird_type[i] == 1, location[i] == 0) for i in range(5)]))

# Assign orders 1-5 to the lectures
for i in range(5):
    solver.add(order[i] >= 1, order[i] <= 5)

# Assign bird types 0-4 to the lectures
for i in range(5):
    solver.add(bird_type[i] >= 0, bird_type[i] <= 4)

# Evaluate each option to see which one must be false
must_be_false = []

# Option A: The first and second lectures are both in Gladwyn Hall.
opt_a_constr = And(location[0] == 0, location[1] == 0)
solver.push()
solver.add(opt_a_constr)
if solver.check() == unsat:
    must_be_false.append("A")
solver.pop()

# Option B: The second and third lectures are both in Howard Auditorium.
opt_b_constr = And(location[1] == 1, location[2] == 1)
solver.push()
solver.add(opt_b_constr)
if solver.check() == unsat:
    must_be_false.append("B")
solver.pop()

# Option C: The second and fifth lectures are both in Gladwyn Hall.
opt_c_constr = And(location[1] == 0, location[4] == 0)
solver.push()
solver.add(opt_c_constr)
if solver.check() == unsat:
    must_be_false.append("C")
solver.pop()

# Option D: The third and fourth lectures are both in Howard Auditorium.
opt_d_constr = And(location[2] == 1, location[3] == 1)
solver.push()
solver.add(opt_d_constr)
if solver.check() == unsat:
    must_be_false.append("D")
solver.pop()

# Option E: The third and fifth lectures are both in Gladwyn Hall.
opt_e_constr = And(location[2] == 0, location[4] == 0)
solver.push()
solver.add(opt_e_constr)
if solver.check() == unsat:
    must_be_false.append("E")
solver.pop()

if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be false")