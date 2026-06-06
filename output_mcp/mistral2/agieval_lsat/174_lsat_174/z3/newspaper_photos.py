from z3 import *

# Initialize solver
solver = Solver()

# Define photographers as integers for simplicity
# 0: Fuentes, 1: Gagnon, 2: Hue
Fuentes, Gagnon, Hue = 0, 1, 2

# Sections: Lifestyle, Metro, Sports
# Each section has 2 photographs, so we use a list of 2 integers per section
Lifestyle = [Int(f'Lifestyle_{i}') for i in range(2)]
Metro = [Int(f'Metro_{i}') for i in range(2)]
Sports = [Int(f'Sports_{i}') for i in range(2)]

# Add constraints for the given condition: one Metro photo is by Fuentes and one by Hue
solver.add(Or(And(Metro[0] == Fuentes, Metro[1] == Hue),
              And(Metro[0] == Hue, Metro[1] == Fuentes)))

# Constraint: Each photographer must have at least 1 and at most 3 photos in total
photographers = [Fuentes, Gagnon, Hue]
total_photos = [0, 0, 0]

# Count total photos per photographer
for section in [Lifestyle, Metro, Sports]:
    for photo in section:
        for idx, p in enumerate(photographers):
            total_photos[idx] += If(photo == p, 1, 0)

for p in photographers:
    solver.add(total_photos[p] >= 1, total_photos[p] <= 3)

# Constraint: At least one photographer in Lifestyle must also have a photo in Metro
lifestyle_photographers = [Lifestyle[0], Lifestyle[1]]
metro_photographers = [Metro[0], Metro[1]]
solver.add(Or([p_l == p_m for p_l in lifestyle_photographers for p_m in metro_photographers]))

# Constraint: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
hue_in_lifestyle = Sum([If(p == Hue, 1, 0) for p in Lifestyle])
fuentes_in_sports = Sum([If(p == Fuentes, 1, 0) for p in Sports])
solver.add(hue_in_lifestyle == fuentes_in_sports)

# Constraint: None of Gagnon's photos can be in Sports
for p in Sports:
    solver.add(p != Gagnon)

# Now evaluate each option
options = [
    ("A", And(Lifestyle[0] == Fuentes, Lifestyle[1] == Fuentes)),
    ("B", And(Lifestyle[0] == Gagnon, Lifestyle[1] == Gagnon)),
    ("C", And(Or(Lifestyle[0] == Gagnon, Lifestyle[1] == Gagnon),
              Or(Lifestyle[0] == Hue, Lifestyle[1] == Hue))),
    ("D", And(Lifestyle[0] == Hue, Lifestyle[1] == Hue)),
    ("E", And(Sports[0] == Fuentes, Sports[1] == Fuentes))
]

found_options = []
for letter, constr in options:
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