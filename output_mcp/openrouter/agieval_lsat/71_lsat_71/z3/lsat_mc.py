from z3 import *

# Define assistants
assistants = ['Julio','Kevin','Lan','Nessa','Olivia','Rebecca']
# Map name to index variable for slot (0..5)
slot = {name: Int(name) for name in assistants}
solver = Solver()
# Slots domain 0..5
for name in assistants:
    solver.add(slot[name] >= 0, slot[name] <= 5)
# All distinct slots
solver.add(Distinct([slot[name] for name in assistants]))
# Helper functions for day and time

def day_of(s):
    # integer division by 2, then +1 for day number 1..3
    return s / 2 + 1  # using integer division (since s is Int, / is Euclidean division)

def time_of(s):
    return s % 2  # 0 morning, 1 afternoon

# Base constraints
# Kevin and Rebecca same day
solver.add(day_of(slot['Kevin']) == day_of(slot['Rebecca']))
# Lan and Olivia different day
solver.add(day_of(slot['Lan']) != day_of(slot['Olivia']))
# Nessa afternoon
solver.add(time_of(slot['Nessa']) == 1)
# Julio earlier day than Olivia
solver.add(day_of(slot['Julio']) < day_of(slot['Olivia']))

# Define option constraints
# mapping for each option: day->(morning, afternoon)
options = {
    'A': {
        'Wednesday': ('Rebecca','Kevin'),
        'Thursday': ('Julio','Lan'),
        'Friday': ('Nessa','Olivia')
    },
    'B': {
        'Wednesday': ('Olivia','Nessa'),
        'Thursday': ('Julio','Lan'),
        'Friday': ('Kevin','Rebecca')
    },
    'C': {
        'Wednesday': ('Lan','Kevin'),
        'Thursday': ('Rebecca','Julio'),
        'Friday': ('Olivia','Nessa')
    },
    'D': {
        'Wednesday': ('Kevin','Rebecca'),
        'Thursday': ('Julio','Nessa'),
        'Friday': ('Olivia','Lan')
    },
    'E': {
        'Wednesday': ('Julio','Lan'),
        'Thursday': ('Olivia','Nessa'),
        'Friday': ('Rebecca','Kevin')
    }
}
# day to index mapping
day_index = {'Wednesday':0, 'Thursday':1, 'Friday':2}

found_options = []
for letter, assign in options.items():
    solver.push()
    # add constraints for each day
    for day, (morning, afternoon) in assign.items():
        d = day_index[day]
        # morning slot = d*2, afternoon = d*2+1
        solver.add(slot[morning] == d*2)
        solver.add(slot[afternoon] == d*2+1)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")