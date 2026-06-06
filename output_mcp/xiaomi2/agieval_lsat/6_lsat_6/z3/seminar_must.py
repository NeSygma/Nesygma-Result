from z3 import *

# Base constraints function
def create_solver():
    solver = Solver()
    students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
    slot = [Int(f'slot_{s}') for s in students]
    
    for i in range(8):
        solver.add(Or(slot[i] == -1, And(slot[i] >= 0, slot[i] <= 5)))
    
    solver.add(Sum([If(slot[i] != -1, 1, 0) for i in range(8)]) == 6)
    
    for i in range(8):
        for j in range(i+1, 8):
            solver.add(Implies(And(slot[i] != -1, slot[j] != -1), slot[i] != slot[j]))
    
    for day in range(3):
        am_slot = day * 2
        pm_slot = day * 2 + 1
        solver.add(Sum([If(slot[i] == am_slot, 1, 0) for i in range(8)]) == 1)
        solver.add(Sum([If(slot[i] == pm_slot, 1, 0) for i in range(8)]) == 1)
    
    # George only on Tuesday
    solver.add(Implies(slot[0] != -1, Or(slot[0] == 2, slot[0] == 3)))
    
    # Olivia and Robert cannot give afternoon reports
    for idx in [6, 7]:
        solver.add(Implies(slot[idx] != -1, Or(slot[idx] == 0, slot[idx] == 2, slot[idx] == 4)))
    
    # Nina constraint
    nina_on_monday = And(slot[5] != -1, Or(slot[5] == 0, slot[5] == 1))
    nina_on_tuesday = And(slot[5] != -1, Or(slot[5] == 2, slot[5] == 3))
    helen_on_tuesday = And(slot[1] != -1, Or(slot[1] == 2, slot[1] == 3))
    irving_on_tuesday = And(slot[2] != -1, Or(slot[2] == 2, slot[2] == 3))
    helen_on_wednesday = And(slot[1] != -1, Or(slot[1] == 4, slot[1] == 5))
    irving_on_wednesday = And(slot[2] != -1, Or(slot[2] == 4, slot[2] == 5))
    
    solver.add(Implies(nina_on_monday, And(helen_on_tuesday, irving_on_tuesday)))
    solver.add(Implies(nina_on_tuesday, And(helen_on_wednesday, irving_on_wednesday)))
    
    # Helen, Kyle, Lenore give the three morning reports
    for idx in [1, 3, 4]:
        solver.add(Or(slot[idx] == 0, slot[idx] == 2, slot[idx] == 4))
    solver.add(Distinct(slot[1], slot[3], slot[4]))
    
    return solver, slot

# Answer choices
options = {
    "A": lambda slot: (slot[1] == 0),  # Helen on Monday (Mon_AM)
    "B": lambda slot: Or(slot[2] == 0, slot[2] == 1),  # Irving on Monday
    "C": lambda slot: Or(slot[2] == 4, slot[2] == 5),  # Irving on Wednesday
    "D": lambda slot: (slot[3] == 2),  # Kyle on Tuesday (Tue_AM)
    "E": lambda slot: (slot[3] == 4),  # Kyle on Wednesday (Wed_AM)
}

# For each option, check if it MUST be true (negation is unsat)
must_be_true = []
for letter, constr_fn in options.items():
    s, slot = create_solver()
    s.add(Not(constr_fn(slot)))
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        m = s.model()
        slot_names = {-1: "N/A", 0: "Mon_AM", 1: "Mon_PM", 2: "Tue_AM", 3: "Tue_PM", 4: "Wed_AM", 5: "Wed_PM"}
        students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
        for i, name in enumerate(students):
            val = int(str(m[slot[i]]))
            print(f"    {name}: {slot_names[val]}")
    else:
        print(f"Option {letter}: unknown")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options: {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")