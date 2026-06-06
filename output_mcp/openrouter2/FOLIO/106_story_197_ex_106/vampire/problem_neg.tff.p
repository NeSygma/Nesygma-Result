tff(person_sort, type, person: $tType).
tff(tom_decl, type, tom: person).

 tff(gre_cost_decl, type, gre_cost: ($int > $o)).
tff(less_than_decl, type, less_than: ($int * $int > $o)).

 tff(gre_applicant_decl, type, gre_applicant: person > $o).
 tff(single_parent_family_decl, type, single_parent_family: person > $o).
 tff(few_resources_decl, type, few_resources: person > $o).
 tff(proves_economic_hardship_decl, type, proves_economic_hardship: person > $o).
 tff(financial_aid_decl, type, financial_aid: person > $o).

 tff(cost_gre, axiom, gre_cost(205)).
 tff(cost_less, axiom, less_than(205,300)).

 tff(single_parent_rule, axiom, ! [X: person] : (single_parent_family(X) => proves_economic_hardship(X))).
 tff(few_resources_rule, axiom, ! [X: person] : (few_resources(X) => proves_economic_hardship(X))).
 tff(financial_aid_rule, axiom, ! [X: person] : ((gre_applicant(X) & proves_economic_hardship(X)) => financial_aid(X))).

 tff(tom_single_parent, axiom, single_parent_family(tom)).
 tff(tom_few_resources, axiom, few_resources(tom)).
 tff(tom_gre_applicant, axiom, gre_applicant(tom)).

 tff(goal, conjecture, ~less_than(205,300)).