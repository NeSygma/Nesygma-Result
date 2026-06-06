from z3 import *

def check_option(order):
    # order is a list of clues in order of chapters 1-7
    # e.g., ['S', 'T', 'Z', 'X', 'U', 'W', 'R']
    pos = {clue: i + 1 for i, clue in enumerate(order)}
    
    # 1. T cannot be mentioned in chapter 1
    if pos['T'] == 1: return False
    
    # 2. T must be mentioned before W, and exactly two chapters separating them
    # pos_W = pos_T + 3
    if pos['W'] != pos['T'] + 3: return False
    
    # 3. S and Z cannot be mentioned in adjacent chapters
    if abs(pos['S'] - pos['Z']) == 1: return False
    
    # 4. W and X cannot be mentioned in adjacent chapters
    if abs(pos['W'] - pos['X']) == 1: return False
    
    # 5. U and X must be mentioned in adjacent chapters
    if abs(pos['U'] - pos['X']) != 1: return False
    
    return True

options = {
    "A": ['S', 'T', 'Z', 'X', 'U', 'W', 'R'],
    "B": ['T', 'X', 'U', 'W', 'S', 'R', 'Z'],
    "C": ['U', 'S', 'X', 'T', 'Z', 'R', 'W'],
    "D": ['X', 'U', 'T', 'Z', 'R', 'W', 'S'],
    "E": ['Z', 'R', 'T', 'U', 'X', 'W', 'S']
}

valid_options = []
for label, order in options.items():
    if check_option(order):
        valid_options.append(label)

print(f"STATUS: sat")
print(f"Valid options: {valid_options}")
if len(valid_options) == 1:
    print(f"answer:{valid_options[0]}")