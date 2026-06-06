fof(premise_2, axiom, ! [X] : (gre_applicant(X) & economic_hardship(X) => financial_aid(X))).
fof(premise_3, axiom, ! [X] : (single_parent_family(X) | few_resources(X) => economic_hardship(X))).
fof(premise_4, axiom, single_parent_family(tom)).
fof(premise_5, axiom, few_resources(tom)).
fof(premise_6, axiom, applying_gre(tom)).
fof(bridge, axiom, ! [X] : (applying_gre(X) => gre_applicant(X))).
fof(goal, conjecture, ~financial_aid(tom)).