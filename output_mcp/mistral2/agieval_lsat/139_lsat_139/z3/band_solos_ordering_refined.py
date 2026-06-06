from z3 import *

solver = Solver()

# Assign unique integer IDs to each musician
guitarist = 0
keyboard_player = 1
percussionist = 2
saxophonist = 3
trumpeter = 4
violinist = 5

# Solo positions: 0 to 5 (first to last)
solo_positions = [Int(f'solo_{i}') for i in range(6)]

# Each position must be assigned to exactly one musician
for pos in solo_positions:
    solver.add(Or([pos == m for m in [guitarist, keyboard_player, percussionist, saxophonist, trumpeter, violinist]]))

# All musicians must be assigned to exactly one position
for m in [guitarist, keyboard_player, percussionist, saxophonist, trumpeter, violinist]:
    solver.add(Sum([If(pos == m, 1, 0) for pos in solo_positions]) == 1)

# Constraint 1: The guitarist does not perform the fourth solo (position 3)
solver.add(solo_positions[3] != guitarist)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
# Find the positions of percussionist and keyboard player
percussionist_pos = Int('percussionist_pos')
keyboard_player_pos = Int('keyboard_player_pos')

solver.add(Or([And(solo_positions[i] == percussionist, percussionist_pos == i) for i in range(6)]))
solver.add(Or([And(solo_positions[i] == keyboard_player, keyboard_player_pos == i) for i in range(6)]))

solver.add(percussionist_pos < keyboard_player_pos)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does
violinist_pos = Int('violinist_pos')
guitarist_pos = Int('guitarist_pos')

solver.add(Or([And(solo_positions[i] == violinist, violinist_pos == i) for i in range(6)]))
solver.add(Or([And(solo_positions[i] == guitarist, guitarist_pos == i) for i in range(6)]))

solver.add(violinist_pos < keyboard_player_pos)
solver.add(keyboard_player_pos < guitarist_pos)

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both
trumpeter_pos = Int('trumpeter_pos')
saxophonist_pos = Int('saxophonist_pos')

solver.add(Or([And(solo_positions[i] == trumpeter, trumpeter_pos == i) for i in range(6)]))
solver.add(Or([And(solo_positions[i] == saxophonist, saxophonist_pos == i) for i in range(6)]))

# Saxophonist must be after percussionist OR trumpeter, but not both
solver.add(Or(
    And(saxophonist_pos > percussionist_pos, saxophonist_pos <= trumpeter_pos),
    And(saxophonist_pos > trumpeter_pos, saxophonist_pos <= percussionist_pos)
))

# Exactly one of the two conditions must hold (not both)
solver.add(Not(And(saxophonist_pos > percussionist_pos, saxophonist_pos > trumpeter_pos)))

# Helper function to create constraints for each option
def get_option_constraints(option_list):
    constraints = []
    for i, musician in enumerate(option_list):
        constraints.append(solo_positions[i] == musician)
    return constraints

# Define the options as lists of musician IDs in order
option_A = [violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard_player]
option_B = [percussionist, violinist, keyboard_player, trumpeter, saxophonist, guitarist]
option_C = [violinist, trumpeter, saxophonist, percussionist, keyboard_player, guitarist]
option_D = [keyboard_player, trumpeter, violinist, saxophonist, guitarist, percussionist]
option_E = [guitarist, violinist, keyboard_player, percussionist, saxophonist, trumpeter]

# Evaluate each option
found_options = []
for letter, option_list in [("A", option_A), ("B", option_B), ("C", option_C), ("D", option_D), ("E", option_E)]:
    solver.push()
    # Add constraints to match the current option
    for i, musician in enumerate(option_list):
        solver.add(solo_positions[i] == musician)
    # Check if the constraints are satisfiable
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