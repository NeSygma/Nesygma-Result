% Positive version
fof(distinct_entities, axiom, (plunger != vacuum & plunger != vampire & plunger != space & plunger != duster & vacuum != vampire & vacuum != space & vacuum != duster & vampire != space & vampire != duster & space != duster)).
fof(plunger_sucks, axiom, suck(plunger)).
fof(vacuum_sucks, axiom, suck(vacuum)).
fof(vampire_sucks, axiom, suck(vampire)).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_not_suck, axiom, ~suck(duster)).
fof(goal, conjecture, vampire(space)).