from z3 import *

# Solver
solver = Solver()

# Constants for sections and photographers
Lifestyle, Metro, Sports = 0,1,2
Fuentes, Gagnon, Hue = 0,1,2

# 6 photos indexed 0..5
photos = list(range(6))
# Variables
section = [Int(f'sec_{i}') for i in photos]
photographer = [Int(f'ph_{i}') for i in photos]

# Section domain 0..2
for i in photos:
    solver.add(Or(section[i]==Lifestyle, section[i]==Metro, section[i]==Sports))
    solver.add(Or(photographer[i]==Fuentes, photographer[i]==Gagnon, photographer[i]==Hue))

# Exactly 2 photos per section
for sec in [Lifestyle, Metro, Sports]:
    solver.add(Sum([If(section[i]==sec, 1, 0) for i in photos]) == 2)

# Photographer counts between 1 and 3
for ph in [Fuentes, Gagnon, Hue]:
    count_ph = Sum([If(photographer[i]==ph, 1, 0) for i in photos])
    solver.add(count_ph >= 1, count_ph <= 3)

# None of Gagnon's photos in Sports
for i in photos:
    solver.add(Implies(photographer[i]==Gagnon, section[i]!=Sports))

# At least one photo in Lifestyle must be by a photographer who has at least one photo in Metro
# For each photographer p, check if they have at least one in both Lifestyle and Metro
conds = []
for ph in [Fuentes, Gagnon, Hue]:
    has_lifestyle = Sum([If(And(photographer[i]==ph, section[i]==Lifestyle), 1, 0) for i in photos])
    has_metro = Sum([If(And(photographer[i]==ph, section[i]==Metro), 1, 0) for i in photos])
    conds.append(And(has_lifestyle >= 1, has_metro >= 1))
solver.add(Or(conds))

# Hue's photos in Lifestyle equal Fuentes photos in Sports
hue_lifestyle = Sum([If(And(photographer[i]==Hue, section[i]==Lifestyle), 1, 0) for i in photos])
fuentes_sports = Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos])
solver.add(hue_lifestyle == fuentes_sports)

# Option constraints
opt_a = And(
    Sum([If(And(photographer[i]==Fuentes, section[i]==Lifestyle), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Metro), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos]) == 1
)
opt_b = And(
    Sum([If(And(photographer[i]==Fuentes, section[i]==Lifestyle), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos]) == 2,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Metro), 1, 0) for i in photos]) == 0
)
opt_c = And(
    Sum([If(And(photographer[i]==Fuentes, section[i]==Lifestyle), 1, 0) for i in photos]) == 2,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Metro), 1, 0) for i in photos]) == 0
)
opt_d = And(
    Sum([If(And(photographer[i]==Fuentes, section[i]==Metro), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos]) == 2,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Lifestyle), 1, 0) for i in photos]) == 0
)
opt_e = And(
    Sum([If(And(photographer[i]==Fuentes, section[i]==Metro), 1, 0) for i in photos]) == 2,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Sports), 1, 0) for i in photos]) == 1,
    Sum([If(And(photographer[i]==Fuentes, section[i]==Lifestyle), 1, 0) for i in photos]) == 0
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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