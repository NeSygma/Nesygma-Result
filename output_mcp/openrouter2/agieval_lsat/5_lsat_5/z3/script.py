from z3 import *

# Solver instance
solver = Solver()

# Student indices
# 0: George, 1: Helen, 2: Irving, 3: Kyle, 4: Lenore, 5: Nina, 6: Olivia, 7: Robert
G, H, I, K, L, N, O, R = 0,1,2,3,4,5,6,7

# Slot variables: slot[day][slot] where day 0=Mon,1=Tue,2=Wed; slot 0=morning,1=afternoon
slot = [[Int(f'slot_{d}_{s}') for s in range(2)] for d in range(3)]

# Bounds for each slot
for d in range(3):
    for s in range(2):
        solver.add(slot[d][s] >= 0, slot[d][s] <= 7)

# All six reports are distinct students
solver.add(Distinct([slot[d][s] for d in range(3) for s in range(2)]))

# George can only report on Tuesday (day 1)
# He must appear on Tuesday; afternoon is Kyle, so morning must be George
solver.add(slot[1][0] == G)
# George cannot report on Monday or Wednesday
solver.add(slot[0][0] != G, slot[0][1] != G, slot[2][0] != G, slot[2][1] != G)

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(slot[d][1] != O, slot[d][1] != R)

# Nina condition: if Nina reports on day d (0 or 1), then on day d+1 both Helen and Irving must report
for d in range(2):
    cond_nina = Or(slot[d][0] == N, slot[d][1] == N)
    cond_h = Or(slot[d+1][0] == H, slot[d+1][1] == H)
    cond_i = Or(slot[d+1][0] == I, slot[d+1][1] == I)
    solver.add(Implies(cond_nina, And(cond_h, cond_i)))

# Given fixed reports
solver.add(slot[1][1] == K)  # Kyle afternoon Tuesday
solver.add(slot[2][1] == H)  # Helen afternoon Wednesday

# Define option constraints
opt_a_constr = And(slot[0][0] == I, slot[1][0] == L, slot[2][0] == N)
opt_b_constr = And(slot[0][0] == L, slot[1][0] == G, slot[2][0] == I)
opt_c_constr = And(slot[0][0] == N, slot[1][0] == I, slot[2][0] == L)
opt_d_constr = And(slot[0][0] == R, slot[1][0] == G, slot[2][0] == I)
opt_e_constr = And(slot[0][0] == R, slot[1][0] == I, slot[2][0] == L)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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