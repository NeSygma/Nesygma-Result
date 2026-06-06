% Positive version: original claim as conjecture
% Premises:
% Plungers suck.
% Vacuums suck.
% Vampires suck.
% Space is a vacuum.
% A duster is a household appliance that doesn't suck.

% Conclusion to evaluate: Space is a vampire.

% Predicates:
% sucks(X) - X sucks
% vacuum(X) - X is a vacuum
% vampire(X) - X is a vampire
% plunger(X) - X is a plunger
% duster(X) - X is a duster
% household_appliance(X) - X is a household appliance

fof(plungers_suck, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuums_suck, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_property, axiom, ! [X] : ((duster(X) & household_appliance(X)) => ~sucks(X))).

fof(conclusion, conjecture, vampire(space)).