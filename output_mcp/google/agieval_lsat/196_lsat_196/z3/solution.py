from z3 import *

# Antiques: H, L, M, S, T, V
# Days: 1, 2, 3, 4, 5, 6
# Variables: day_H, day_L, day_M, day_S, day_T, day_V

def check_option(order):
    # order is a list of antiques in order of days 1-6
    # e.g., ["H", "T", "S", "L", "V", "M"]
    
    # Map antique to day
    day = {}
    for i, antique in enumerate(order):
        day[antique] = i + 1
        
    # 1. The sundial is not auctioned on June 1st.
    if day["S"] == 1:
        return False
        
    # 2. If the harmonica is auctioned on an earlier date than the lamp, 
    #    then the mirror is also auctioned on an earlier date than the lamp.
    if day["H"] < day["L"]:
        if not (day["M"] < day["L"]):
            return False
            
    # 3. The sundial is auctioned on an earlier date than the mirror 
    #    and also on an earlier date than the vase.
    if not (day["S"] < day["M"]):
        return False
    if not (day["S"] < day["V"]):
        return False
        
    # 4. The table is auctioned on an earlier date than the harmonica 
    #    or on an earlier date than the vase, but not both.
    cond1 = (day["T"] < day["H"])
    cond2 = (day["T"] < day["V"])
    if not (cond1 ^ cond2):
        return False
        
    return True

options = {
    "A": ["H", "T", "S", "L", "V", "M"],
    "B": ["L", "H", "S", "M", "V", "T"],
    "C": ["H", "S", "T", "M", "L", "V"],
    "D": ["S", "M", "H", "T", "V", "L"],
    "E": ["V", "S", "L", "H", "T", "M"]
}

valid_options = []
for label, order in options.items():
    if check_option(order):
        valid_options.append(label)

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")