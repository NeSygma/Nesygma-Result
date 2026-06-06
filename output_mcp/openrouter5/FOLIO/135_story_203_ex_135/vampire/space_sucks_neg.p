% Negative version: negated claim "Space does NOT suck" as conjecture
fof(plungers_suck, axiom, plunger_sucks).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_doesnt_suck, axiom, ! [X] : (duster(X) => ~sucks(X))).
fof(goal, conjecture, ~sucks(space)).