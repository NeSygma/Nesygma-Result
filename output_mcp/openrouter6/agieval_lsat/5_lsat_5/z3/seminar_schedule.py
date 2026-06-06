from z3 import *

# Student indices
GEORGE = 0
HELEN = 1
IRVING = 2
KYLE = 3
LENORE = 4
NINA = 5
OLIVIA = 6
ROBERT = 7

# Create solver
solver = Solver()

# Variables for each slot: Monday morning, Monday afternoon, Tuesday morning, Tuesday afternoon, Wednesday morning, Wednesday afternoon
mm = Int('mm')
ma = Int('ma')
tm = Int('tm')
ta = Int('ta')
wm = Int('wm')
wa = Int('wa')

# Domain: each variable must be between 0 and 7 inclusive
solver.add(mm >= 0, mm <= 7)
solver.add(ma >= 0, ma <= 7)
solver.add(tm >= 0, tm <= 7)
solver.add(ta >= 0, ta <= 7)
solver.add(wm >= 0, wm <= 7)
solver.add(wa >= 0, wa <= 7)

# All six slots must be distinct (each student gives at most one report)
solver.add(Distinct([mm, ma, tm, ta, wm, wa]))

# Condition 1: Tuesday is the only day George can give a report
solver.add(mm != GEORGE)
solver.add(ma != GEORGE)
solver.add(wm != GEORGE)
solver.add(wa != GEORGE)

# Condition 2: Neither Olivia nor Robert can give an afternoon report
solver.add(ma != OLIVIA, ma != ROBERT)
solver.add(ta != OLIVIA, ta != ROBERT)
solver.add(wa != OLIVIA, wa != ROBERT)

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday.
# We encode implications for each slot that could be Nina.
# If Nina on Monday morning or afternoon, then Tuesday must have both Helen and Irving.
# We'll create a helper: Tuesday must have Helen and Irving (in some order)
tuesday_has_helen_irving = Or(And(tm == HELEN, ta == IRVING), And(tm == IRVING, ta == HELEN))
# If Nina on Tuesday morning or afternoon, then Wednesday must have both Helen and Irving.
wednesday_has_helen_irving = Or(And(wm == HELEN, wa == IRVING), And(wm == IRVING, wa == HELEN))

# Implications
solver.add(Implies(mm == NINA, tuesday_has_helen_irving))
solver.add(Implies(ma == NINA, tuesday_has_helen_irving))
solver.add(Implies(tm == NINA, wednesday_has_helen_irving))
solver.add(Implies(ta == NINA, wednesday_has_helen_irving))
# If Nina on Wednesday, no condition (so nothing added)

# Additional given: Kyle gives the afternoon report on Tuesday, and Helen gives the afternoon report on Wednesday.
solver.add(ta == KYLE)
solver.add(wa == HELEN)

# Now, we will test each option for the morning reports.
# Options are tuples (mm, tm, wm) for Monday, Tuesday, Wednesday mornings.
options = [
    ("A", (IRVING, LENORE, NINA)),   # A: Irving, Lenore, Nina
    ("B", (LENORE, GEORGE, IRVING)), # B: Lenore, George, Irving
    ("C", (NINA, IRVING, LENORE)),   # C: Nina, Irving, Lenore
    ("D", (ROBERT, GEORGE, IRVING)), # D: Robert, George, Irving
    ("E", (ROBERT, IRVING, LENORE))  # E: Robert, Irving, Lenore
]

found_options = []
for letter, (m_mon, m_tue, m_wed) in options:
    solver.push()
    # Add morning constraints
    solver.add(mm == m_mon)
    solver.add(tm == m_tue)
    solver.add(wm == m_wed)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")