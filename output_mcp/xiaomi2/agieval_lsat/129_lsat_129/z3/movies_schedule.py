from z3 import *

# Movies: horror=0, mystery=1, romance=2, sci-fi=3, western=4
# Each movie gets a screen (1,2,3) and a time
# Screen 1: 7pm(19), 9pm(21)
# Screen 2: 7pm(19), 9pm(21)
# Screen 3: 8pm(20)

# We model each movie's screen and time
# There are 5 slots total:
#   slot 0: screen 1, 7pm (time 19)
#   slot 1: screen 1, 9pm (time 21)
#   slot 2: screen 2, 7pm (time 19)
#   slot 3: screen 2, 9pm (time 21)
#   slot 4: screen 3, 8pm (time 20)

# Each movie assigned to exactly one slot (0-4), all different
# slot_to_screen = [1, 1, 2, 2, 3]
# slot_to_time  = [19, 21, 19, 21, 20]

slot_screen = [1, 1, 2, 2, 3]
slot_time   = [19, 21, 19, 21, 20]

def build_base():
    """Return solver with all base constraints."""
    s = Solver()
    
    # movie slot assignments: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
    slot = [Int(f'slot_{m}') for m in range(5)]
    movie_names = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
    
    # Each movie in exactly one slot (0-4), all different
    for i in range(5):
        s.add(slot[i] >= 0, slot[i] <= 4)
    s.add(Distinct(slot))
    
    # Helper: screen of movie i
    def screen_of(i):
        return If(slot[i] == 0, 1,
               If(slot[i] == 1, 1,
               If(slot[i] == 2, 2,
               If(slot[i] == 3, 2, 3))))
    
    # Helper: time of movie i
    def time_of(i):
        return If(slot[i] == 0, 19,
               If(slot[i] == 1, 21,
               If(slot[i] == 2, 19,
               If(slot[i] == 3, 21, 20))))
    
    # Constraint 1: Western (4) begins before Horror (0)
    s.add(time_of(4) < time_of(0))
    
    # Constraint 2: Sci-fi (3) not on screen 3
    s.add(screen_of(3) != 3)
    
    # Constraint 3: Romance (2) not on screen 2
    s.add(screen_of(2) != 2)
    
    # Constraint 4: Horror (0) and Mystery (1) on different screens
    s.add(screen_of(0) != screen_of(1))
    
    return s, slot, movie_names

# Define what each option means for screen 2
# Screen 2 has slots 2 (7pm) and 3 (9pm)
# Option A: sci-fi at 7pm on screen 2, horror at 9pm on screen 2 => slot[3]=2, slot[0]=3
# Option B: sci-fi at 7pm on screen 2, mystery at 9pm on screen 2 => slot[3]=2, slot[1]=3
# Option C: sci-fi at 7pm on screen 2, western at 9pm on screen 2 => slot[3]=2, slot[4]=3
# Option D: western at 7pm on screen 2, horror at 9pm on screen 2 => slot[4]=2, slot[0]=3
# Option E: western at 7pm on screen 2, mystery at 9pm on screen 2 => slot[4]=2, slot[1]=3

options = [
    ("A", lambda slot: And(slot[3] == 2, slot[0] == 3)),  # sci-fi, horror
    ("B", lambda slot: And(slot[3] == 2, slot[1] == 3)),  # sci-fi, mystery
    ("C", lambda slot: And(slot[3] == 2, slot[4] == 3)),  # sci-fi, western
    ("D", lambda slot: And(slot[4] == 2, slot[0] == 3)),  # western, horror
    ("E", lambda slot: And(slot[4] == 2, slot[1] == 3)),  # western, mystery
]

found_options = []
for letter, constr_fn in options:
    s, slot, movie_names = build_base()
    s.push()
    s.add(constr_fn(slot))
    if s.check() == sat:
        m = s.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT - schedule:")
        for i in range(5):
            sv = m[slot[i]].as_long()
            print(f"  {movie_names[i]} -> screen {slot_screen[sv]}, time {slot_time[sv]}:00")
    else:
        print(f"Option {letter}: UNSAT - cannot be scheduled")
    s.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")