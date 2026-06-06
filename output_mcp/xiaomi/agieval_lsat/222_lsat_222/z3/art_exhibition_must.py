from z3 import *

solver = Solver()

students = ['F', 'G', 'H', 'I']
types = ['O', 'W']

wall = {}
pos = {}
for s in students:
    for t in types:
        wall[s,t] = Int(f'wall_{s}_{t}')
        pos[s,t] = Int(f'pos_{s}_{t}')
        solver.add(wall[s,t] >= 1, wall[s,t] <= 4)
        solver.add(pos[s,t] >= 0, pos[s,t] <= 1)

# Each (wall, position) pair has exactly one painting
for w in range(1, 5):
    for p in range(2):
        paintings_here = [And(wall[s,t] == w, pos[s,t] == p) for s in students for t in types]
        solver.add(Or(paintings_here))
        for i in range(len(paintings_here)):
            for j in range(i+1, len(paintings_here)):
                solver.add(Not(And(paintings_here[i], paintings_here[j])))

# Constraint 1: No wall has only watercolors
for w in range(1, 5):
    solver.add(Or([And(wall[s,'O'] == w) for s in students]))

# Constraint 2: No wall has work of only one student
for w in range(1, 5):
    student_on_wall = {}
    for s in students:
        student_on_wall[s] = Or(wall[s,'O'] == w, wall[s,'W'] == w)
    pairs = []
    for i in range(len(students)):
        for j in range(i+1, len(students)):
            pairs.append(And(student_on_wall[students[i]], student_on_wall[students[j]]))
    solver.add(Or(pairs))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    franz_on_w = Or(wall['F','O'] == w, wall['F','W'] == w)
    isaacs_on_w = Or(wall['I','O'] == w, wall['I','W'] == w)
    solver.add(Not(And(franz_on_w, isaacs_on_w)))

# Constraint 4: Greene's watercolor is in the upper position of the wall where Franz's oil is
solver.add(wall['G','W'] == wall['F','O'])
solver.add(pos['G','W'] == 0)

# Constraint 5: Isaacs's oil is in the lower position of wall 4
solver.add(wall['I','O'] == 4)
solver.add(pos['I','O'] == 1)

# Constraint 6: Greene's oil is on the same wall as Franz's watercolor
solver.add(wall['G','O'] == wall['F','W'])

# Answer choices
opt_a = (pos['G','O'] == 0)
opt_b = (wall['H','W'] == wall['I','W'])
opt_c = (pos['H','O'] == 0)
opt_d = (wall['H','O'] == wall['I','W'])
opt_e = (pos['I','W'] == 1)

# To find what MUST be true, check if the negation is UNSAT
# If Not(option) is UNSAT, then option must be true in all models
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s2 = Solver()
    # Copy all base constraints
    for c in solver.assertions():
        s2.add(c)
    # Add negation of the option
    s2.add(Not(constr))
    result = s2.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter} MUST be true (negation is UNSAT)")
    else:
        print(f"Option {letter} does NOT have to be true (negation is SAT)")
        m = s2.model()
        print(f"  Counterexample:")
        for s in students:
            for t in types:
                w_val = m[wall[s,t]].as_long()
                p_val = m[pos[s,t]].as_long()
                print(f"    {s}'s {t}: wall {w_val}, {'upper' if p_val==0 else 'lower'}")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")