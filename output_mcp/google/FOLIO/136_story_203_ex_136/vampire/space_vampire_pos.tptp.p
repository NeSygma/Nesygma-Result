fof(plunger_sucks, axiom, ! [X] : (is_a(X, plunger_class) => sucks(X))).
fof(vacuum_sucks, axiom, ! [X] : (is_a(X, vacuum_class) => sucks(X))).
fof(vampire_sucks, axiom, ! [X] : (is_a(X, vampire_class) => sucks(X))).
fof(space_is_vacuum, axiom, is_a(space, vacuum_class)).
fof(duster_is_appliance, axiom, is_a(duster, household_appliance_class)).
fof(duster_doesnt_suck, axiom, ~sucks(duster)).
fof(distinct_entities, axiom, (space != duster)).
fof(goal, conjecture, is_a(space, vampire_class)).