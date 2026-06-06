from z3 import *

# Historians: F, G, H, J
# Topics: L, O, S, W
# Time slots: 1, 2, 3, 4

def check_constraints(assignment):
    # assignment is a list of tuples: (historian, topic, time)
    # e.g., [('Farley', 'sculptures', 1), ...]
    
    # Extract times for topics
    time_L = [a[2] for a in assignment if a[1] == 'lithographs'][0]
    time_O = [a[2] for a in assignment if a[1] == 'oil paintings'][0]
    time_S = [a[2] for a in assignment if a[1] == 'sculptures'][0]
    time_W = [a[2] for a in assignment if a[1] == 'watercolors'][0]
    
    # Extract times for historians
    time_F = [a[2] for a in assignment if a[0] == 'Farley'][0]
    time_G = [a[2] for a in assignment if a[0] == 'Garcia'][0]
    time_H = [a[2] for a in assignment if a[0] == 'Holden'][0]
    time_J = [a[2] for a in assignment if a[0] == 'Jiang'][0]
    
    # Constraints:
    # 1. O < L and W < L
    c1 = (time_O < time_L) and (time_W < time_L)
    # 2. F < O
    c2 = (time_F < time_O)
    # 3. H < G and H < J
    c3 = (time_H < time_G) and (time_H < time_J)
    
    return c1 and c2 and c3

# Answer Choices
# (A) Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
# (B) Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
# (C) Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
# (D) Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
# (E) Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs

choices = {
    "A": [('Farley', 'sculptures', 1), ('Holden', 'lithographs', 2), ('Garcia', 'oil paintings', 3), ('Jiang', 'watercolors', 4)],
    "B": [('Farley', 'watercolors', 1), ('Jiang', 'oil paintings', 2), ('Holden', 'sculptures', 3), ('Garcia', 'lithographs', 4)],
    "C": [('Garcia', 'sculptures', 1), ('Farley', 'watercolors', 2), ('Holden', 'oil paintings', 3), ('Jiang', 'lithographs', 4)],
    "D": [('Holden', 'oil paintings', 1), ('Jiang', 'watercolors', 2), ('Farley', 'lithographs', 3), ('Garcia', 'sculptures', 4)],
    "E": [('Holden', 'sculptures', 1), ('Farley', 'watercolors', 2), ('Jiang', 'oil paintings', 3), ('Garcia', 'lithographs', 4)]
}

valid_options = []
for letter, assignment in choices.items():
    if check_constraints(assignment):
        valid_options.append(letter)

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")