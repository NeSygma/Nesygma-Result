from z3 import *

# Movies: 0:Horror, 1:Mystery, 2:Romance, 3:Sci-fi, 4:Western
# Slots: 0:(1,7), 1:(1,9), 2:(2,7), 3:(2,9), 4:(3,8)
# Times: 0:7, 1:9, 2:7, 3:9, 4:8
# Screens: 0:1, 1:1, 2:2, 3:2, 4:3

slot_time = [7, 9, 7, 9, 8]
slot_screen = [1, 1, 2, 2, 3]

def check_option(m_slots):
    # m_slots is a list where m_slots[m] is the slot index for movie m
    # m_slots[0]=H, m_slots[1]=M, m_slots[2]=R, m_slots[3]=S, m_slots[4]=W
    
    # 1. Western begins before Horror
    if not (slot_time[m_slots[4]] < slot_time[m_slots[0]]):
        return False
    
    # 2. Sci-fi not on screen 3
    if not (slot_screen[m_slots[3]] != 3):
        return False
    
    # 3. Romance not on screen 2
    if not (slot_screen[m_slots[2]] != 2):
        return False
    
    # 4. Horror and Mystery on different screens
    if not (slot_screen[m_slots[0]] != slot_screen[m_slots[1]]):
        return False
        
    # 5. Each movie in a unique slot
    if len(set(m_slots)) != 5:
        return False
        
    return True

# Options:
# (A) S1: R(7), H(9); S2: W(7), S(9); S3: M(8)
# Slots: (1,7)=0, (1,9)=1, (2,7)=2, (2,9)=3, (3,8)=4
# A: R=0, H=1, W=2, S=3, M=4
opt_a = [1, 4, 0, 3, 2]
# (B) S1: M(7), R(9); S2: H(7), S(9); S3: W(8)
# B: M=0, R=1, H=2, S=3, W=4
opt_b = [2, 0, 1, 3, 4]
# (C) S1: W(7), S(9); S2: M(7), H(9); S3: R(8)
# C: W=0, S=1, M=2, H=3, R=4
opt_c = [3, 2, 4, 1, 0]
# (D) S1: R(7), M(9); S2: W(7), H(9); S3: S(8)
# D: R=0, M=1, W=2, H=3, S=4
opt_d = [3, 1, 0, 4, 2]
# (E) S1: W(7), M(9); S2: S(7), R(9); S3: H(8)
# E: W=0, M=1, S=2, R=3, H=4
opt_e = [4, 1, 3, 2, 0]

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found = []
for name, m_slots in options:
    if check_option(m_slots):
        found.append(name)

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")