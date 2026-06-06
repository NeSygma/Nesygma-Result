from z3 import *

solver = Solver()

# Student IDs
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]

# Days 0..4 (Mon..Fri)
first = [Int(f'first_{d}') for d in range(5)]
second = [Int(f'second_{d}') for d in range(5)]

# Domain constraints and no same student both shifts a day
for d in range(5):
    solver.add(first[d] >= 0, first[d] <= 4)
    solver.add(second[d] >= 0, second[d] <= 4)
    solver.add(first[d] != second[d])

# Each student works exactly two shifts total
for s in students:
    cnt = Sum([If(first[d] == s, 1, 0) + If(second[d] == s, 1, 0) for d in range(5)])
    solver.add(cnt == 2)

# Louise works second shift on two consecutive days (exactly two second shifts)
solver.add(Sum([If(second[d] == L, 1, 0) for d in range(5)]) == 2)
consec_pairs = []
for i in range(4):
    consec_pairs.append(And(second[i] == L, second[i+1] == L))
solver.add(Or(consec_pairs))

# Grecia works first shift on two nonconsecutive days (exactly two first shifts)
solver.add(Sum([If(first[d] == G, 1, 0) for d in range(5)]) == 2)
for i in range(4):
    solver.add(Not(And(first[i] == G, first[i+1] == G)))

# Katya works on Tuesday (day 1) and Friday (day 4)
solver.add(Or(first[1] == K, second[1] == K))
solver.add(Or(first[4] == K, second[4] == K))

# Hakeem and Joe work on the same day at least once (different shifts)
same_day_hj = []
for d in range(5):
    same_day_hj.append(Or(And(first[d] == H, second[d] == J), And(first[d] == J, second[d] == H)))
solver.add(Or(same_day_hj))

# Grecia and Louise never work on the same day
for d in range(5):
    g_on_day = Or(first[d] == G, second[d] == G)
    l_on_day = Or(first[d] == L, second[d] == L)
    solver.add(Not(And(g_on_day, l_on_day)))

# Premise: at least one day where Grecia and Joe both work (different shifts)
same_day_gj = []
for d in range(5):
    same_day_gj.append(Or(And(first[d] == G, second[d] == J), And(first[d] == J, second[d] == G)))
solver.add(Or(same_day_gj))

# Option constraints definitions
opt_a_constr = first[1] == G  # Grecia first shift on Tuesday
opt_b_constr = second[0] == H  # Hakeem second shift on Monday
opt_c_constr = second[2] == H  # Hakeem second shift on Wednesday
opt_d_constr = first[2] == J   # Joe first shift on Wednesday
opt_e_constr = first[3] == J   # Joe first shift on Thursday

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