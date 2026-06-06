from z3 import *

solver = Solver()

# Students: G=0, H=1, J=2, K=3, L=4
# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
# Shifts: First=0, Second=1

G, H, J, K, L = 0, 1, 2, 3, 4
NUM_DAYS = 5
NUM_SHIFTS = 2

# Assignment variables: assign[d][s] = student working day d, shift s
assign = [[Int(f"assign_{d}_{s}") for s in range(NUM_SHIFTS)] for d in range(NUM_DAYS)]

# Domain constraints: each assignment is a valid student (0-4)
for d in range(NUM_DAYS):
    for s in range(NUM_SHIFTS):
        solver.add(assign[d][s] >= 0, assign[d][s] <= 4)

# Constraint 1: Each student works exactly 2 shifts
for student in range(5):
    solver.add(Sum([If(assign[d][s] == student, 1, 0) 
                     for d in range(NUM_DAYS) for s in range(NUM_SHIFTS)]) == 2)

# Constraint 2: No student works both shifts of any day
for d in range(NUM_DAYS):
    solver.add(assign[d][0] != assign[d][1])

# Constraint 3: Louise works second shift on two consecutive days
# Since Louise works exactly 2 shifts, both must be second shifts on consecutive days
consecutive_louise = []
for d in range(4):  # pairs: (0,1), (1,2), (2,3), (3,4)
    consecutive_louise.append(And(assign[d][1] == L, assign[d+1][1] == L))
solver.add(Or(consecutive_louise))

# Constraint 4: Grecia works first shift on two nonconsecutive days
# Since Grecia works exactly 2 shifts, both are first shifts on nonconsecutive days
solver.add(Sum([If(assign[d][0] == G, 1, 0) for d in range(NUM_DAYS)]) == 2)
nonconsecutive_grecia = []
for d1 in range(NUM_DAYS):
    for d2 in range(d1 + 2, NUM_DAYS):  # gap >= 2 means nonconsecutive
        nonconsecutive_grecia.append(And(assign[d1][0] == G, assign[d2][0] == G))
solver.add(Or(nonconsecutive_grecia))

# Constraint 5: Katya works on Tuesday and Friday
# Katya works exactly 2 shifts, one on Tuesday and one on Friday
solver.add(Or(assign[1][0] == K, assign[1][1] == K))  # Tuesday
solver.add(Or(assign[4][0] == K, assign[4][1] == K))  # Friday

# Constraint 6: Hakeem and Joe work on the same day at least once
hj_same_day = []
for d in range(NUM_DAYS):
    h_works_d = Or(assign[d][0] == H, assign[d][1] == H)
    j_works_d = Or(assign[d][0] == J, assign[d][1] == J)
    hj_same_day.append(And(h_works_d, j_works_d))
solver.add(Or(hj_same_day))

# Constraint 7: Grecia and Louise never work on the same day
for d in range(NUM_DAYS):
    g_works_d = Or(assign[d][0] == G, assign[d][1] == G)
    l_works_d = Or(assign[d][0] == L, assign[d][1] == L)
    solver.add(Not(And(g_works_d, l_works_d)))

# Additional condition: At least one day where both Grecia and Joe work
gj_same_day = []
for d in range(NUM_DAYS):
    g_works_d = Or(assign[d][0] == G, assign[d][1] == G)
    j_works_d = Or(assign[d][0] == J, assign[d][1] == J)
    gj_same_day.append(And(g_works_d, j_works_d))
solver.add(Or(gj_same_day))

# Define answer options
opt_a = (assign[1][0] == G)   # Grecia works first shift on Tuesday
opt_b = (assign[0][1] == H)   # Hakeem works second shift on Monday
opt_c = (assign[2][1] == H)   # Hakeem works second shift on Wednesday
opt_d = (assign[2][0] == J)   # Joe works first shift on Wednesday
opt_e = (assign[3][0] == J)   # Joe works first shift on Thursday

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        student_names = ["G", "H", "J", "K", "L"]
        print(f"Option {letter} is SAT:")
        for d in range(NUM_DAYS):
            s0 = m.evaluate(assign[d][0])
            s1 = m.evaluate(assign[d][1])
            s0_str = student_names[int(str(s0))]
            s1_str = student_names[int(str(s1))]
            print(f"  {day_names[d]}: 1st={s0_str}, 2nd={s1_str}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")