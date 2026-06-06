tff(gre_cost, type, gre_test_cost: $int).
tff(cheaper_than_300, axiom, gre_test_cost = 205).
tff(cheaper_than_300_2, axiom, $lesseq(gre_test_cost, 300)).

tff(ets_financial_aid_def, axiom,
    ! [A] : (economic_hardship(A) => ets_financial_aid(A))).

tff(economic_hardship_def, axiom,
    ! [A] : ((single_parent_family(A) | few_resources(A)) => economic_hardship(A))).

tff(tom_single_parent, axiom, single_parent_family(tom)).
tff(tom_few_resources, axiom, few_resources(tom)).


tff(goal, conjecture, $lesseq(gre_test_cost, 300)).