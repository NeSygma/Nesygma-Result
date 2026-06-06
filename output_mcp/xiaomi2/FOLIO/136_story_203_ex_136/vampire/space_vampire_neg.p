fof(plunger_sucks, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_sucks, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_sucks, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_appliance, axiom, household_appliance(the_duster)).
fof(duster_is_duster, axiom, duster(the_duster)).
fof(duster_not_suck, axiom, ~sucks(the_duster)).
fof(distinct_names, axiom, (space != the_duster)).
fof(goal, conjecture, ~vampire(space)).