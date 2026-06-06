fof(plunger_suck, axiom, ! [X] : (plunger(X) => suck(X))).
fof(vacuum_suck, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(vampire_suck, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_household, axiom, household_appliance(duster)).
fof(duster_not_suck, axiom, ~suck(duster)).
fof(distinct_consts, axiom, (plunger != vacuum & plunger != vampire & plunger != space & plunger != duster & vacuum != vampire & vacuum != space & vacuum != duster & vampire != space & vampire != duster & space != duster)).
fof(goal_neg, conjecture, ? [X] : (household_appliance(X) & ~suck(X))).