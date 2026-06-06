from z3 import *

# Movies: horror=0, mystery=1, romance=2, sci-fi=3, western=4
# Slots: 0=scr1/7pm, 1=scr1/9pm, 2=scr2/7pm, 3=scr2/9pm, 4=scr3/8pm

slot_screen = [1, 1, 2, 2, 3]
slot_time   = [19, 21, 19, 21, 20]

def build_base():
    s = Solver()
    slot = [Int(f'slot_{m}') for m in range(5)]
    movie_names = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
    
    for i in range(5):
        s.add(slot[i] >= 0, slot[i] <= 4)
    s.add(Distinct(slot))
    
    def screen_of(i):
        return If(slot[i] == 0, 1,
               If(slot[i] == 1, 1,
               If(slot[i] == 2, 2,
               If(slot[i] == 3, 2, 3))))
    
    def time_of(i):
        return If(slot[i] == 0, 19,
               If(slot[i] == 1, 21,
               If(slot[i] == 2, 19,
               If(slot[i] == 3, 21, 20))))
    
    # Western before Horror
    s.add(time_of(4) < time_of(0))
    # Sci-fi not on screen 3
    s.add(screen_of(3) != 3)
    # Romance not on screen 2
    s.add(screen_of(2) != 2)
    # Horror and Mystery on different screens
    s.add(screen_of(0) != screen_of(1))
    
    return s, slot, movie_names

# Screen 2: slot 2 (7pm) and slot 3 (9pm)
options = [
    ("A", lambda slot: And(slot[3] == 2, slot[0] == 3)),  # sci-fi, horror
    ("B", lambda slot: And(slot[3] == 2, slot[1] == 3)),  # sci-fi, mystery
    ("C", lambda slot: And(slot[3] == 2, slot[4] == 3)),  # sci-fi, western
    ("D", lambda slot: And(slot[4] == 2, slot[0] == 3)),  # western, horror
    ("E", lambda slot: And(slot[4] == 2, slot[1] == 3)),  # western, mystery
]

# Find which option CANNOT be valid (is UNSAT)
impossible_options = []
for letter, constr_fn in options:
    s, slot, movie_names = build_base()
    s.push()
    s.add(constr_fn(slot))
    result = s.check()
    if result == sat:
        print(f"Option {letter}: SAT (possible)")
    else:
        print(f"Option {letter}: UNSAT (IMPOSSIBLE)")
        impossible_options.append(letter)
    s.pop()

print()
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")