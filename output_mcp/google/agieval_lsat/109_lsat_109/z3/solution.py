from z3 import *

# Articles
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
# Topics
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
topic = {
    'G': 'F', 'H': 'F', 'J': 'F',
    'Q': 'N', 'R': 'N', 'S': 'N',
    'Y': 'W'
}

def check_order(order):
    # order is a list of 7 articles
    if len(order) != 7 or len(set(order)) != 7:
        return False
    
    # Condition 1: Consecutive articles cannot cover the same topic
    for i in range(6):
        if topic[order[i]] == topic[order[i+1]]:
            return False
            
    # Condition 2: S can be earlier than Q only if Q is third.
    # (S < Q) => (Q == 3rd)
    pos = {article: i for i, article in enumerate(order)}
    if pos['S'] < pos['Q']:
        if pos['Q'] != 2: # 0-indexed, so 3rd is index 2
            return False
            
    # Condition 3: S must be earlier than Y.
    if not (pos['S'] < pos['Y']):
        return False
        
    # Condition 4: J < G < R
    if not (pos['J'] < pos['G'] < pos['R']):
        return False
        
    return True

options = {
    'A': ['H', 'S', 'J', 'Q', 'Y', 'G', 'R'],
    'B': ['J', 'Q', 'G', 'H', 'S', 'Y', 'R'],
    'C': ['Q', 'J', 'S', 'H', 'Y', 'G', 'R'],
    'D': ['Q', 'J', 'Y', 'S', 'G', 'R', 'H'],
    'E': ['S', 'G', 'Q', 'J', 'Y', 'R', 'H']
}

found_options = []
for letter, order in options.items():
    if check_order(order):
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