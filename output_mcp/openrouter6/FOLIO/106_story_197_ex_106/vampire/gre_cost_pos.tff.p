tff(cost_type, type, gre_cost: $int).
tff(gre_cost_axiom, axiom, gre_cost = 205).
tff(cheaper_axiom, axiom, $less(205, 300)).

% Person type and predicates
tff(person_type, type, person: $tType).
tff(tom_decl, type, tom: person).
tff(single_parent_family_type, type, single_parent_family: person > $o).
tff(few_resources_type, type, few_resources: person > $o).
tff(applicant_type, type, applicant: person > $o).
tff(proves_hardship_type, type, proves_hardship: person > $o).
tff(financial_aid_type, type, financial_aid: person > $o).

% Premise 2: ETS provides financial aid to those GRE applicants who prove economic hardship.
tff(premise_2, axiom, ! [P: person] : (applicant(P) & proves_hardship(P) => financial_aid(P))).

% Premise 3: Those living in single-parent families or having few resources can prove economic hardship.
tff(premise_3, axiom, ! [P: person] : (single_parent_family(P) | few_resources(P) => proves_hardship(P))).

% Premise 4: Tom lives in a single-parent family.
tff(premise_4, axiom, single_parent_family(tom)).

% Premise 5: Tom's dad has been out of work, and Tom has few resources available to them.
tff(premise_5, axiom, few_resources(tom)).

% Premise 6: Tom is applying to take the GRE test.
tff(premise_6, axiom, applicant(tom)).

% Conclusion: It costs below US $300 to take the GRE test.
tff(goal, conjecture, $less(gre_cost, 300)).