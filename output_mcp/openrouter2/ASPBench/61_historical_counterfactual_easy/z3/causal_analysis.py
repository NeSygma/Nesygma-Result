from z3 import *

# Define events and their prerequisites
events = [
    'discovery_of_america',
    'columbian_exchange',
    'spanish_empire',
    'industrial_revolution',
    'world_wars'
]

prereqs = {
    'discovery_of_america': [],
    'columbian_exchange': ['discovery_of_america'],
    'spanish_empire': ['discovery_of_america'],
    'industrial_revolution': ['spanish_empire'],
    'world_wars': ['industrial_revolution']
}

# Intervention: prevent discovery_of_america
intervention_events = ['discovery_of_america']

# Create solver and variables
solver = Solver()
occurs = {e: Bool(e) for e in events}

# Add constraints
for e in events:
    if e in intervention_events:
        # Prevented by intervention
        solver.add(occurs[e] == False)
    else:
        # Event occurs iff all prerequisites occur
        if prereqs[e]:
            solver.add(occurs[e] == And([occurs[p] for p in prereqs[e]]))
        else:
            # No prerequisites: event occurs
            solver.add(occurs[e] == True)

# Check satisfiability
result = solver.check()
if result == sat:
    model = solver.model()
    # Build lists
    original_timeline = events
    alternate_timeline = [e for e in events if is_true(model[occurs[e]])]
    prevented_events = [e for e in events if not is_true(model[occurs[e]])]
    # Direct effects: events that have the intervention event as a prerequisite
    direct_effects = [e for e in events if 'discovery_of_america' in prereqs[e]]
    # Cascade effects: prevented events that are not direct effects
    cascade_effects = [e for e in prevented_events if e not in direct_effects]
    preserved_events = alternate_timeline
    # Print results
    print("STATUS: sat")
    print("original_timeline =", original_timeline)
    print("alternate_timeline =", alternate_timeline)
    print("prevented_events =", prevented_events)
    print("causal_analysis.direct_effects =", direct_effects)
    print("causal_analysis.cascade_effects =", cascade_effects)
    print("causal_analysis.preserved_events =", preserved_events)
    print("causal_analysis.intervention_events =", intervention_events)
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")