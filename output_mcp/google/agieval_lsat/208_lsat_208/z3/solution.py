from z3 import *

# Students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
# Teams: 0 = Green, 1 = Red
# Facilitator: True/False

def check_option(team_assignment, facilitators):
    # team_assignment: dict {student: team_id}
    # facilitators: dict {student: is_facilitator}
    
    # 1. Juana different team than Olga
    if team_assignment['Juana'] == team_assignment['Olga']:
        return False
    
    # 2. Lateefah on Green
    if team_assignment['Lateefah'] != 0:
        return False
        
    # 3. Kelly not a facilitator
    if facilitators['Kelly']:
        return False
        
    # 4. Olga is a facilitator
    if not facilitators['Olga']:
        return False
        
    # Team sizes: one 2, one 3
    green_members = [s for s in students if team_assignment[s] == 0]
    red_members = [s for s in students if team_assignment[s] == 1]
    if not ((len(green_members) == 2 and len(red_members) == 3) or 
            (len(green_members) == 3 and len(red_members) == 2)):
        return False
        
    # One facilitator per team
    green_facs = [s for s in green_members if facilitators[s]]
    red_facs = [s for s in red_members if facilitators[s]]
    if len(green_facs) != 1 or len(red_facs) != 1:
        return False
        
    return True

# Define options
options = {
    "A": {
        "team": {'Juana': 0, 'Lateefah': 0, 'Olga': 0, 'Kelly': 1, 'Mei': 1},
        "fac": {'Juana': False, 'Lateefah': False, 'Olga': True, 'Kelly': False, 'Mei': True}
    },
    "B": {
        "team": {'Kelly': 0, 'Lateefah': 0, 'Olga': 0, 'Juana': 1, 'Mei': 1},
        "fac": {'Kelly': False, 'Lateefah': True, 'Olga': False, 'Juana': False, 'Mei': True}
    },
    "C": {
        "team": {'Kelly': 0, 'Lateefah': 0, 'Olga': 0, 'Juana': 1, 'Mei': 1},
        "fac": {'Kelly': False, 'Lateefah': False, 'Olga': True, 'Juana': True, 'Mei': False}
    },
    "D": {
        "team": {'Kelly': 0, 'Mei': 0, 'Olga': 0, 'Juana': 1, 'Lateefah': 1},
        "fac": {'Kelly': False, 'Mei': False, 'Olga': True, 'Juana': True, 'Lateefah': False}
    },
    "E": {
        "team": {'Lateefah': 0, 'Olga': 0, 'Juana': 1, 'Kelly': 1, 'Mei': 1},
        "fac": {'Lateefah': False, 'Olga': True, 'Juana': False, 'Kelly': True, 'Mei': False}
    }
}

for label, opt in options.items():
    if check_option(opt['team'], opt['fac']):
        print(f"Option {label} is valid.")
    else:
        print(f"Option {label} is invalid.")