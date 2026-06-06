from z3 import *

# Owners: 0=RealProp,1=Southco,2=Trustcorp
owners = {}
for b in ['G','F','L','K','M','O','Y','Z']:
    owners[b] = Int(f'owner_{b}')
    # domain 0..2
    # We'll add later

solver = Solver()
for b in owners:
    solver.add(owners[b] >= 0, owners[b] <= 2)

# Premise: Trustcorp (2) owns no class2 buildings: L,K,M,O
class2 = ['L','K','M','O']
for b in class2:
    solver.add(owners[b] != 2)

# Define option constraints as functions returning Bool

def opt_A():
    # RealProp owns a class1 building (G or F)
    return Or(owners['G'] == 0, owners['F'] == 0)

def opt_B():
    # Southco owns only class2 buildings: cannot own G,F,Y,Z
    return And(owners['G'] != 1, owners['F'] != 1, owners['Y'] != 1, owners['Z'] != 1)

def opt_C():
    # Approximate: Southco and Trustcorp own at least one building each (i.e., they have interacted?)
    # We'll interpret as Southco owns at least one building and Trustcorp owns at least one building.
    # Since premise ensures Trustcorp owns some buildings (class1 or class3), we just require Southco owns at least one building.
    return Or([owners[b] == 1 for b in owners])

def opt_D():
    # Trustcorp owns Garza Tower (G)
    return owners['G'] == 2

def opt_E():
    # Trustcorp owns Zimmer House (Z)
    return owners['Z'] == 2

options = [
    ("A", opt_A()),
    ("B", opt_B()),
    ("C", opt_C()),
    ("D", opt_D()),
    ("E", opt_E()),
]

found_options = []
for letter, opt in options:
    # Check if premise implies opt i.e., premise & Not(opt) is unsat
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(opt))
    if s.check() == unsat:
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