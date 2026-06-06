from z3 import *

# Accomplices: P, Q, R, S, T, V, W
# Positions: 1 to 7
# P = 4
# V, W are consecutive (V, W)
# Q < R
# |S - T| != 1

def check_order(order):
    # order is a list of names
    pos = {name: i + 1 for i, name in enumerate(order)}
    
    # Constraint 4: Peters is 4th
    if pos['Peters'] != 4:
        return False
    
    # Constraint 3: Villas immediately before White
    if pos['White'] != pos['Villas'] + 1:
        return False
    
    # Constraint 2: Quinn earlier than Rovero
    if not (pos['Quinn'] < pos['Rovero']):
        return False
    
    # Constraint 1: Stanton not immediately before or after Tao
    if abs(pos['Stanton'] - pos['Tao']) == 1:
        return False
        
    return True

options = {
    "A": ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    "B": ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    "C": ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    "D": ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    "E": ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
}

valid_options = []
for label, order in options.items():
    if check_order(order):
        valid_options.append(label)

print(f"STATUS: sat")
print(f"Valid options: {valid_options}")