from z3 import *

def get_base_constraints(pos):
    # pos is a dict mapping singer name to their position (1-6)
    singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
    constraints = []
    # Positions are 1-6
    for s in singers:
        constraints.append(pos[s] >= 1)
        constraints.append(pos[s] <= 6)
    constraints.append(Distinct([pos[s] for s in singers]))
    
    # Condition 1: 4th audition cannot be recorded (K, L are recorded)
    # pos[K] != 4, pos[L] != 4
    constraints.append(pos['K'] != 4)
    constraints.append(pos['L'] != 4)
    
    # Condition 2: 5th audition must be recorded
    # pos[K] == 5 or pos[L] == 5
    constraints.append(Or(pos['K'] == 5, pos['L'] == 5))
    
    # Condition 4: K < T
    constraints.append(pos['K'] < pos['T'])
    
    # Condition 5: Z < Y
    constraints.append(pos['Z'] < pos['Y'])
    
    return constraints

def get_original_condition(pos):
    # Waite's audition must take place earlier than the two recorded auditions (K, L)
    return And(pos['W'] < pos['K'], pos['W'] < pos['L'])

# Define the options
def get_option_constraints(pos, letter):
    if letter == "A":
        # Zinn's audition is the only one that can take place earlier than Waite's.
        # This means for any singer S != Z, pos[S] > pos[W] is NOT necessarily true,
        # but it means if pos[S] < pos[W], then S must be Z.
        # So for all S != Z, pos[S] > pos[W].
        return And([Implies(s != 'Z', pos[s] > pos['W']) for s in ['K', 'L', 'T', 'Y']])
    elif letter == "B":
        # Waite's audition must take place either immediately before or immediately after Zinn's.
        return Or(pos['W'] == pos['Z'] - 1, pos['W'] == pos['Z'] + 1)
    elif letter == "C":
        # Waite's audition must take place earlier than Lugo's.
        return pos['W'] < pos['L']
    elif letter == "D":
        # Waite's audition must be either first or second.
        return Or(pos['W'] == 1, pos['W'] == 2)
    elif letter == "E":
        # The first audition cannot be recorded.
        return And(pos['K'] != 1, pos['L'] != 1)
    return BoolVal(False)

# Check equivalence
# Two conditions C1 and C2 are equivalent under BaseConstraints if:
# (Base + C1) <=> (Base + C2)
# Which is equivalent to:
# (Base + C1) => C2  AND  (Base + C2) => C1

pos = {s: Int(s) for s in ['K', 'L', 'T', 'W', 'Y', 'Z']}
base = get_base_constraints(pos)
orig = get_original_condition(pos)

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    opt = get_option_constraints(pos, letter)
    
    # Check (Base + Orig) => Opt
    s1 = Solver()
    s1.add(base)
    s1.add(orig)
    s1.add(Not(opt))
    
    # Check (Base + Opt) => Orig
    s2 = Solver()
    s2.add(base)
    s2.add(opt)
    s2.add(Not(orig))
    
    if s1.check() == unsat and s2.check() == unsat:
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