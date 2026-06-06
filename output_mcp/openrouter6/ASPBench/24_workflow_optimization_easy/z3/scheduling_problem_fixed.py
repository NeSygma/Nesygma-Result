from z3 import *

# Problem data
tasks = [
    {"id": 0, "duration": 3, "prerequisites": []},
    {"id": 1, "duration": 2, "prerequisites": []},
    {"id": 2, "duration": 4, "prerequisites": [0]},
    {"id": 3, "duration": 1, "prerequisites": [1]},
    {"id": 4, "duration": 5, "prerequisites": [2, 3]},
    {"id": 5, "duration": 2, "prerequisites": [0]},
    {"id": 6, "duration": 3, "prerequisites": [4]},
    {"id": 7, "duration": 2, "prerequisites": [5, 6]}
]

# Extract durations and prerequisites for easier access
durations = [t["duration"] for t in tasks]
prerequisites = [t["prerequisites"] for t in tasks]

# Create solver
opt = Optimize()

# Declare start time variables for each task
start = [Int(f"start_{i}") for i in range(8)]
end = [Int(f"end_{i}") for i in range(8)]

# Add constraints: end_time = start_time + duration
for i in range(8):
    opt.add(end[i] == start[i] + durations[i])

# Add precedence constraints: task cannot start until all prerequisites are completed
for i in range(8):
    for p in prerequisites[i]:
        opt.add(start[i] >= end[p])

# All start times must be non-negative
for i in range(8):
    opt.add(start[i] >= 0)

# Define makespan as the maximum end time
makespan = Int("makespan")
# Use z3.Max to compute maximum of end times
opt.add(makespan == Max(end))

# Minimize makespan
opt.minimize(makespan)

# Check for solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract schedule from model
    schedule = []
    for i in range(8):
        start_val = model[start[i]].as_long()
        end_val = model[end[i]].as_long()
        schedule.append({
            "task": i,
            "start_time": start_val,
            "end_time": end_val
        })
    
    # Extract makespan
    makespan_val = model[makespan].as_long()
    
    # Compute critical path by tracing back from the task that ends at makespan
    # Find the task that ends at makespan
    end_times = [model[end[i]].as_long() for i in range(8)]
    makespan_task = end_times.index(makespan_val)
    
    # Trace back to find critical path
    critical_path = []
    current_task = makespan_task
    
    while True:
        critical_path.insert(0, current_task)
        # Find a prerequisite that ends exactly at the start time of current task
        current_start = model[start[current_task]].as_long()
        prereqs = prerequisites[current_task]
        if not prereqs:
            break
        # Find a prerequisite that ends at current_start (there should be at least one)
        found = False
        for p in prereqs:
            if model[end[p]].as_long() == current_start:
                current_task = p
                found = True
                break
        if not found:
            # If no prerequisite ends exactly at start time, pick the one with the latest end time
            # (this handles cases where multiple prerequisites exist but only one is on critical path)
            latest_end = -1
            latest_p = None
            for p in prereqs:
                p_end = model[end[p]].as_long()
                if p_end > latest_end:
                    latest_end = p_end
                    latest_p = p
            if latest_p is not None:
                current_task = latest_p
            else:
                break
    
    # Print results
    print("STATUS: sat")
    print("\nSchedule:")
    for entry in schedule:
        print(f"  Task {entry['task']}: start={entry['start_time']}, end={entry['end_time']}")
    
    print(f"\nMakespan: {makespan_val}")
    print(f"Critical path: {critical_path}")
    
    # Verify critical path length equals makespan
    critical_path_length = sum(durations[t] for t in critical_path)
    print(f"Critical path length: {critical_path_length}")
    
    # Additional verification: check that all constraints are satisfied
    print("\nVerification:")
    for i in range(8):
        start_val = model[start[i]].as_long()
        end_val = model[end[i]].as_long()
        print(f"  Task {i}: start={start_val}, end={end_val}, duration={durations[i]}, " +
              f"end-start={end_val-start_val}, matches duration={end_val-start_val == durations[i]}")
        # Check precedence constraints
        for p in prerequisites[i]:
            p_end = model[end[p]].as_long()
            print(f"    Prerequisite {p} ends at {p_end}, start of {i} is {start_val}, " +
                  f"constraint satisfied: {p_end <= start_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")