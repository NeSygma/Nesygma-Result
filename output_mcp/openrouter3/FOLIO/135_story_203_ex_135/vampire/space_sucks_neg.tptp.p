% Premises about sucking
fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_cleaner_sucks, axiom, sucks(vacuum_cleaner)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, is_vacuum(space)).
fof(duster_doesnt_suck, axiom, ~sucks(duster)).

% General rule: If something is a vacuum, it sucks
fof(vacuum_sucks_rule, axiom, ! [X] : (is_vacuum(X) => sucks(X))).

% Negated conclusion
fof(goal_neg, conjecture, ~sucks(space)).