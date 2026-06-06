fof(plunger_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_property, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~sucks(X)))).
fof(conjecture, conjecture, ? [X] : (household_appliance(X) & ~sucks(X))).