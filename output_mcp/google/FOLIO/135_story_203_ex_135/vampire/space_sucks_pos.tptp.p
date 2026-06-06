fof(plungers_suck, axiom, sucks(plunger)).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_info, axiom, (household_appliance(duster) & ~sucks(duster))).
fof(goal, conjecture, sucks(space)).