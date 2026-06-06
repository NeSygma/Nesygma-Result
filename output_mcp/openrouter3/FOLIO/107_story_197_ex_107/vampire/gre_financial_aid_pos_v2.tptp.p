% Positive version: Original claim as conjecture
% Using relational predicates to avoid numeric literals in fof
fof(gre_test_exists, axiom, gre_test(gre_test)).
fof(cheaper_than_300, axiom, cheaper_than(gre_test, three_hundred_dollars)).
fof(financial_aid_rule, axiom, ! [X] : (applying(X) & economic_hardship(X) => financial_aid(X))).
fof(economic_hardship_rule, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => economic_hardship(X))).
fof(tom_single_parent, axiom, single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(tom_applying, axiom, applying(tom)).
fof(distinct_entities, axiom, (tom != gre_test & tom != three_hundred_dollars)).
fof(goal, conjecture, ~? [X] : (taking(X) & financial_aid(X))). % No one taking the GRE test has financial aid