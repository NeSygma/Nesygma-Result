fof(plungers_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_appliance, axiom, household_appliance(duster_1)).
fof(duster_is_duster, axiom, duster(duster_1)).
fof(duster_doesnt_suck, axiom, ~sucks(duster_1)).

fof(goal, conjecture, ~sucks(space)).