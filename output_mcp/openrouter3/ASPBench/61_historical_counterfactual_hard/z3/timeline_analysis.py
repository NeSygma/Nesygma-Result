from z3 import *

# Define the events with their years
events = {
    'ancient_knowledge': 100,
    'fall_of_rome': 476,
    'dark_ages': 500,
    'renaissance': 1300,
    'age_of_sail': 1400,
    'age_of_steam': 1700,
    'discovery_of_new_world': 1492,
    'global_trade_routes': 1550,
    'industrial_revolution': 1760,
    'information_age': 1970,
    'alternate_industrial_revolution': 1780,
    'digital_renaissance': 1980
}

# Create boolean variables for each event in both timelines
original = {}
alternate = {}
for event in events:
    original[event] = Bool(f'orig_{event}')
    alternate[event] = Bool(f'alt_{event}')

# Create solver instances
solver_orig = Solver()
solver_alt = Solver()

# Add year ordering constraints (events can only occur in chronological order)
# This is implicit in the problem but we'll add it for clarity
for event1, year1 in events.items():
    for event2, year2 in events.items():
        if year1 < year2:
            # If event1 occurs after event2, it's a paradox (but we'll let solver handle)
            pass

# Define prerequisites
prerequisites = {
    'fall_of_rome': ['ancient_knowledge'],
    'dark_ages': ['fall_of_rome'],
    'renaissance': ['dark_ages'],
    'age_of_sail': ['renaissance'],
    'age_of_steam': ['renaissance'],
    'discovery_of_new_world': ['age_of_sail'],
    'global_trade_routes': ['age_of_sail'],
    'industrial_revolution': ['age_of_steam'],
    'information_age': ['industrial_revolution'],
    'digital_renaissance': ['alternate_industrial_revolution']
}

# Define pivot groups
pivot_groups = {
    'paradigm': ['age_of_sail', 'age_of_steam']
}

# Define conditional prerequisites
conditional_prereqs = {
    'alternate_industrial_revolution': {
        'requires': 'global_trade_routes',
        'unless': 'age_of_steam'
    }
}

# Add prerequisite constraints for original timeline
for event, prereqs in prerequisites.items():
    if event in original:
        # Event can only occur if all prerequisites occur
        solver_orig.add(Implies(original[event], And([original[p] for p in prereqs])))

# Add pivot constraints for original timeline
for group, events_in_group in pivot_groups.items():
    # At most one event from each pivot group can occur
    for i in range(len(events_in_group)):
        for j in range(i+1, len(events_in_group)):
            solver_orig.add(Or(Not(original[events_in_group[i]]), Not(original[events_in_group[j]])))
    
    # If any event in a pivot group is possible (prerequisites met), exactly one must be chosen
    # We need to check if prerequisites are met for any event in the group
    possible_events = []
    for event in events_in_group:
        if event in prerequisites:
            # Check if prerequisites can be satisfied
            possible_events.append(And([original[p] for p in prerequisites[event]]))
        else:
            # No prerequisites, always possible
            possible_events.append(True)
    
    # If any event is possible, exactly one must occur
    any_possible = Or(possible_events)
    exactly_one = Or([And(original[e], *[Not(original[other]) for other in events_in_group if other != e]) 
                     for e in events_in_group])
    solver_orig.add(Implies(any_possible, exactly_one))

# Add conditional prerequisite constraints for original timeline
for event, condition in conditional_prereqs.items():
    if event in original:
        requires = condition['requires']
        unless = condition['unless']
        # Event requires 'requires' UNLESS 'unless' occurs
        # This means: if event occurs, then (requires occurs OR unless occurs)
        solver_orig.add(Implies(original[event], Or(original[requires], original[unless])))

# Add intervention: prevent age_of_sail in alternate timeline
solver_alt.add(Not(alternate['age_of_sail']))

# Add prerequisite constraints for alternate timeline
for event, prereqs in prerequisites.items():
    if event in alternate:
        solver_alt.add(Implies(alternate[event], And([alternate[p] for p in prereqs])))

# Add pivot constraints for alternate timeline
for group, events_in_group in pivot_groups.items():
    # At most one event from each pivot group can occur
    for i in range(len(events_in_group)):
        for j in range(i+1, len(events_in_group)):
            solver_alt.add(Or(Not(alternate[events_in_group[i]]), Not(alternate[events_in_group[j]])))
    
    # If any event in a pivot group is possible (prerequisites met), exactly one must be chosen
    possible_events = []
    for event in events_in_group:
        if event in prerequisites:
            possible_events.append(And([alternate[p] for p in prerequisites[event]]))
        else:
            possible_events.append(True)
    
    any_possible = Or(possible_events)
    exactly_one = Or([And(alternate[e], *[Not(alternate[other]) for other in events_in_group if other != e]) 
                     for e in events_in_group])
    solver_alt.add(Implies(any_possible, exactly_one))

