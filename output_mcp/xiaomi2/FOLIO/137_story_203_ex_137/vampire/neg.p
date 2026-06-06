% Premises
fof(plunger_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_appliance, axiom, household_appliance(duster_1)).
fof(duster_is_duster, axiom, duster(duster_1)).
fof(duster_not_suck, axiom, ~sucks(duster_1)).

% Distinctness
fof(distinct, axiom, (space != duster_1)).

% Negated conclusion: It is NOT the case that all household appliances suck.
fof(goal, conjecture, ~(! [X] : (household_appliance(X) => sucks(X)))).