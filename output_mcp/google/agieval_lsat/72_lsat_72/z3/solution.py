from z3 import *

# Assistants
assistants = ['J', 'K', 'L', 'N', 'O', 'R']
# Days: 0=Wed, 1=Thu, 2=Fri
# Times: 0=AM, 1=PM

def solve():
    solver = Solver()
    
    # Variables
    day = {a: Int(f'day_{a}') for a in assistants}
    time = {a: Int(f'time_{a}') for a in assistants}
    
    # Domains
    for a in assistants:
        solver.add(day[a] >= 0, day[a] <= 2)
        solver.add(time[a] >= 0, time[a] <= 1)
        
    # Each session is unique (day, time)
    # There are 6 assistants and 6 slots (3 days * 2 times)
    # So all (day, time) pairs must be distinct
    for i in range(len(assistants)):
        for j in range(i + 1, len(assistants)):
            a1, a2 = assistants[i], assistants[j]
            solver.add(Not(And(day[a1] == day[a2], time[a1] == time[a2])))
            
    # Constraints
    # 1. Kevin and Rebecca must lead sessions that meet on the same day.
    solver.add(day['K'] == day['R'])
    
    # 2. Lan and Olivia cannot lead sessions that meet on the same day.
    solver.add(day['L'] != day['O'])
    
    # 3. Nessa must lead an afternoon session.
    solver.add(time['N'] == 1)
    
    # 4. Julio's session must meet on an earlier day of the week than Olivia's.
    solver.add(day['J'] < day['O'])
    
    # Condition: Lan does not lead a Wednesday session
    solver.add(day['L'] != 0)
    
    # Check each option: "Who must lead a Thursday session?"
    # Thursday is day 1.
    # We want to find which assistant X MUST have day[X] == 1.
    # This means for all valid models, day[X] == 1.
    # Or: there is no valid model where day[X] != 1.
    
    options = {
        'A': 'R',
        'B': 'O',
        'C': 'N',
        'D': 'K',
        'E': 'J'
    }
    
    valid_options = []
    for label, assistant in options.items():
        solver.push()
        # Add constraint that this assistant does NOT lead a Thursday session
        solver.add(day[assistant] != 1)
        
        # If this is unsatisfiable, then the assistant MUST lead a Thursday session
        if solver.check() == unsat:
            valid_options.append(label)
        solver.pop()
        
    if len(valid_options) == 1:
        print("STATUS: sat")
        print(f"answer:{valid_options[0]}")
    elif len(valid_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {valid_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()