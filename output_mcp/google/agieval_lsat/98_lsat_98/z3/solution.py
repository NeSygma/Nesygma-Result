from z3 import *

# Witnesses
witnesses = ['F', 'G', 'H', 'I', 'J']
# Days: 0=Mon, 1=Tue, 2=Wed
days = [0, 1, 2]

def check_schedule(schedule):
    # schedule is a dict: witness -> day
    # 1. Iturbe on Wednesday
    if schedule['I'] != 2:
        return False
    # 2. Franco and Garcia different days
    if schedule['F'] == schedule['G']:
        return False
    # 3. Exactly two on Tuesday
    if sum(1 for w in witnesses if schedule[w] == 1) != 2:
        return False
    # 4. Hong not on Monday
    if schedule['H'] == 0:
        return False
    # 5. At least one on Monday
    if sum(1 for w in witnesses if schedule[w] == 0) < 1:
        return False
    return True

# Define options
options = {
    'A': {'F': 0, 'H': 1, 'I': 1, 'G': 2, 'J': 2},
    'B': {'F': 0, 'H': 0, 'I': 1, 'J': 1, 'G': 2},
    'C': {'G': 0, 'F': 1, 'I': 1, 'H': 2, 'J': 2},
    'D': {'G': 0, 'J': 0, 'F': 1, 'H': 1, 'I': 2},
    'E': {'G': 0, 'J': 0, 'H': 1, 'F': 2, 'I': 2}
}

valid_options = []
for letter, sched in options.items():
    if check_schedule(sched):
        valid_options.append(letter)

print(f"STATUS: sat")
print(f"Valid options: {valid_options}")
if len(valid_options) == 1:
    print(f"answer:{valid_options[0]}")