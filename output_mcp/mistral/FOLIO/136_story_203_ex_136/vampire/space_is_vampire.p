fof(all_plungers_suck, axiom, ! [X] : (plunger(X) => suck(X))).
fof(all_vacuums_suck, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(all_vampires_suck, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(all_dusters_are_household_appliances_that_dont_suck, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~suck(X)))).

fof(space_is_vampire_conjecture, conjecture, vampire(space)).