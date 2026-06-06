fof(axiom_plunger, axiom, ! [X] : (plunger(X) => suck(X))).
fof(axiom_vacuum, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(axiom_vampire, axiom, ! [X] : (vampire(X) => suck(X))).
fof(axiom_space_vacuum, axiom, vacuum(space)).
fof(axiom_duster_not_suck, axiom, ~suck(duster)).
fof(distinct_space_duster, axiom, space != duster).
fof(goal, conjecture, suck(space)).