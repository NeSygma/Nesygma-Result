from z3 import *

# Create solver
solver = Solver()

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
J, K, L, N, O, R = 0, 1, 2, 3, 4, 5  # indices for convenience

# Variables: day[assistant] (0=Wed, 1=Thu, 2=Fri), time[assistant] (0=morning, 1=afternoon)
day = [Int(f"day_{a}") for a in assistants]
time = [Int(f"time_{a}") for a in assistants]

# Domain constraints for days and times
for i in range(6):
    solver.add(day[i] >= 0, day[i] <= 2)  # 0=Wed, 1=Thu, 2=Fri
    solver.add(time[i] >= 0, time[i] <= 1)  # 0=morning, 1=afternoon

# Constraint 1: Kevin and Rebecca same day
solver.add(day[K] == day[R])

# Constraint 2: Lan and Olivia different days
solver.add(day[L] != day[O])

# Constraint 3: Nessa afternoon
solver.add(time[N] == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(day[J] < day[O])

# Constraint 5: Kevin's day is day before Nessa's
solver.add(day[K] == day[N] - 1)

# Additional: All sessions must be distinct (each day-time combination used exactly once)
for i in range(6):
    for j in range(i+1, 6):
        solver.add(Or(day[i] != day[j], time[i] != time[j]))

# Now define the options as sets of assistants
options = {
    "A": [J, N],  # Julio, Nessa
    "B": [K, R],  # Kevin, Rebecca
    "C": [K, N, R],  # Kevin, Nessa, Rebecca
    "D": [J, K, N, R],  # Julio, Kevin, Nessa, Rebecca
    "E": [J, K, L, N, R]  # Julio, Kevin, Lan, Nessa, Rebecca
}

# For each option, check if it's the complete and accurate list
found_options = []

for letter, option_assistants in options.items():
    # First, check if each assistant in the option CAN lead Thursday afternoon
    all_in_option_possible = True
    for a in option_assistants:
        s = Solver()
        # Add all base constraints
        for i in range(6):
            s.add(day[i] >= 0, day[i] <= 2)
            s.add(time[i] >= 0, time[i] <= 1)
        s.add(day[K] == day[R])
        s.add(day[L] != day[O])
        s.add(time[N] == 1)
        s.add(day[J] < day[O])
        s.add(day[K] == day[N] - 1)
        for i in range(6):
            for j in range(i+1, 6):
                s.add(Or(day[i] != day[j], time[i] != time[j]))
        
        # Add constraint that this assistant leads Thursday afternoon
        s.add(day[a] == 1)  # Thursday
        s.add(time[a] == 1)  # afternoon
        
        if s.check() != sat:
            all_in_option_possible = False
            break
    
    if not all_in_option_possible:
        continue  # This option is invalid
    
    # Second, check if each assistant NOT in the option CANNOT lead Thursday afternoon
    all_outside_option_impossible = True
    for a in range(6):
        if a in option_assistants:
            continue  # Skip assistants in the option
        
        s = Solver()
        # Add all base constraints
        for i in range(6):
            s.add(day[i] >= 0, day[i] <= 2)
            s.add(time[i] >= 0, time[i] <= 1)
        s.add(day[K] == day[R])
        s.add(day[L] != day[O])
        s.add(time[N] == 1)
        s.add(day[J] < day[O])
        s.add(day[K] == day[N] - 1)
        for i in range(6):
            for j in range(i+1, 6):
                s.add(Or(day[i] != day[j], time[i] != time[j]))
        
        # Add constraint that this assistant leads Thursday afternoon
        s.add(day[a] == 1)  # Thursday
        s.add(time[a] == 1)  # afternoon
        
        if s.check() == sat:
            # This assistant outside the option CAN lead Thursday afternoon
            # So the option is not complete
            all_outside_option_impossible = False
            break
    
    if all_outside_option_impossible:
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