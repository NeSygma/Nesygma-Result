fof(premise1, axiom, ! [X] : (is_plunger(X) => suck(X))).
fof(premise2, axiom, ! [X] : (is_vacuum(X) => suck(X))).
fof(premise3, axiom, ! [X] : (is_vampire(X) => suck(X))).
fof(premise4, axiom, is_vacuum(space)).
fof(premise5, axiom, is_duster(duster) & is_household_appliance(duster) & ~suck(duster)).
fof(distinct, axiom, space != duster).
fof(goal, conjecture, is_vampire(space)).