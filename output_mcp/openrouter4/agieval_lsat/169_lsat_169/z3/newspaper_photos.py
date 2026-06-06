from z3 import *

solver = Solver()

# Variables: counts per photographer per section
l_F, l_G, l_H = Ints('l_F l_G l_H')
m_F, m_G, m_H = Ints('m_F m_G m_H')
s_F, s_G, s_H = Ints('s_F s_G s_H')

# Each variable between 0 and 2
vars_list = [l_F, l_G, l_H, m_F, m_G, m_H, s_F, s_G, s_H]
for v in vars_list:
    solver.add(v >= 0, v <= 2)

# Each section has exactly 2 photos
solver.add(l_F + l_G + l_H == 2)
solver.add(m_F + m_G + m_H == 2)
solver.add(s_F + s_G + s_H == 2)

# Total per photographer: at least 1, at most 3
total_F = l_F + m_F + s_F
total_G = l_G + m_G + s_G
total_H = l_H + m_H + s_H

solver.add(total_F >= 1, total_F <= 3)
solver.add(total_G >= 1, total_G <= 3)
solver.add(total_H >= 1, total_H <= 3)

# At least one photograph in Lifestyle by a photographer who has at least one in Metro
solver.add(Or(
    And(l_F > 0, m_F > 0),
    And(l_G > 0, m_G > 0),
    And(l_H > 0, m_H > 0)
))

# Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(l_H == s_F)

# None of Gagnon's photos in Sports
solver.add(s_G == 0)

# Given: Both photos in Lifestyle are by Hue
solver.add(l_H == 2)
solver.add(l_F == 0)
solver.add(l_G == 0)

# Check satisfiability first
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")

if result == sat:
    m = solver.model()
    print("Sample model:")
    print(f"  l_F={m[l_F]}, l_G={m[l_G]}, l_H={m[l_H]}")
    print(f"  m_F={m[m_F]}, m_G={m[m_G]}, m_H={m[m_H]}")
    print(f"  s_F={m[s_F]}, s_G={m[s_G]}, s_H={m[s_H]}")
    print(f"  total_F={m.eval(total_F)}, total_G={m.eval(total_G)}, total_H={m.eval(total_H)}")
    
    # Now check each option
    found_options = []
    options = [
        ("A", total_F == 1),
        ("B", total_F == 3),
        ("C", total_G == 1),
        ("D", total_G == 2),
        ("E", total_H == 2)
    ]
    
    for letter, constr in options:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            found_options.append(letter)
        solver.pop()
    
    print(f"Found options: {found_options}")
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    print("Refine: No valid model found")