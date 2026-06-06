% Premises about sucking things
fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_sucks, axiom, sucks(vacuum)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, is_vacuum(space)).
fof(duster_doesnt_suck, axiom, ~sucks(duster)).

% Logical rules
fof(vacuums_suck, axiom, ! [X] : (is_vacuum(X) => sucks(X))).
fof(vampires_suck, axiom, ! [X] : (is_vampire(X) => sucks(X))).

% Distinct entities
fof(distinct_entities, axiom, (plunger != vacuum & plunger != vampire & plunger != space & plunger != duster & vacuum != vampire & vacuum != space & vacuum != duster & vampire != space & vampire != duster & space != duster)).

% Negated conclusion
fof(goal_negated, conjecture, ~is_vampire(space)).