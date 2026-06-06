from z3 import *

solver = Solver()

# Students: Franz (F), Greene (G), Hidalgo (H), Isaacs (I)
students = ['F', 'G', 'H', 'I']

# Walls: 1, 2, 3, 4
walls = [1, 2, 3, 4]

# Positions: 0 = upper, 1 = lower
positions = [0, 1]

# Each student has exactly two paintings: an oil and a watercolor.
# We'll model each painting as a pair (student, medium) placed on a (wall, position).
# Let's use variables:
# For each student s and medium m (0=oil, 1=watercolor), we have wall[s][m] and pos[s][m]
# wall[s][m] = which wall (1-4)
# pos[s][m] = which position (0=upper, 1=lower)

wall = {}
pos = {}
for s in students:
    for m in [0, 1]:  # 0=oil, 1=watercolor
        wall[(s, m)] = Int(f'wall_{s}_{m}')
        pos[(s, m)] = Int(f'pos_{s}_{m}')
        solver.add(wall[(s, m)] >= 1, wall[(s, m)] <= 4)
        solver.add(pos[(s, m)] >= 0, pos[(s, m)] <= 1)

# Exactly two paintings on each wall, one upper and one lower.
# So for each wall w, exactly one painting is upper and exactly one is lower.
# We'll enforce this via the assignment constraints.

# Each wall has exactly 2 paintings (one upper, one lower)
# So for each wall, exactly 2 of the 8 paintings are assigned to it.
# And for each wall, exactly one painting is upper and exactly one is lower.

# Let's use a different approach: assign each painting to a unique (wall, position) slot.
# There are 4 walls * 2 positions = 8 slots. Each of the 8 paintings gets a unique slot.

# We can think of it as: for each student s and medium m, we assign a wall and position.
# The 8 assignments must be a bijection to the 8 slots.

# Enforce that each (wall, position) pair gets exactly one painting.
# We'll use a counting constraint: for each wall w and position p, exactly one painting is assigned there.

for w in walls:
    for p in positions:
        # Count how many paintings have wall=w and pos=p
        count = Sum([If(And(wall[(s, m)] == w, pos[(s, m)] == p), 1, 0) for s in students for m in [0, 1]])
        solver.add(count == 1)

# Condition 1: No wall has only watercolors displayed on it.
# So on each wall, at least one painting is an oil.
for w in walls:
    # At least one painting on wall w is an oil (m=0)
    solver.add(Or([And(wall[(s, 0)] == w) for s in students]))

# Condition 2: No wall has the work of only one student displayed on it.
# So on each wall, the two paintings are by different students.
for w in walls:
    # For each pair of distinct students, they can't both be on the same wall... 
    # Actually simpler: for each wall, the two students must be different.
    # We need to ensure that for each wall, there are at least 2 different students.
    # Equivalent: it's not the case that both paintings on wall w are by the same student.
    for s in students:
        # It's not the case that both paintings on wall w are by student s
        solver.add(Not(And(
            Or([And(wall[(s, 0)] == w, wall[(s, 1)] == w)]),
            # Actually both paintings on wall w could be by s only if s has both paintings on w
            # But s has exactly 2 paintings (oil and watercolor). So both on same wall means both are on w.
            # Let's just say: for each wall w, the two paintings are by different students.
        )))
    # Better: For each wall w, the set of students with paintings on w has size >= 2.
    # Count distinct students on wall w:
    # For each student s, check if s has any painting on wall w.
    # Then require at least 2 such students.
    student_on_wall = [Or([And(wall[(s, m)] == w) for m in [0, 1]]) for s in students]
    solver.add(Sum([If(cond, 1, 0) for cond in student_on_wall]) >= 2)

# Condition 3: No wall has both a painting by Franz and a painting by Isaacs displayed on it.
for w in walls:
    solver.add(Not(And(
        Or([And(wall[('F', m)] == w) for m in [0, 1]]),
        Or([And(wall[('I', m)] == w) for m in [0, 1]])
    )))

# Condition 4: Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed.
# So: wall(G, watercolor) = wall(F, oil) AND pos(G, watercolor) = 0 (upper)
solver.add(wall[('G', 1)] == wall[('F', 0)])
solver.add(pos[('G', 1)] == 0)

# Condition 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(wall[('I', 0)] == 4)
solver.add(pos[('I', 0)] == 1)

# Now evaluate each option.
# Each option gives a list of paintings in the lower position on walls 1 through 4.
# We need to check if the option is consistent with all constraints.

# Helper: parse option strings
# Each option is like "Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil"
# meaning lower position on wall 1, 2, 3, 4 respectively.

def parse_option(opt_str):
    """Return list of (student, medium) for walls 1..4 lower position."""
    mapping = {
        "Franz's oil": ('F', 0),
        "Franz's watercolor": ('F', 1),
        "Greene's oil": ('G', 0),
        "Greene's watercolor": ('G', 1),
        "Hidalgo's oil": ('H', 0),
        "Hidalgo's watercolor": ('H', 1),
        "Isaacs's oil": ('I', 0),
        "Isaacs's watercolor": ('I', 1),
    }
    parts = [p.strip() for p in opt_str.split(',')]
    return [mapping[p] for p in parts]

options = {
    "A": "Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil",
    "B": "Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil",
    "C": "Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil",
    "D": "Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil",
    "E": "Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil",
}

found_options = []
for letter, opt_str in options.items():
    parsed = parse_option(opt_str)
    solver.push()
    # For each wall w (1-indexed), the lower position (pos=1) must have the specified painting
    for w_idx, (s, m) in enumerate(parsed):
        wall_num = w_idx + 1
        solver.add(wall[(s, m)] == wall_num)
        solver.add(pos[(s, m)] == 1)
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