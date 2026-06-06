fof(ets_aid_rule, axiom, ! [X] : ((applicant_for(X, gre_test) & can_prove_hardship(X)) => provides_financial_aid(ets, X))).
fof(hardship_rule1, axiom, ! [X] : (single_parent_family(X) => can_prove_hardship(X))).
fof(hardship_rule2, axiom, ! [X] : (few_resources(X) => can_prove_hardship(X))).
fof(tom_single_parent, axiom, single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(tom_applying, axiom, applicant_for(tom, gre_test)).
fof(distinct_entities, axiom, (tom != ets & tom != gre_test & ets != gre_test)).
fof(goal, conjecture, ? [X, Y] : (applicant_for(X, gre_test) & provides_financial_aid(Y, X))).