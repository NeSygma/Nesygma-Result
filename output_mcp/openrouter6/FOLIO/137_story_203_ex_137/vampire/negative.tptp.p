fof(premise_plunger, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(premise_vacuum, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(premise_vampire, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(premise_space, axiom, vacuum(space)).
fof(premise_duster, axiom, household_appliance(duster) & ~sucks(duster)).
fof(distinct, axiom, space != duster).
fof(negated_conclusion, conjecture, ? [X] : (household_appliance(X) & ~sucks(X))).