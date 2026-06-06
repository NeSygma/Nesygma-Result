fof(plungers_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_appliance, axiom, household_appliance(duster)).
fof(duster_does_not_suck, axiom, ~sucks(duster)).
fof(distinct_entities, axiom, (duster != space)).
fof(goal, conjecture, ? [X] : (household_appliance(X) & ~sucks(X))).