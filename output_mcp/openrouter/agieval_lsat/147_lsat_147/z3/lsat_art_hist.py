from z3 import *

solver = Solver()

# Historians
hist = ['F', 'G', 'H', 'J']
# Topics: 0=Lithographs, 1=Oil, 2=Sculptures, 3=Watercolors

pos = {h: Int(f'pos_{h}') for h in hist}
topic = {h: Int(f'topic_{h}') for h in hist}

# Domain constraints
for h in hist:
    solver.add(pos[h] >= 1, pos[h] <= 4)
    solver.add(topic[h] >= 0, topic[h] <= 3)

# All positions distinct, all topics distinct
solver.add(Distinct([pos[h] for h in hist]))
solver.add(Distinct([topic[h] for h in hist]))

# Helper: for any two historians h1,h2, if h1 has topic t1 and h2 has topic t2 then enforce ordering if needed

def earlier_if(topic1, topic2):
    # enforce: any historian with topic1 is earlier than any historian with topic2
    for h1 in hist:
        for h2 in hist:
            solver.add(Or(topic[h1] != topic1, topic[h2] != topic2, pos[h1] < pos[h2]))

# O (1) and W (3) earlier than L (0)
earlier_if(1, 0)  # Oil before Lithographs
earlier_if(3, 0)  # Watercolors before Lithographs

# Farley earlier than Oil paintings
for h in hist:
    solver.add(Or(topic[h] != 1, pos['F'] < pos[h]))

# Holden earlier than Garcia and Jiang
solver.add(pos['H'] < pos['G'])
solver.add(pos['H'] < pos['J'])

# Define option constraints
opt_a_constr = (topic['F'] == 0)  # Farley gives lithographs
opt_b_constr = (topic['G'] == 2)  # Garcia gives sculptures
opt_c_constr = (topic['G'] == 3)  # Garcia gives watercolors
opt_d_constr = (topic['H'] == 1)  # Holden gives oil paintings
opt_e_constr = (topic['J'] == 3)  # Jiang gives watercolors

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option cannot be true (i.e., not in found_options)
all_opts = {"A", "B", "C", "D", "E"}
cannot = all_opts - set(found_options)
if len(cannot) == 1:
    ans = cannot.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
else:
    # fallback handling
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")