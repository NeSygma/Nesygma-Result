% Axioms
fof(axiom_vacuum_suck, axiom, ! [X] : (vacuum(X) => suck(X))).
fof(fact_plunger_suck, axiom, suck(plunger)).
fof(fact_space_vacuum, axiom, vacuum(space)).
fof(fact_vampire_suck, axiom, suck(vampire)).
fof(fact_duster_not_suck, axiom, ~suck(duster)).
fof(conjecture, conjecture, ~vampire(space)).