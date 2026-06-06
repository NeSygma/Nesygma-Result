% Negative version: Negated claim as conjecture
fof(cost_gre, axiom, cost(gre_test, 205)).
fof(cheaper_than_300, axiom, cheaper_than(gre_test, 300)).
fof(financial_aid_rule, axiom, ! [X] : (applying(X) & economic_hardship(X) => financial_aid(X))).
fof(economic_hardship_rule, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => economic_hardship(X))).
fof(tom_single_parent, axiom, single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(tom_applying, axiom, applying(tom)).
fof(distinct_entities, axiom, (tom != gre_test)).
fof(goal, conjecture, ? [X] : (taking(X) & financial_aid(X))). % Someone taking the GRE test has financial aid