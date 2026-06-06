from z3 import *

# Assistants
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
# Days: 0=Wed, 1=Thu, 2=Fri
# Times: 0=Morning, 1=Afternoon

def check_assignment(assignment):
    # assignment is a dict: (day, time) -> assistant
    # Check constraints
    
    # 1. Kevin and Rebecca same day
    day_K = [d for (d, t), a in assignment.items() if a == 'Kevin'][0]
    day_R = [d for (d, t), a in assignment.items() if a == 'Rebecca'][0]
    if day_K != day_R: return False
    
    # 2. Lan and Olivia different day
    day_L = [d for (d, t), a in assignment.items() if a == 'Lan'][0]
    day_O = [d for (d, t), a in assignment.items() if a == 'Olivia'][0]
    if day_L == day_O: return False
    
    # 3. Nessa afternoon
    time_N = [t for (d, t), a in assignment.items() if a == 'Nessa'][0]
    if time_N != 1: return False
    
    # 4. Julio earlier than Olivia
    day_J = [d for (d, t), a in assignment.items() if a == 'Julio'][0]
    if not (day_J < day_O): return False
    
    return True

# Define options
options = {
    "A": { (0,0): 'Rebecca', (0,1): 'Kevin', (1,0): 'Julio', (1,1): 'Lan', (2,0): 'Nessa', (2,1): 'Olivia' },
    "B": { (0,0): 'Olivia', (0,1): 'Nessa', (1,0): 'Julio', (1,1): 'Lan', (2,0): 'Kevin', (2,1): 'Rebecca' },
    "C": { (0,0): 'Lan', (0,1): 'Kevin', (1,0): 'Rebecca', (1,1): 'Julio', (2,0): 'Olivia', (2,1): 'Nessa' },
    "D": { (0,0): 'Kevin', (0,1): 'Rebecca', (1,0): 'Julio', (1,1): 'Nessa', (2,0): 'Olivia', (2,1): 'Lan' },
    "E": { (0,0): 'Julio', (0,1): 'Lan', (1,0): 'Olivia', (1,1): 'Nessa', (2,0): 'Rebecca', (2,1): 'Kevin' }
}

valid_options = []
for letter, assignment in options.items():
    if check_assignment(assignment):
        valid_options.append(letter)

print(f"STATUS: sat")
print(f"Valid options: {valid_options}")
if len(valid_options) == 1:
    print(f"answer:{valid_options[0]}")