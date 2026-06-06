tff(cost_205, type, cost_205: $int).
tff(cost_300, type, cost_300: $int).
tff(person_type, type, person: $tType).
tff(tom, type, tom: person).

tff(gre_cost_type, type, gre_cost: ($int) > $o ).
tff(cheaper_than_type, type, cheaper_than: ($int * $int) > $o ).
tff(financial_aid_available_type, type, financial_aid_available: $o ).
tff(eligible_for_aid_type, type, eligible_for_aid: (person) > $o ).
tff(proves_hardship_type, type, proves_hardship: (person) > $o ).
tff(single_parent_family_type, type, single_parent_family: (person) > $o ).
tff(few_resources_type, type, few_resources: (person) > $o ).
tff(applying_for_gre_type, type, applying_for_gre: (person) > $o ).

tff(gre_cost_205, axiom, gre_cost(cost_205)).
tff(cheaper_than_205_300, axiom, cheaper_than(cost_205, cost_300)).
tff(financial_aid_available, axiom, financial_aid_available).
tff(proves_hardship_implies_eligible, axiom, ! [P: person] : (proves_hardship(P) => eligible_for_aid(P))).
tff(hardship_conditions, axiom, ! [P: person] : ((single_parent_family(P) | few_resources(P)) => proves_hardship(P))).
tff(tom_single_parent, axiom, single_parent_family(tom)).
tff(tom_few_resources, axiom, few_resources(tom)).
tff(tom_applying, axiom, applying_for_gre(tom)).

tff(conclusion_negation, conjecture, ~cheaper_than(cost_205, cost_300)).