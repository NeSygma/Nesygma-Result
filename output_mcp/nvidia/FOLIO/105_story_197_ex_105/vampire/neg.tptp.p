fof(axiom_hardship_aid, axiom, ! [X] : ((gre_applicant(X) & proves_hardship(X)) => provides_aid(X))).
fof(axiom_hardship_or, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => proves_hardship(X))).
fof(axiom_tom_single_parent, axiom, single_parent_family(tom)).
fof(axiom_tom_few_resources, axiom, few_resources(tom)).
fof(axiom_tom_gre_applicant, axiom, gre_applicant(tom)).
fof(conjecture, conjecture, ~provides_aid(tom)).