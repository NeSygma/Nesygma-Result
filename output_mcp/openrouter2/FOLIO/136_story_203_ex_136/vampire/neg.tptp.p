fof(plunger_suck, axiom, ! [X] : (plunger(X) => suck(X))).
fof(vacuum_suck, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(vampire_suck, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_not_suck, axiom, ! [X] : (duster(X) => ~suck(X))).
fof(conjecture, conjecture, ~vampire(space)).