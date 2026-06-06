from z3 import *

employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
spaces = [1, 2, 3, 4, 5, 6]

# Variables: pos[employee] = space
pos = {e: Int(e) for e in employees}

solver = Solver()

# Each employee gets a unique space
solver.add(Distinct([pos[e] for e in employees]))
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)

# Rules
solver.add(pos['Young'] > pos['Togowa'])
solver.add(pos['Xu'] > pos['Souza'])
solver.add(pos['Robertson'] > pos['Young'])
solver.add(pos['Robertson'] <= 4)

# Find possible spaces for each employee
possible_spaces = {e: [] for e in employees}
for e in employees:
    for s in spaces:
        solver.push()
        solver.add(pos[e] == s)
        if solver.check() == sat:
            possible_spaces[e].append(s)
        solver.pop()

# Count employees with exactly two possible spaces
count = 0
for e in employees:
    if len(possible_spaces[e]) == 2:
        count += 1
        print(f"{e} has {len(possible_spaces[e])} possible spaces: {possible_spaces[e]}")
    else:
        print(f"{e} has {len(possible_spaces[e])} possible spaces: {possible_spaces[e]}")

print(f"Number of employees with exactly two possible spaces: {count}")

# Check against answer choices
# (A)none (B)two (C)three (D)four (E)five
# If count is 2, answer is B.
if count == 0: print("answer:A")
elif count == 2: print("answer:B")
elif count == 3: print("answer:C")
elif count == 4: print("answer:D")
elif count == 5: print("answer:E")
else: print(f"Result {count} not in choices")