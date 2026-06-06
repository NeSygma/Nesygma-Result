% Axioms
fof(axiom_provides_aid, axiom, ! [X] : ((takes_gre(X) & proves_hardship(X)) => provides_aid(X))).
fof(axiom_hardship, axiom, ! [X] : ((lives_in_single_parent_family(X) | has_few_resources(X)) => proves_hardship(X))).
fof(axiom_tom_single_parent, axiom, lives_in_single_parent_family(tom)).
fof(axiom_tom_few_resources, axiom, has_few_resources(tom)).
fof(axiom_tom_takes_gre, axiom, takes_gre(tom)).
% Conjecture
fof(conjecture, conjecture, ! [X] : (takes_gre(X) => ~provides_aid(X))).