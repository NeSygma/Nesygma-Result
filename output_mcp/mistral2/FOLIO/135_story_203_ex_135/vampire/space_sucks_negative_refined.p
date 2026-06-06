fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_sucks, axiom, sucks(vacuum)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, space = vacuum).
fof(duster_def, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~sucks(X)))).
fof(duster_is_duster, axiom, duster(duster)).

fof(goal_negation, conjecture, ~sucks(space)).