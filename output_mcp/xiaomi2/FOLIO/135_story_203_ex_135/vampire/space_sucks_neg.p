fof(plungers_suck, axiom, ! [X] : (plunger(X) => suck(X))).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_properties, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~suck(X)))).
fof(goal, conjecture, ~suck(space)).