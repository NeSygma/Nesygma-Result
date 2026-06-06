from z3 import *

# Students
students = ['G', 'H', 'I', 'K', 'L', 'N', 'O', 'R']
# Slots
slots = ['M_AM', 'M_PM', 'T_AM', 'T_PM', 'W_AM', 'W_PM']

# Variables: which student is in which slot?
# We use a function mapping slot to student.
# Since exactly 6 students are chosen, we can represent this as:
# slot_to_student[slot] = student_index (0-7)
# If a slot is empty, we can't have that, all 6 slots must be filled.
# Let's use an Int for each slot representing the student index.
# 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R

slot_to_student = [Int(f'slot_{s}') for s in slots]
solver = Solver()

# Each slot has a student, all distinct
solver.add(Distinct(slot_to_student))
for s in slot_to_student:
    solver.add(s >= 0, s <= 7)

# Mapping indices
G, H, I, K, L, N, O, R = range(8)

# C1: Tuesday is the only day George can give a report.
# George is in slot_to_student[2] or slot_to_student[3] if he gives a report.
# If he doesn't give a report, he's not in any slot.
# Wait, the problem says "exactly six will give individual oral reports".
# So G might not be chosen.
# Let's add a boolean for each student: chosen[student]
chosen = [Bool(f'chosen_{st}') for st in students]
for i in range(8):
    solver.add(chosen[i] == Or([slot_to_student[j] == i for j in range(6)]))

# C1: If G is chosen, G must be in T_AM or T_PM.
solver.add(Implies(chosen[G], Or(slot_to_student[2] == G, slot_to_student[3] == G)))

# C2: Neither Olivia nor Robert can give an afternoon report.
# Afternoon slots: M_PM (1), T_PM (3), W_PM (5)
for st in [O, R]:
    solver.add(Not(Or(slot_to_student[1] == st, slot_to_student[3] == st, slot_to_student[5] == st)))

# C3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
# Nina is in slot_to_student[j]
# If N in {M_AM, M_PM}, then H and I must be in {T_AM, T_PM}.
# If N in {T_AM, T_PM}, then H and I must be in {W_AM, W_PM}.
# If N in {W_AM, W_PM}, no condition.
n_in_mon = Or(slot_to_student[0] == N, slot_to_student[1] == N)
n_in_tue = Or(slot_to_student[2] == N, slot_to_student[3] == N)
h_in_tue = Or(slot_to_student[2] == H, slot_to_student[3] == H)
i_in_tue = Or(slot_to_student[2] == I, slot_to_student[3] == I)
h_in_wed = Or(slot_to_student[4] == H, slot_to_student[5] == H)
i_in_wed = Or(slot_to_student[4] == I, slot_to_student[5] == I)

solver.add(Implies(n_in_mon, And(h_in_tue, i_in_tue)))
solver.add(Implies(n_in_tue, And(h_in_wed, i_in_wed)))

# Q: If Kyle gives the afternoon report on Tuesday (K = T_PM), and Helen gives the afternoon report on Wednesday (H = W_PM)
solver.add(slot_to_student[3] == K)
solver.add(slot_to_student[5] == H)

# Answer choices: (M_AM, T_AM, W_AM)
options = {
    "A": (I, L, N),
    "B": (L, G, I),
    "C": (N, I, L),
    "D": (R, G, I),
    "E": (R, I, L)
}

found_options = []
for letter, (m_am, t_am, w_am) in options.items():
    solver.push()
    solver.add(slot_to_student[0] == m_am)
    solver.add(slot_to_student[2] == t_am)
    solver.add(slot_to_student[4] == w_am)
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