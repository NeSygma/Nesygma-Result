fof(plunger_sucks, axiom, sucks(plunger)).
fof(vacuum_sucks, axiom, sucks(vacuum)).
fof(vampire_sucks, axiom, sucks(vampire)).
fof(space_is_vacuum, axiom, space = vacuum).
fof(duster_def, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~sucks(X)))).
fof(duster_is_duster, axiom, duster(duster)).

fof(distinct_entities, axiom, (plunger != vacuum & plunger != vampire & plunger != space & plunger != duster &
                              vacuum != vampire & vacuum != space & vacuum != duster &
                              vampire != space & vampire != duster &
                              space != duster)).

fof(goal, conjecture, sucks(space)).