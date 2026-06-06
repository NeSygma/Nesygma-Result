fof(plunger_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_vacuum, axiom, vacuum(space)).
fof(duster_appliance, axiom, household_appliance(duster)).
fof(duster_not_suck, axiom, ~sucks(duster)).
fof(goal, conjecture, ~(! [X] : (household_appliance(X) => sucks(X)))).