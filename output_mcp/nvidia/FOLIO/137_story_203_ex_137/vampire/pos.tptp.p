% Axioms
fof(axiom_plunger_sucks, axiom, sucks(plunger)).
fof(axiom_vacuum_sucks, axiom, sucks(vacuum)).
fof(axiom_vampire_sucks, axiom, sucks(vampire)).
fof(axiom_space_is_vacuum, axiom, vacuum(space)).
fof(axiom_duster_is_household, axiom, household_appliance(duster)).
fof(axiom_duster_not_suck, axiom, ~sucks(duster)).
% Conjecture
fof(conclusion, conjecture, ! [X] : (household_appliance(X) => sucks(X))).