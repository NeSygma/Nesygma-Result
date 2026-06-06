from z3 import *

solver = Solver()

# Singers: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = [Int(f'singer_{i}') for i in range(6)]
names = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']

# Each singer gets a unique position 1-6
for s in singers:
    solver.add(s >= 1, s <= 6)
solver.add(Distinct(singers))

# Recorded auditions: Kammer (0) and Lugo (1)
# Not recorded: Trillo (2), Waite (3), Yoshida (4), Zinn (5)

# Condition 1: The fourth audition cannot be recorded
# So position 4 is NOT Kammer and NOT Lugo
solver.add(singers[0] != 4)  # Kammer not at position 4
solver.add(singers[1] != 4)  # Lugo not at position 4

# Condition 2: The fifth audition must be recorded
# So position 5 is either Kammer or Lugo
solver.add(Or(singers[0] == 5, singers[1] == 5))

# Condition 3: Waite's audition must take place earlier than the two recorded auditions
# Waite (3) < Kammer (0) AND Waite (3) < Lugo (1)
solver.add(singers[3] < singers[0])
solver.add(singers[3] < singers[1])

# Condition 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(singers[0] < singers[2])

# Condition 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(singers[5] < singers[4])

# Now check each answer choice for Yoshida (singer[4])
found_options = []

# (A) Yoshida is fifth
solver.push()
solver.add(singers[4] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Yoshida is fourth
solver.push()
solver.add(singers[4] == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Yoshida is third
solver.push()
solver.add(singers[4] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Yoshida is second
solver.push()
solver.add(singers[4] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Yoshida is first
solver.push()
solver.add(singers[4] == 1)
if solver.check() == sat:
    found_options.append("E")
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