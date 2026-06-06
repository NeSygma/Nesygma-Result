% Positive version: original conclusion as conjecture
% Premises:
% Plungers suck.
% Vacuums suck.
% Vampires suck.
% Space is a vacuum.
% A duster is a household appliance that doesn't suck.

fof(distinct, axiom, (plunger != vacuum & plunger != vampire & plunger != space & plunger != duster & vacuum != vampire & vacuum != space & vacuum != duster & vampire != space & vampire != duster & space != duster)).

fof(plunger_sucks, axiom, ! [X] : (plunger(X) => sucks(X))).
fof(vacuum_sucks, axiom, ! [X] : (vacuum(X) => sucks(X))).
fof(vampire_sucks, axiom, ! [X] : (vampire(X) => sucks(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_is_appliance_not_suck, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~sucks(X)))).

% Also need to define that there exists a duster
fof(duster_exists, axiom, ? [X] : duster(X)).

% Conclusion: If something is a household appliance, it sucks.
fof(goal, conjecture, ! [X] : (household_appliance(X) => sucks(X))).