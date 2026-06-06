from z3 import *

# Define variables for each section and photographer
# L_F, L_G, L_H: number of photos by F, G, H in Lifestyle
# M_F, M_G, M_H: number of photos by F, G, H in Metro
# S_F, S_G, S_H: number of photos by F, G, H in Sports

def check_option(L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H):
    solver = Solver()
    
    # Total photos per section is 2
    solver.add(L_F + L_G + L_H == 2)
    solver.add(M_F + M_G + M_H == 2)
    solver.add(S_F + S_G + S_H == 2)
    
    # Total photos per photographer is between 1 and 3
    F_total = L_F + M_F + S_F
    G_total = L_G + M_G + S_G
    H_total = L_H + M_H + S_H
    
    solver.add(F_total >= 1, F_total <= 3)
    solver.add(G_total >= 1, G_total <= 3)
    solver.add(H_total >= 1, H_total <= 3)
    
    # At least one photo in L must be by a photographer who has at least one photo in M
    # (L_F > 0 AND M_F > 0) OR (L_G > 0 AND M_G > 0) OR (L_H > 0 AND M_H > 0)
    solver.add(Or(
        And(L_F > 0, M_F > 0),
        And(L_G > 0, M_G > 0),
        And(L_H > 0, M_H > 0)
    ))
    
    # Hue's photos in L = Fuentes's photos in S
    solver.add(L_H == S_F)
    
    # None of Gagnon's photos in S
    solver.add(S_G == 0)
    
    return solver.check() == sat

# Define options
options = [
    ("A", (2, 0, 0, 1, 0, 1, 0, 1, 1)),
    ("B", (1, 1, 0, 1, 1, 0, 0, 0, 2)),
    ("C", (2, 0, 0, 0, 2, 0, 0, 0, 2)),
    ("D", (0, 2, 0, 1, 1, 0, 1, 0, 1)),
    ("E", (0, 1, 1, 0, 0, 2, 1, 0, 1))
]

found_options = []
for letter, vals in options:
    if check_option(*vals):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")