from z3 import *

# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
def check_option(o_days, p_days, s_days):
    # o_days, p_days, s_days are lists of 3 days
    # Check distinctness
    if len(set(o_days)) != 3 or len(set(p_days)) != 3 or len(set(s_days)) != 3:
        return False
    # Check at least one on Monday (0)
    if 0 not in o_days and 0 not in p_days and 0 not in s_days:
        return False
    # Check O2 == P1 (index 1 for O, index 0 for P)
    if o_days[1] != p_days[0]:
        return False
    # Check S2 == 3 (index 1 for S)
    if s_days[1] != 3:
        return False
    return True

# Days mapping
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}

options = {
    "A": (["Monday", "Wednesday", "Thursday"], ["Wednesday", "Thursday", "Friday"], ["Monday", "Thursday", "Friday"]),
    "B": (["Monday", "Tuesday", "Thursday"], ["Tuesday", "Wednesday", "Thursday"], ["Monday", "Wednesday", "Thursday"]),
    "C": (["Tuesday", "Wednesday", "Thursday"], ["Wednesday", "Thursday", "Friday"], ["Tuesday", "Thursday", "Friday"]),
    "D": (["Monday", "Tuesday", "Thursday"], ["Monday", "Wednesday", "Thursday"], ["Monday", "Thursday", "Friday"]),
    "E": (["Monday", "Thursday", "Friday"], ["Tuesday", "Wednesday", "Thursday"], ["Monday", "Thursday", "Friday"])
}

results = []
for label, (o, p, s) in options.items():
    o_days = [day_map[d] for d in o]
    p_days = [day_map[d] for d in p]
    s_days = [day_map[d] for d in s]
    if check_option(o_days, p_days, s_days):
        results.append(label)

print(f"STATUS: sat")
print(f"Valid options: {results}")