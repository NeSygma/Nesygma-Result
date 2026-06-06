fof(plunger_sucks, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_sucks, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_sucks, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_appliance, axiom, household_appliance(duster)).
fof(duster_not_sucks, axiom, ~sucks(duster)).
fof(distinct_entities, axiom, (space != duster)).
fof(goal_negation, conjecture, ~(! [X] : (household_appliance(X) => sucks(X)))).