from z3 import *

solver = Solver()

# Singers
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']

# Position variables: pos[s] = position (1-6) for each singer
pos = {s: Int(f'pos_{s}') for s in singers}

# Each singer gets a unique position from 1 to 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)
solver.add(Distinct([pos[s] for s in singers]))

# Recorded singers: Kammer and Lugo
recorded = ['Kammer', 'Lugo']
not_recorded = ['Trillo', 'Waite', 'Yoshida', 'Zinn']

# The fourth audition cannot be recorded
for s in recorded:
    solver.add(pos[s] != 4)

# The fifth audition must be recorded
solver.add(Or(pos['Kammer'] == 5, pos['Lugo'] == 5))

# Waite's audition must take place earlier than the two recorded auditions
solver.add(pos['Waite'] < pos['Kammer'])
solver.add(pos['Waite'] < pos['Lugo'])

# Kammer's audition must take place earlier than Trillo's audition
solver.add(pos['Kammer'] < pos['Trillo'])

# Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos['Zinn'] < pos['Yoshida'])

# Now test each option for who could be the sixth audition
found_options = []

# Option A: Kammer is 6th
solver.push()
solver.add(pos['Kammer'] == 6)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Lugo is 6th
solver.push()
solver.add(pos['Lugo'] == 6)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Trillo is 6th
solver.push()
solver.add(pos['Trillo'] == 6)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Waite is 6th
solver.push()
solver.add(pos['Waite'] == 6)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Zinn is 6th
solver.push()
solver.add(pos['Zinn'] == 6)
if solver.check() == sat:
    found_options.append('E')
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