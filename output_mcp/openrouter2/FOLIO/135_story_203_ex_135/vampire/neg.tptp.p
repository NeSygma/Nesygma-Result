fof(rule_plunger, axiom, ! [X] : (plunger(X) => suck(X))).
fof(rule_vacuum, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(rule_vampire, axiom, ! [X] : (vampire(X) => suck(X))).
fof(space_is_vacuum, axiom, vacuum(space)).
fof(duster_rule, axiom, ! [X] : (duster(X) => ~suck(X))).
fof(conj, conjecture, ~suck(space)).