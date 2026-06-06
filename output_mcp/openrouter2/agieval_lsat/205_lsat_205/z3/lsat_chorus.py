from z3 import *
solver = Solver()
# Define singers
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']
pos = {name: Int(name) for name in singers}
# Domain constraints
for name in singers:
    solver.add(pos[name] >= 1, pos[name] <= 6)
# All distinct
solver.add(Distinct([pos[name] for name in singers]))
# Fourth audition cannot be recorded (i.e., not Kammer or Lugo)
solver.add(pos['Kammer'] != 4, pos['Lugo'] != 4)
# Fifth audition must be recorded (Kammer or Lugo)
solver.add(Or(pos['Kammer'] == 5, pos['Lugo'] == 5))
# Waite earlier than both recorded auditions
solver.add(pos['Waite'] < pos['Kammer'], pos['Waite'] < pos['Lugo'])
# Kammer earlier than Trillo
solver.add(pos['Kammer'] < pos['Trillo'])
# Zinn earlier than Yoshida
solver.add(pos['Zinn'] < pos['Yoshida'])
# Kammer immediately before Yoshida
solver.add(pos['Yoshida'] == pos['Kammer'] + 1)
# Option constraints
opt_a_constr = pos['Kammer'] == 2
opt_b_constr = pos['Trillo'] == 4
opt_c_constr = pos['Waite'] == 3
opt_d_constr = pos['Yoshida'] == 6
opt_e_constr = pos['Zinn'] == 2
# Evaluate options
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