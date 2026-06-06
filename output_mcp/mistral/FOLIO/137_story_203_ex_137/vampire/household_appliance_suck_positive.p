fof(plunger_sucks, axiom, ! [X] : (plunger(X) => suck(X))).
fof(vacuum_sucks, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(vampire_sucks, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_household_no_suck, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~suck(X)))).
fof(conclusion, conjecture, ! [X] : (household_appliance(X) => suck(X))).