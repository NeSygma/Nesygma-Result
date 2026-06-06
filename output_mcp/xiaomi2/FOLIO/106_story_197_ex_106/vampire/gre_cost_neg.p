tff(gre_cost_type, type, gre_cost: $int).

% Premise 1: It costs $205 to take the GRE test, which is cheaper than $300.
tff(gre_cost_val, axiom, gre_cost = 205).
tff(gre_cheaper_than_300, axiom, $less(gre_cost, 300)).

% Premise 2: ETS provides financial aid to GRE applicants who prove economic hardship.
tff(person_type, type, person: $tType).
tff(tom_decl, type, tom: person).
tff(gre_applicant_type, type, gre_applicant: person > $o).
tff(proves_hardship_type, type, proves_hardship: person > $o).
tff(gets_aid_type, type, gets_aid: person > $o).

tff(financial_aid_rule, axiom, ! [P: person] :
    ((gre_applicant(P) & proves_hardship(P)) => gets_aid(P))).

% Premise 3: Those in single-parent families or with few resources can prove hardship.
tff(single_parent_type, type, single_parent: person > $o).
tff(few_resources_type, type, few_resources: person > $o).

tff(hardship_rule, axiom, ! [P: person] :
    ((single_parent(P) | few_resources(P)) => proves_hardship(P))).

% Premise 4: Tom lives in a single-parent family.
tff(tom_single_parent, axiom, single_parent(tom)).

% Premise 5: Tom's dad has been out of work, and Tom has few resources.
tff(tom_few_resources, axiom, few_resources(tom)).

% Premise 6: Tom is applying to take the GRE test.
tff(tom_applicant, axiom, gre_applicant(tom)).

% Negated conclusion: It is NOT the case that GRE costs below $300.
tff(goal, conjecture, ~$less(gre_cost, 300)).