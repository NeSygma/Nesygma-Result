fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_sucks, axiom, sucks(vacuum)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, is_a(space, vacuum)).
fof(duster_is_appliance, axiom, is_a(duster, household_appliance)).
fof(duster_not_suck, axiom, ~sucks(duster)).

% The conclusion: Space is a vampire.
fof(goal, conjecture, is_a(space, vampire)).