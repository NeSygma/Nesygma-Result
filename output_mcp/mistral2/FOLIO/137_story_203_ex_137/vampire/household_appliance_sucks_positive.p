fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_sucks, axiom, sucks(vacuum)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_household_appliance, axiom, household_appliance(duster)).
fof(duster_does_not_suck, axiom, ~sucks(duster)).
fof(household_appliance_implies_sucks, conjecture, ! [X] : (household_appliance(X) => sucks(X))).