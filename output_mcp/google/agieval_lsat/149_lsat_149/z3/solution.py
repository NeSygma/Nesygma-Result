from z3 import *

# Colors: 0:Forest, 1:Olive, 2:Peach, 3:Turquoise, 4:White, 5:Yellow
colors = range(6)
color_names = ["Forest", "Olive", "Peach", "Turquoise", "White", "Yellow"]

def check_option(rugs):
    # rugs is a list of lists of color indices
    # 1. Exactly 5 colors used
    used_colors = []
    for r in rugs:
        used_colors.extend(r)
    if len(used_colors) != 5:
        return False
    if len(set(used_colors)) != 5:
        return False
    
    # 2. Each color used in only one rug (already satisfied by structure)
    
    # Rules:
    # 1. In any rug in which white (4) is used, two other colors are also used.
    for r in rugs:
        if 4 in r:
            if len(r) != 3:
                return False
    
    # 2. In any rug in which olive (1) is used, peach (2) is also used.
    for r in rugs:
        if 1 in r:
            if 2 not in r:
                return False
                
    # 3. Forest (0) and turquoise (3) are not used together.
    for r in rugs:
        if 0 in r and 3 in r:
            return False
            
    # 4. Peach (2) and turquoise (3) are not used together.
    for r in rugs:
        if 2 in r and 3 in r:
            return False
            
    # 5. Peach (2) and yellow (5) are not used together.
    for r in rugs:
        if 2 in r and 5 in r:
            return False
            
    return True

# Options
# (A) forest only; turquoise only; olive, peach, and white
# (B) forest only; turquoise only; olive, peach, and yellow
# (C) peach only; turquoise only; forest, olive, and white
# (D) yellow only; forest and turquoise; olive and peach
# (E) yellow only; olive and peach; turquoise and white

options = {
    "A": [[0], [3], [1, 2, 4]],
    "B": [[0], [3], [1, 2, 5]],
    "C": [[2], [3], [0, 1, 4]],
    "D": [[5], [0, 3], [1, 2]],
    "E": [[5], [1, 2], [3, 4]]
}

results = {}
for name, rugs in options.items():
    results[name] = check_option(rugs)

print("STATUS: sat")
for name, valid in results.items():
    print(f"Option {name}: {valid}")