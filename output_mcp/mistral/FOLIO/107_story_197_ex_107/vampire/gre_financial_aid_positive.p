fof(premise1, axiom, ! [X] : ((gre_applicant(X) & can_prove_hardship(X)) => receives_financial_aid(X))).
fof(premise2, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => can_prove_hardship(X))).
fof(premise3, axiom, single_parent_family(tom)).
fof(premise4, axiom, few_resources(tom)).
fof(premise5, axiom, gre_applicant(tom)).
fof(premise6, axiom, taking_gre(tom)).
fof(conclusion, conjecture, ! [X] : (taking_gre(X) => ~receives_financial_aid(X))).