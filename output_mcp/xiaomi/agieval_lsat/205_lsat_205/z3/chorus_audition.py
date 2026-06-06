from z3 import *

solver = Solver()

# Define singers
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']

# Position variables: each singer gets a position 1-6
pos = {s: Int(f'pos_{s}') for s in singers}

# Each position is between 1 and 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions are distinct
solver.add(Distinct([pos[s] for s in singers]))

# Recorded singers: Kammer and Lugo
# Non-recorded: Trillo, Waite, Yoshida, Zinn

# Condition 1: The fourth audition cannot be recorded
# So position 4 cannot be Kammer or Lugo
solver.add(pos['Kammer'] != 4)
solver.add(pos['Lugo'] != 4)

# Condition 2: The fifth audition must be recorded
# So position 5 must be Kammer or Lugo
solver.add(Or(pos['Kammer'] == 5, pos['Lugo'] == 5))

# Condition 3: Waite's audition must take place earlier than the two recorded auditions
# Waite < Kammer AND Waite < Lugo
solver.add(pos['Waite'] < pos['Kammer'])
solver.add(pos['Waite'] < pos['Lugo'])

# Condition 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(pos['Kammer'] < pos['Trillo'])

# Condition 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos['Zinn'] < pos['Yoshida'])

# Additional condition: Kammer's audition is immediately before Yoshida's
solver.add(pos['Kammer'] + 1 == pos['Yoshida'])

# Define option constraints
opt_a = (pos['Kammer'] == 2)
opt_b = (pos['Trillo'] == 4)
opt_c = (pos['Waite'] == 3)
opt_d = (pos['Yoshida'] == 6)
opt_e = (pos['Zinn'] == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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