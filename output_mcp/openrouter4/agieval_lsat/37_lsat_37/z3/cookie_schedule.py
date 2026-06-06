from z3 import *

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

solver = Solver()

# For each option, we'll define the days for each kind
# The options list the days in chronological order (1st batch, 2nd batch, 3rd batch)
options = {
    "A": {
        "oatmeal": (0, 2, 3),     # Monday, Wednesday, Thursday
        "peanut": (2, 3, 4),      # Wednesday, Thursday, Friday
        "sugar": (0, 3, 4)        # Monday, Thursday, Friday
    },
    "B": {
        "oatmeal": (0, 1, 3),     # Monday, Tuesday, Thursday
        "peanut": (1, 2, 3),      # Tuesday, Wednesday, Thursday
        "sugar": (0, 2, 3)        # Monday, Wednesday, Thursday
    },
    "C": {
        "oatmeal": (1, 2, 3),     # Tuesday, Wednesday, Thursday
        "peanut": (2, 3, 4),      # Wednesday, Thursday, Friday
        "sugar": (1, 3, 4)        # Tuesday, Thursday, Friday
    },
    "D": {
        "oatmeal": (0, 1, 3),     # Monday, Tuesday, Thursday
        "peanut": (0, 2, 3),      # Monday, Wednesday, Thursday
        "sugar": (0, 3, 4)        # Monday, Thursday, Friday
    },
    "E": {
        "oatmeal": (0, 3, 4),     # Monday, Thursday, Friday
        "peanut": (1, 2, 3),      # Tuesday, Wednesday, Thursday
        "sugar": (0, 3, 4)        # Monday, Thursday, Friday
    }
}

def check_option(opt_days):
    """Check if a given set of days satisfies all constraints.
    Days are given as (d1, d2, d3) for each kind in chronological order."""
    
    o1, o2, o3 = opt_days["oatmeal"]
    p1, p2, p3 = opt_days["peanut"]
    s1, s2, s3 = opt_days["sugar"]
    
    # Constraint 1: No two batches of the same kind on the same day
    # (already satisfied since we use distinct days in chronological order)
    
    # Constraint 2: At least one batch on Monday (day 0)
    monday_batches = [o1, o2, o3, p1, p2, p3, s1, s2, s3]
    if 0 not in monday_batches:
        return False
    
    # Constraint 3: The second batch of oatmeal = the first batch of peanut butter
    if o2 != p1:
        return False
    
    # Constraint 4: The second batch of sugar is on Thursday (day 3)
    if s2 != 3:
        return False
    
    return True

found_options = []
for letter, days in options.items():
    if check_option(days):
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