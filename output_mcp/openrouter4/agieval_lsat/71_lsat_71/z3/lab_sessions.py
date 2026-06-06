from z3 import *

solver = Solver()

# Session indices: 0=WedAM, 1=WedPM, 2=ThuAM, 3=ThuPM, 4=FriAM, 5=FriPM
# Day of session i: i // 2  (0=Wed, 1=Thu, 2=Fri)
# Time of session i: i % 2  (0=morning, 1=afternoon)

# Variables: each assistant gets a session number (0-5), all distinct
J, K, L, N, O, R = Ints('J K L N O R')
assistants = [J, K, L, N, O, R]

# Domain constraints: each assistant assigned to a session 0-5
for a in assistants:
    solver.add(a >= 0, a <= 5)

# All sessions assigned to different assistants
solver.add(Distinct(assistants))

# Constraint 1: Kevin and Rebecca must lead sessions that meet on the same day
# day(K) == day(R)  =>  K//2 == R//2
solver.add(K / 2 == R / 2)

# Constraint 2: Lan and Olivia cannot lead sessions that meet on the same day
# day(L) != day(O)  =>  L//2 != O//2
solver.add(L / 2 != O / 2)

# Constraint 3: Nessa must lead an afternoon session
# N % 2 == 1
solver.add(N % 2 == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
# day(J) < day(O)  =>  J//2 < O//2
solver.add(J / 2 < O / 2)

# Now evaluate each option
# Session mapping: 0=WedAM, 1=WedPM, 2=ThuAM, 3=ThuPM, 4=FriAM, 5=FriPM

options = {
    "A": {
        # Wed: Rebecca(AM), Kevin(PM) -> R=0, K=1
        # Thu: Julio(AM), Lan(PM) -> J=2, L=3
        # Fri: Nessa(AM), Olivia(PM) -> N=4, O=5
        0: R, 1: K, 2: J, 3: L, 4: N, 5: O
    },
    "B": {
        # Wed: Olivia(AM), Nessa(PM) -> O=0, N=1
        # Thu: Julio(AM), Lan(PM) -> J=2, L=3
        # Fri: Kevin(AM), Rebecca(PM) -> K=4, R=5
        0: O, 1: N, 2: J, 3: L, 4: K, 5: R
    },
    "C": {
        # Wed: Lan(AM), Kevin(PM) -> L=0, K=1
        # Thu: Rebecca(AM), Julio(PM) -> R=2, J=3
        # Fri: Olivia(AM), Nessa(PM) -> O=4, N=5
        0: L, 1: K, 2: R, 3: J, 4: O, 5: N
    },
    "D": {
        # Wed: Kevin(AM), Rebecca(PM) -> K=0, R=1
        # Thu: Julio(AM), Nessa(PM) -> J=2, N=3
        # Fri: Olivia(AM), Lan(PM) -> O=4, L=5
        0: K, 1: R, 2: J, 3: N, 4: O, 5: L
    },
    "E": {
        # Wed: Julio(AM), Lan(PM) -> J=0, L=1
        # Thu: Olivia(AM), Nessa(PM) -> O=2, N=3
        # Fri: Rebecca(AM), Kevin(PM) -> R=4, K=5
        0: J, 1: L, 2: O, 3: N, 4: R, 5: K
    }
}

found_options = []
for letter, opt_assignments in options.items():
    solver.push()
    # Add constraints that fix each session to its assigned assistant
    for session_idx, assistant_var in opt_assignments.items():
        solver.add(assistant_var == session_idx)
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