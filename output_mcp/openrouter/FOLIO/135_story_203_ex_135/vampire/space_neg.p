% Negative version (negated conclusion)
fof(plunger_rule, axiom, ! [X] : (plunger(X) => suck(X))).
fof(vacuum_rule, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(vampire_rule, axiom, ! [X] : (vampire(X) => suck(X))).
fof(duster_rule, axiom, ! [X] : (duster(X) => (household_appliance(X) & ~suck(X)))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(goal, conjecture, ~suck(space)).