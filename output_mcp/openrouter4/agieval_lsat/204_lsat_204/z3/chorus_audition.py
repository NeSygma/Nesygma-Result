from z3 import *

solver = Solver()

# Singers: Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']
# Variables for each singer's position (1-indexed)
pos = {s: Int(f'pos_{s}') for s in singers}

# Domain: positions 1 through 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions are distinct
solver.add(Distinct([pos[s] for s in singers]))

# Recorded auditions: Kammer and Lugo
recorded = {'Kammer', 'Lugo'}

# Condition 1: The fourth audition cannot be recorded.
# The singer at position 4 is not Kammer and not Lugo.
solver.add(pos['Kammer'] != 4)
solver.add(pos['Lugo'] != 4)

# Condition 2: The fifth audition must be recorded.
# The singer at position 5 is Kammer or Lugo.
solver.add(Or(pos['Kammer'] == 5, pos['Lugo'] == 5))

# Condition 3: Waite's audition must take place earlier than the two recorded auditions.
solver.add(pos['Waite'] < pos['Kammer'])
solver.add(pos['Waite'] < pos['Lugo'])

# Condition 4: Kammer's audition must take place earlier than Trillo's audition.
solver.add(pos['Kammer'] < pos['Trillo'])

# Condition 5: Zinn's audition must take place earlier than Yoshida's audition.
solver.add(pos['Zinn'] < pos['Yoshida'])

# Now evaluate each option for the 6th audition
options = {
    "A": pos['Kammer'] == 6,
    "B": pos['Lugo'] == 6,
    "C": pos['Trillo'] == 6,
    "D": pos['Waite'] == 6,
    "E": pos['Zinn'] == 6
}

found_options = []
for letter, constr in options.items():
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