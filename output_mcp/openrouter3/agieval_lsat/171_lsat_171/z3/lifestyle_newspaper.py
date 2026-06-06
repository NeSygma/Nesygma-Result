from z3 import *

solver = Solver()

# Variables
f_l, f_m, f_s = Ints('f_l f_m f_s')
g_l, g_m, g_s = Ints('g_l g_m g_s')
h_l, h_m, h_s = Ints('h_l h_m h_s')

# Each section has exactly 2 photos
solver.add(f_l + g_l + h_l == 2)
solver.add(f_m + g_m + h_m == 2)
solver.add(f_s + g_s + h_s == 2)

# Each photographer has between 1 and 3 photos total
solver.add(1 <= f_l + f_m + f_s, f_l + f_m + f_s <= 3)
solver.add(1 <= g_l + g_m + g_s, g_l + g_m + g_s <= 3)
solver.add(1 <= h_l + h_m + h_s, h_l + h_m + h_s <= 3)

# At least one Lifestyle photo by a photographer who also has at least one Metro photo
solver.add(Or(
    And(f_l > 0, f_m > 0),
    And(g_l > 0, g_m > 0),
    And(h_l > 0, h_m > 0)
))

# Number of Hue's Lifestyle photos equals number of Fuentes' Sports photos
solver.add(h_l == f_s)

# No Gagnon photos in Sports
solver.add(g_s == 0)

# All counts must be non-negative integers
solver.add(f_l >= 0, f_m >= 0, f_s >= 0)
solver.add(g_l >= 0, g_m >= 0, g_s >= 0)
solver.add(h_l >= 0, h_m >= 0, h_s >= 0)

# Evaluate each answer choice
found_options = []

# Option A: f_l=1, f_m=1, f_s=1
solver.push()
solver.add(f_l == 1, f_m == 1, f_s == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: f_l=1, f_s=2, f_m=0
solver.push()
solver.add(f_l == 1, f_s == 2, f_m == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: f_l=2, f_s=1, f_m=0
solver.push()
solver.add(f_l == 2, f_s == 1, f_m == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: f_m=1, f_s=2, f_l=0
solver.push()
solver.add(f_m == 1, f_s == 2, f_l == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: f_m=2, f_s=1, f_l=0
solver.push()
solver.add(f_m == 2, f_s == 1, f_l == 0)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")