# Add conditional prerequisite constraints for alternate timeline
for event, condition in conditional_prereqs.items():
    if event in alternate:
        requires = condition['requires']
        unless = condition['unless']
        solver_alt.add(Implies(alternate[event], Or(alternate[requires], alternate[unless])))

# Add deterministic pivot selection rule for original timeline
# "In the original timeline, when multiple pivot events are possible, choose the one with the earliest year"
# This means: if both age_of_sail and age_of_steam are possible, choose age_of_sail (earlier year)
# We need to model this as a constraint
for group, events_in_group in pivot_groups.items():
    # Sort events by year
    sorted_events = sorted(events_in_group, key=lambda e: events[e])
    # For each pair, if earlier event is possible, it should be chosen over later ones
    for i in range(len(sorted_events)):
        for j in range(i+1, len(sorted_events)):
            earlier = sorted_events[i]
            later = sorted_events[j]
            # If earlier is possible (prerequisites met), then later should not occur
            if earlier in prerequisites:
                earlier_possible = And([original[p] for p in prerequisites[earlier]])
            else:
                earlier_possible = True
            solver_orig.add(Implies(earlier_possible, Not(original[later])))

# Check original timeline
print("=== ORIGINAL TIMELINE ===")
result_orig = solver_orig.check()
if result_orig == sat:
    model_orig = solver_orig.model()
    original_events = []
    for event in events:
        if is_true(model_orig[original[event]]):
            original_events.append((event, events[event]))
    original_events.sort(key=lambda x: x[1])  # Sort by year
    print("STATUS: sat")
    print("original_timeline:", [e[0] for e in original_events])
elif result_orig == unsat:
    print("STATUS: unsat")
    print("No valid original timeline exists")
else:
    print("STATUS: unknown")

# Check alternate timeline
print("\n=== ALTERNATE TIMELINE ===")
result_alt = solver_alt.check()
if result_alt == sat:
    model_alt = solver_alt.model()
    alternate_events = []
    for event in events:
        if is_true(model_alt[alternate[event]]):
            alternate_events.append((event, events[event]))
    alternate_events.sort(key=lambda x: x[1])  # Sort by year
    print("STATUS: sat")
    print("alternate_timeline:", [e[0] for e in alternate_events])
elif result_alt == unsat:
    print("STATUS: unsat")
    print("No valid alternate timeline exists")
else:
    print("STATUS: unknown")

# Calculate differences and paradoxes
if result_orig == sat and result_alt == sat:
    orig_set = set(e[0] for e in original_events)
    alt_set = set(e[0] for e in alternate_events)
    
    prevented = sorted(list(orig_set - alt_set))
    activated = sorted(list(alt_set - orig_set))
    
    print("\n=== DIFFERENCES ===")
    print("prevented_events:", prevented)
    print("activated_events:", activated)
    
    # Check for paradoxes (logical impossibilities)
    # A paradox would be if the same event occurs in both timelines but violates constraints
    # For now, we'll check if the alternate timeline violates any original constraints
    paradoxes = []
    
    # Check if alternate timeline violates original pivot exclusivity
    for group, events_in_group in pivot_groups.items():
        orig_pivot_events = [e for e in events_in_group if e in orig_set]
        alt_pivot_events = [e for e in events_in_group if e in alt_set]
        if len(orig_pivot_events) > 1 or len(alt_pivot_events) > 1:
            paradoxes.append(f"Multiple events in pivot group {group}")
    
    # Check if alternate timeline violates original conditional prerequisites
    for event, condition in conditional_prereqs.items():
        if event in alt_set:
            requires = condition['requires']
            unless = condition['unless']
            if not (requires in alt_set or unless in alt_set):
                paradoxes.append(f"Conditional prerequisite violation for {event}")
    
    print("paradoxes:", paradoxes)
    
    # Final status
    if paradoxes:
        print("\nSTATUS: unsat")
        print("Paradoxes detected in alternate timeline")
    else:
        print("\nSTATUS: sat")
        print("Analysis complete - no paradoxes detected")
else:
    print("\nSTATUS: unsat")
    print("Cannot complete analysis due to timeline inconsistencies")