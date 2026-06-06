from z3 import *

solver = Solver()

# People indices
JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA = 0, 1, 2, 3, 4, 5
NAMES = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# Each person gets a session slot 0-5
# Slots: 0=WedAM, 1=WedPM, 2=ThuAM, 3=ThuPM, 4=FriAM, 5=FriPM
sessions = [Int(f'session_{i}') for i in range(6)]

# Each session assigned to a different person (bijection: 6 people, 6 slots)
solver.add(Distinct(sessions))

# Domain: each session is 0-5
for s in sessions:
    solver.add(s >= 0, s <= 5)

# Helper: day of session (0=Wed, 1=Thu, 2=Fri)
def day_of_session(s):
    return s / 2

# Helper: time of session (0=AM, 1=PM)
def time_of_session(s):
    return s % 2

# Constraint 1: Kevin and Rebecca same day
solver.add(day_of_session(sessions[KEVIN]) == day_of_session(sessions[REBECCA]))

# Constraint 2: Lan and Olivia different day
solver.add(day_of_session(sessions[LAN]) != day_of_session(sessions[OLIVIA]))

# Constraint 3: Nessa must lead an afternoon session (time == 1)
solver.add(time_of_session(sessions[NESSA]) == 1)

# Constraint 4: Julio earlier day than Olivia
solver.add(day_of_session(sessions[JULIO]) < day_of_session(sessions[OLIVIA]))

# Additional condition: Lan does not lead a Wednesday session
solver.add(day_of_session(sessions[LAN]) != 0)

# Now test each option: which person MUST be on Thursday?
# For each candidate, add constraint "person is NOT on Thursday".
# If that makes the problem UNSAT, then that person MUST be on Thursday.
found_options = []

for letter, person_idx in [("A", REBECCA), ("B", OLIVIA), ("C", NESSA), ("D", KEVIN), ("E", JULIO)]:
    solver.push()
    # Constraint: this person is NOT on Thursday
    solver.add(day_of_session(sessions[person_idx]) != 1)
    result = solver.check()
    if result == unsat:
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