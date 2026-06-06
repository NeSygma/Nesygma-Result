% Negative version: negated claim as conjecture
% Premises:
% Plungers suck.
% Vacuums suck.
% Vampires suck.
% Space is a vacuum.
% A duster is a household appliance that doesn't suck.

% Conclusion to evaluate: Space is a vampire.
% Negated: Space is NOT a vampire.

fof(plungers_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_property, axiom, ! [X] : ((duster(X) & household_appliance(X)) => ~sucks(X))).

fof(conclusion_negated, conjecture, ~vampire(space)).