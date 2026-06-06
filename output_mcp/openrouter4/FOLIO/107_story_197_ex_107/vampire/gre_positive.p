fof(premise2, axiom, ! [X] : ((gre_applicant(X) & proves_hardship(X)) => has_financial_aid(X))).
fof(premise3, axiom, ! [X] : ((lives_single_parent(X) | has_few_resources(X)) => proves_hardship(X))).
fof(premise4, axiom, lives_single_parent(tom)).
fof(premise5, axiom, has_few_resources(tom)).
fof(premise6, axiom, gre_applicant(tom)).
fof(goal, conjecture, ! [X] : (gre_applicant(X) => ~has_financial_aid(X))).