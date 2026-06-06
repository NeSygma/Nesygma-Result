from z3 import *

# Problem Data
jobs_data = {
    1: {"due": 20, "weight": 3, "ops": [
        {"dur": 4, "mach": 1, "master": False},
        {"dur": 5, "mach": 3, "master": True},
        {"dur": 3, "mach": 2, "master": False}
    ]},
    2: {"due": 25, "weight": 1, "ops": [
        {"dur": 6, "mach": 2, "master": False},
        {"dur": 4, "mach": 4, "master": False},
        {"dur": 2, "mach": 1, "master": False},
        {"dur": 3, "mach": 3, "master": False}
    ]},
    3: {"due": 22, "weight": 2, "ops": [
        {"dur": 7, "mach": 4, "master": True},
        {"dur": 6, "mach": 1, "master": False},
        {"dur": 2, "mach": 3, "master": False}
    ]},
    4: {"due": 30, "weight": 1, "ops": [
        {"dur": 2, "mach": 3, "master": False},
        {"dur": 5, "mach": 2, "master": False},
        {"dur": 3, "mach": 4, "master": False},
        {"dur": 4, "mach": 1, "master": True}
    ]}
}

opt = Optimize()

# Variables
# start[job_id][op_idx]
start = {}
for j_id, data in jobs_data.items():
    start[j_id] = [Int(f"start_{j_id}_{o}") for o in range(len(data["ops"]))]

# Constraints
for j_id, data in jobs_data.items():
    for o in range(len(data["ops"])):
        # Time horizon
        opt.add(start[j_id][o] >= 0)
        opt.add(start[j_id][o] + data["ops"][o]["dur"] <= 40)
        
        # Precedence
        if o > 0:
            opt.add(start[j_id][o] >= start[j_id][o-1] + data["ops"][o-1]["dur"])
            
        # Maintenance
        m = data["ops"][o]["mach"]
        dur = data["ops"][o]["dur"]
        if m == 2:
            # Unavailable 10-11 inclusive
            opt.add(Or(start[j_id][o] + dur <= 10, start[j_id][o] >= 12))
        elif m == 4:
            # Unavailable 15-16 inclusive
            opt.add(Or(start[j_id][o] + dur <= 15, start[j_id][o] >= 17))

# Machine Exclusivity
all_ops = []
for j_id, data in jobs_data.items():
    for o in range(len(data["ops"])):
        all_ops.append((j_id, o))

for i in range(len(all_ops)):
    for j in range(i + 1, len(all_ops)):
        j1, o1 = all_ops[i]
        j2, o2 = all_ops[j]
        
        # Same machine
        if jobs_data[j1]["ops"][o1]["mach"] == jobs_data[j2]["ops"][o2]["mach"]:
            opt.add(Or(
                start[j1][o1] + jobs_data[j1]["ops"][o1]["dur"] <= start[j2][o2],
                start[j2][o2] + jobs_data[j2]["ops"][o2]["dur"] <= start[j1][o1]
            ))
            
        # Master Operator Exclusivity
        if jobs_data[j1]["ops"][o1]["master"] and jobs_data[j2]["ops"][o2]["master"]:
            opt.add(Or(
                start[j1][o1] + jobs_data[j1]["ops"][o1]["dur"] <= start[j2][o2],
                start[j2][o2] + jobs_data[j2]["ops"][o2]["dur"] <= start[j1][o1]
            ))

# Objective
makespan = Int("makespan")
for j_id, data in jobs_data.items():
    last_op_idx = len(data["ops"]) - 1
    opt.add(makespan >= start[j_id][last_op_idx] + data["ops"][last_op_idx]["dur"])

total_penalty = Int("total_penalty")
penalties = []
for j_id, data in jobs_data.items():
    last_op_idx = len(data["ops"]) - 1
    finish_time = start[j_id][last_op_idx] + data["ops"][last_op_idx]["dur"]
    tardiness = Int(f"tardiness_{j_id}")
    opt.add(tardiness == If(finish_time > data["due"], finish_time - data["due"], 0))
    penalties.append(tardiness * data["weight"])

opt.add(total_penalty == Sum(penalties))
opt.minimize(makespan + total_penalty)

if opt.check() == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Makespan: {m[makespan]}")
    print(f"Total Penalty: {m[total_penalty]}")
    print(f"Total Cost: {m[makespan].as_long() + m[total_penalty].as_long()}")
    for j_id in jobs_data:
        for o in range(len(jobs_data[j_id]["ops"])):
            print(f"Job {j_id} Op {o+1}: Start {m[start[j_id][o]]}, Dur {jobs_data[j_id]['ops'][o]['dur']}, Mach {jobs_data[j_id]['ops'][o]['mach']}")
else:
    print("STATUS: unsat")