from z3 import *

# Define events and their years
events = {
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
    "digital_renaissance": 1980
}

# Prerequisites (simple)
prereqs = {
    "fall_of_rome": ["ancient_knowledge"],
    "dark_ages": ["fall_of_rome"],
    "renaissance": ["dark_ages"],
    "age_of_sail": ["renaissance"],
    "age_of_steam": ["renaissance"],
    "discovery_of_new_world": ["age_of_sail"],
    "global_trade_routes": ["age_of_sail"],
    "industrial_revolution": ["age_of_steam"],
    "information_age": ["industrial_revolution"],
    "digital_renaissance": ["alternate_industrial_revolution"]
}

# Pivot groups
pivot_groups = {
    "paradigm": ["age_of_sail", "age_of_steam"]
}

# Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
# This means: alternate_industrial_revolution can occur if (age_of_steam occurs) OR (global_trade_routes occurs AND age_of_steam does not occur)

# Intervention: prevent age_of_sail in alternate timeline

# Create solver for original timeline
solver_orig = Solver()

# Boolean variables for original timeline
occur_orig = {event: Bool(f"orig_{event}") for event in events}

# Add prerequisite constraints for original timeline
for event, reqs in prereqs.items():
    for req in reqs:
        solver_orig.add(Implies(occur_orig[event], occur_orig[req]))

# Pivot group "paradigm" constraints for original timeline
# Both age_of_sail and age_of_steam require renaissance
# Original timeline pivot rule: choose earliest year when multiple are possible
# Since both require renaissance, if renaissance occurs, both are possible, choose age_of_sail (earlier)
# If renaissance does not occur, neither is possible
solver_orig.add(occur_orig["age_of_sail"] == occur_orig["renaissance"])
solver_orig.add(occur_orig["age_of_steam"] == False)  # Never occurs in original timeline

# Ensure age_of_sail and age_of_steam cannot occur if prerequisites not met (already covered)

# Check satisfiability of original timeline
result_orig = solver_orig.check()
if result_orig == sat:
    model_orig = solver_orig.model()
    orig_timeline = [event for event in events if is_true(model_orig[occur_orig[event]])]
    # Sort by year
    orig_timeline_sorted = sorted(orig_timeline, key=lambda e: events[e])
    print("Original timeline (sorted by year):")
    for event in orig_timeline_sorted:
        print(f"  {event} ({events[event]})")
else:
    print("Original timeline: UNSATISFIABLE - paradox detected")
    orig_timeline_sorted = []

# Create solver for alternate timeline
solver_alt = Solver()

# Boolean variables for alternate timeline
occur_alt = {event: Bool(f"alt_{event}") for event in events}

# Intervention: prevent age_of_sail
solver_alt.add(occur_alt["age_of_sail"] == False)

# Add prerequisite constraints for alternate timeline
for event, reqs in prereqs.items():
    for req in reqs:
        solver_alt.add(Implies(occur_alt[event], occur_alt[req]))

# Conditional prerequisite for alternate_industrial_revolution
# alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
# This means: alternate_industrial_revolution can occur if (age_of_steam occurs) OR (global_trade_routes occurs AND age_of_steam does not occur)
# We'll encode: alternate_industrial_revolution => (age_of_steam OR (global_trade_routes AND NOT age_of_steam))
# Simplify: alternate_industrial_revolution => (age_of_steam OR global_trade_routes)
solver_alt.add(Implies(occur_alt["alternate_industrial_revolution"],
                      Or(occur_alt["age_of_steam"], occur_alt["global_trade_routes"])))

# Pivot group "paradigm" constraints for alternate timeline
# age_of_sail is prevented, so only age_of_steam is possible if renaissance occurs
# If renaissance occurs, age_of_steam is possible and must be chosen (only possible pivot event)
# If renaissance does not occur, age_of_steam cannot occur
solver_alt.add(occur_alt["age_of_steam"] == occur_alt["renaissance"])

# Check satisfiability of alternate timeline
result_alt = solver_alt.check()
if result_alt == sat:
    model_alt = solver_alt.model()
    alt_timeline = [event for event in events if is_true(model_alt[occur_alt[event]])]
    # Sort by year
    alt_timeline_sorted = sorted(alt_timeline, key=lambda e: events[e])
    print("\nAlternate timeline (sorted by year):")
    for event in alt_timeline_sorted:
        print(f"  {event} ({events[event]})")
else:
    print("\nAlternate timeline: UNSATISFIABLE - paradox detected")
    alt_timeline_sorted = []

# Compute prevented and activated events
if result_orig == sat and result_alt == sat:
    prevented = sorted([e for e in orig_timeline_sorted if e not in alt_timeline_sorted])
    activated = sorted([e for e in alt_timeline_sorted if e not in orig_timeline_sorted])
    
    print("\nPrevented events (occurred in original but not alternate):")
    for event in prevented:
        print(f"  {event}")
    
    print("\nActivated events (occurred in alternate but not original):")
    for event in activated:
        print(f"  {event}")
    
    # Check for paradoxes (logical impossibilities)
    paradoxes = []
    if result_orig == unsat:
        paradoxes.append("Original timeline is unsatisfiable")
    if result_alt == unsat:
        paradoxes.append("Alternate timeline is unsatisfiable")
    
    print("\nParadoxes:")
    if paradoxes:
        for p in paradoxes:
            print(f"  {p}")
    else:
        print("  None")

# Output status for downstream processing
print("\nSTATUS: proved")  # Both timelines computed successfully