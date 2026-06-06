fof(premise_plungers, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(premise_vacuums, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(premise_vampires, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(premise_space_is_vacuum, axiom, vacuum(space)).
fof(premise_duster, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~sucks(X)))).
fof(conclusion, conjecture, sucks(space)).