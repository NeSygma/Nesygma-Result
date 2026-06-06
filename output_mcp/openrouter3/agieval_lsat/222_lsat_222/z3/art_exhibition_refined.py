from z3 import *

# Create solver
solver = Solver()

# Students and painting types
students = ["F", "G", "H", "I"]  # Franz, Greene, Hidalgo, Isaacs
paintings = ["O", "W"]  # Oil, Watercolor

# For each student and painting type, we need wall (1-4) and position (U/L)
wall = {}
pos = {}

for s in students:
    for p in paintings:
        wall[(s, p)] = Int(f"wall_{s}_{p}")
        pos[(s, p)] = Bool(f"pos_{s}_{p}")  # True = Upper, False = Lower

# Domain constraints for walls
for s in students:
    for p in paintings:
        solver.add(wall[(s, p)] >= 1)
        solver.add(wall[(s, p)] <= 4)

# Each wall has exactly 2 paintings (one upper, one lower)
for w in range(1, 5):
    paintings_on_wall = []
    for s in students:
        for p in paintings:
            paintings_on_wall.append(If(wall[(s, p)] == w, 1, 0))
    solver.add(Sum(paintings_on_wall) == 2)
    
    # Exactly one upper and one lower on each wall
    upper_count = []
    lower_count = []
    for s in students:
        for p in paintings:
            upper_count.append(If(And(wall[(s, p)] == w, pos[(s, p)]), 1, 0))
            lower_count.append(If(And(wall[(s, p)] == w, Not(pos[(s, p)])), 1, 0))
    solver.add(Sum(upper_count) == 1)
    solver.add(Sum(lower_count) == 1)

# Constraint 1: No wall has only watercolors
for w in range(1, 5):
    has_watercolor = Or([And(wall[(s, "W")] == w) for s in students])
    has_oil = Or([And(wall[(s, "O")] == w) for s in students])
    solver.add(Implies(has_watercolor, has_oil))

# Constraint 2: No wall has work of only one student
for w in range(1, 5):
    student_on_wall = []
    for s in students:
        student_on_wall.append(Or(
            wall[(s, "O")] == w,
            wall[(s, "W")] == w
        ))
    solver.add(Sum([If(student_on_wall[i], 1, 0) for i in range(4)]) >= 2)

# Constraint 3: No wall has both Franz and Isaacs together
for w in range(1, 5):
    franz_on_wall = Or(wall[("F", "O")] == w, wall[("F", "W")] == w)
    isaacs_on_wall = Or(wall[("I", "O")] == w, wall[("I", "W")] == w)
    solver.add(Not(And(franz_on_wall, isaacs_on_wall)))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is displayed
solver.add(wall[("G", "W")] == wall[("F", "O")])
solver.add(pos[("G", "W")] == True)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(wall[("I", "O")] == 4)
solver.add(pos[("I", "O")] == False)

# Additional premise for the question: Greene's oil is on same wall as Franz's watercolor
premise = (wall[("G", "O")] == wall[("F", "W")])

# Define options
opt_a = pos[("G", "O")] == True  # Greene's oil is in upper position
opt_b = wall[("H", "W")] == wall[("I", "W")]  # Hidalgo's watercolor on same wall as Isaacs's watercolor
opt_c = pos[("H", "O")] == True  # Hidalgo's oil in upper position
opt_d = wall[("H", "O")] == wall[("I", "W")]  # Hidalgo's oil on same wall as Isaacs's watercolor
opt_e = pos[("I", "W")] == False  # Isaacs's watercolor in lower position

# For each option, check if premise ∧ ¬option is unsatisfiable
# If so, then the option must be true
must_be_true = []

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(premise)
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

# Also check that premise itself is consistent
solver.push()
solver.add(premise)
premise_consistent = (solver.check() == sat)
solver.pop()

if not premise_consistent:
    print("STATUS: unsat")
    print("Refine: Premise is inconsistent")
elif len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")