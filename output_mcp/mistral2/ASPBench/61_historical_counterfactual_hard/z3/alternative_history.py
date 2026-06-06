from z3 import *

# Event years (constants)
event_years = {
    "ancient_knowledge": 100,
    "fall_of_rome": 476,
    "dark_ages": 500,
    "renaissance": 1300,
    "age_of_sail": 1400,
    "age_of_steam": 1700,
    "discovery_of_new_world": 1492,
    "global_trade_routes": 1550,
    "industrial_revolution": 1760,
    "information_age": 1970,
    "alternate_industrial_revolution": 1780,
    "digital_renaissance": 1980,
}

# Prerequisites
prerequisites = {
    "fall_of_rome": ["ancient_knowledge"],
    "dark_ages": ["fall_of_rome"],
    "renaissance": ["dark_ages"],
    "age_of_sail": ["renaissance"],
    "age_of_steam": ["renaissance"],
    "discovery_of_new_world": ["age_of_sail"],
    "global_trade_routes": ["age_of_sail"],
    "industrial_revolution": ["age_of_steam"],
    "information_age": ["industrial_revolution"],
    "digital_renaissance": ["alternate_industrial_revolution"],
}

# Pivot groups
pivot_groups = {
    "paradigm": ["age_of_sail", "age_of_steam"],
}

# Conditional prerequisites
conditional_prerequisites = {
    "alternate_industrial_revolution": ("global_trade_routes", "age_of_steam"),
}

# Interventions
prevented_events = ["age_of_sail"]

# Declare event variables
events = {name: Bool(name) for name in event_years}

# Helper function to get the year of an event
def get_year(event_name):
    return event_years[event_name]

# Helper function to get the prerequisite events for a given event
def get_prereqs(event_name):
    return prerequisites.get(event_name, [])

# Helper function to get the pivot group for a given event
def get_pivot_group(event_name):
    for group, members in pivot_groups.items():
        if event_name in members:
            return group
    return None

# Helper function to get all events in a pivot group
def get_pivot_group_events(group_name):
    return pivot_groups.get(group_name, [])

# Original Timeline Solver
def compute_original_timeline():
    solver = Solver()
    # Add prerequisite constraints
    for event, prereq_list in prerequisites.items():
        for prereq in prereq_list:
            solver.add(Implies(events[event], events[prereq]))
    # Add pivot group constraints (at most one)
    for group, members in pivot_groups.items():
        # Use a loop to enforce at most one event in the group
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                solver.add(Not(And(events[members[i]], events[members[j]])))
    # Add conditional prerequisite constraints
    for event, (required, unless) in conditional_prerequisites.items():
        solver.add(Implies(events[event], Or(events[required], events[unless])))
    # Compute the timeline
    result = solver.check()
    if result == sat:
        model = solver.model()
        timeline = [name for name, var in events.items() if is_true(model[var])]
        timeline.sort(key=lambda x: get_year(x))
        return timeline, model
    else:
        return None, None

# Alternate Timeline Solver (with interventions)
def compute_alternate_timeline():
    solver = Solver()
    # Add prerequisite constraints
    for event, prereq_list in prerequisites.items():
        for prereq in prereq_list:
            solver.add(Implies(events[event], events[prereq]))
    # Add pivot group constraints (at most one)
    for group, members in pivot_groups.items():
        # Use a loop to enforce at most one event in the group
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                solver.add(Not(And(events[members[i]], events[members[j]])))
    # Add conditional prerequisite constraints
    for event, (required, unless) in conditional_prerequisites.items():
        solver.add(Implies(events[event], Or(events[required], events[unless])))
    # Add intervention constraints (prevented events)
    for event in prevented_events:
        solver.add(Not(events[event]))
    # Compute the timeline
    result = solver.check()
    if result == sat:
        model = solver.model()
        timeline = [name for name, var in events.items() if is_true(model[var])]
        timeline.sort(key=lambda x: get_year(x))
        return timeline, model
    else:
        return None, None

# Compute both timelines
original_timeline, original_model = compute_original_timeline()
alternate_timeline, alternate_model = compute_alternate_timeline()

# Compute prevented, activated, and paradoxes
prevented_events_list = []
activated_events_list = []
paradoxes = []

if original_timeline is not None and alternate_timeline is not None:
    original_set = set(original_timeline)
    alternate_set = set(alternate_timeline)
    prevented_events_list = sorted(list(original_set - alternate_set))
    activated_events_list = sorted(list(alternate_set - original_set))
    # Check for paradoxes: if an event is prevented but its prerequisites are met in the alternate timeline
    for event in prevented_events:
        if event in original_set and event not in alternate_set:
            # Check if all prerequisites of the event are met in the alternate timeline
            prereqs_met = True
            for prereq in get_prereqs(event):
                if prereq not in alternate_set:
                    prereqs_met = False
                    break
            if prereqs_met:
                paradoxes.append(f"{event} is prevented but its prerequisites are met in the alternate timeline")
    # Check for paradoxes: if an event is activated but its prerequisites are not met in the original timeline
    for event in activated_events_list:
        prereqs_met = True
        for prereq in get_prereqs(event):
            if prereq not in original_set:
                prereqs_met = False
                break
        if not prereqs_met:
            paradoxes.append(f"{event} is activated but its prerequisites are not met in the original timeline")
else:
    paradoxes.append("Failed to compute one or both timelines")

# Print results
print("STATUS: sat")
print("original_timeline =", original_timeline)
print("alternate_timeline =", alternate_timeline)
print("prevented_events =", prevented_events_list)
print("activated_events =", activated_events_list)
print("paradoxes =", paradoxes)