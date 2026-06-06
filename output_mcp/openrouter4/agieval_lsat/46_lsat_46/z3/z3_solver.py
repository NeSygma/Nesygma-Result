from z3 import *

solver = Solver()

# Students: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Plays: 0=Sunset, 1=Tamerlane, 2=Undulation
NUM_STUDENTS = 5
NUM_PLAYS = 3

# Variables: student_play[s][p] is True iff student s reviews play p
student_play = [[Bool(f's_{s}_p_{p}') for p in range(NUM_PLAYS)] for s in range(NUM_STUDENTS)]

# Each student reviews one or more of exactly three plays (1 to 3 plays)
for s in range(NUM_STUDENTS):
    count = Sum([If(student_play[s][p], 1, 0) for p in range(NUM_PLAYS)])
    solver.add(count >= 1)
    solver.add(count <= 3)

# Constraint 1: Kramer (1) and Lopez (2) each review fewer plays than Megregian (3)
kramer_count = Sum([If(student_play[1][p], 1, 0) for p in range(NUM_PLAYS)])
lopez_count = Sum([If(student_play[2][p], 1, 0) for p in range(NUM_PLAYS)])
megregian_count = Sum([If(student_play[3][p], 1, 0) for p in range(NUM_PLAYS)])
solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# Constraint 2: Neither Lopez (2) nor Megregian (3) reviews any play Jiang (0) reviews
# For each play p: not (Jiang reviews p AND Lopez reviews p)
# and not (Jiang reviews p AND Megregian reviews p)
for p in range(NUM_PLAYS):
    solver.add(Not(And(student_play[0][p], student_play[2][p])))
    solver.add(Not(And(student_play[0][p], student_play[3][p])))

# Constraint 3: Kramer (1) and O'Neill (4) both review Tamerlane (play index 1)
solver.add(student_play[1][1] == True)
solver.add(student_play[4][1] == True)

# Constraint 4: Exactly two of the students review exactly the same play or plays as each other.
# This means exactly one pair of students has identical review sets.
pair_same_vars = []
for i in range(NUM_STUDENTS):
    for j in range(i+1, NUM_STUDENTS):
        same = Bool(f'same_{i}_{j}')
        # same is True iff for all plays p, student i and j have the same boolean value
        solver.add(same == And([student_play[i][p] == student_play[j][p] for p in range(NUM_PLAYS)]))
        pair_same_vars.append(same)

# Exactly one pair has identical sets
solver.add(PbEq([(v, 1) for v in pair_same_vars], 1))

# Now test the answer choices
# Each option is an "accurate and complete list" - i.e., exactly those students review Tamerlane
# and no other students review Tamerlane

options = {
    "A": [0, 1],      # Jiang, Kramer
    "B": [1, 4],      # Kramer, O'Neill
    "C": [1, 2, 4],   # Kramer, Lopez, O'Neill
    "D": [1, 3, 4],   # Kramer, Megregian, O'Neill
    "E": [2, 3, 4]    # Lopez, Megregian, O'Neill
}

found_options = []

for letter, tamerlane_students in options.items():
    solver.push()
    # For students in the list: they review Tamerlane
    for s in tamerlane_students:
        solver.add(student_play[s][1] == True)
    # For students NOT in the list: they do NOT review Tamerlane
    for s in range(NUM_STUDENTS):
        if s not in tamerlane_students:
            solver.add(student_play[s][1] == False)
    
    if solver.check() == sat:
        found_options.append(letter)
        # For debugging, let's see the model
        # m = solver.model()
        # print(f"Option {letter} model:")
        # for s in range(NUM_STUDENTS):
        #     plays = [p for p in range(NUM_PLAYS) if is_true(m.eval(student_play[s][p]))]
        #     print(f"  Student {s}: plays {plays}")
    
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