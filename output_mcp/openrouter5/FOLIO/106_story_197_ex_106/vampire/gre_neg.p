% Negative version: negated conclusion as conjecture
% Negated conclusion: It does NOT cost below US $300 to take the GRE test.

% Premise 1: It costs $205 to take the GRE test, which is cheaper than $300.
tff(cost_gre_type, type, cost_gre: $int).
tff(cost_gre_val, axiom, cost_gre = 205).
tff(cheaper_than_300, axiom, $less(cost_gre, 300)).

% Premise 2: ETS provides financial aid to those GRE applicants who prove economic hardship.
tff(person_type, type, person: $tType).
tff(gre_applicant_decl, type, gre_applicant: person > $o).
tff(proves_hardship_decl, type, proves_hardship: person > $o).
tff(receives_aid_decl, type, receives_aid: person > $o).
tff(ets_aid_rule, axiom, ! [P: person] : ((gre_applicant(P) & proves_hardship(P)) => receives_aid(P))).

% Premise 3: Those living in single-parent families or having few resources available to them can prove economic hardship.
tff(lives_single_parent_decl, type, lives_single_parent: person > $o).
tff(has_few_resources_decl, type, has_few_resources: person > $o).
tff(hardship_rule, axiom, ! [P: person] : ((lives_single_parent(P) | has_few_resources(P)) => proves_hardship(P))).

% Premise 4: Tom lives in a single-parent family.
tff(tom_decl, type, tom: person).
tff(tom_single_parent, axiom, lives_single_parent(tom)).

% Premise 5: Tom's dad has been out of work, and Tom has few resources available to them.
tff(tom_few_resources, axiom, has_few_resources(tom)).

% Premise 6: Tom is applying to take the GRE test.
tff(tom_applicant, axiom, gre_applicant(tom)).

% Negated conclusion: It does NOT cost below US $300 to take the GRE test.
tff(goal_neg, conjecture, ~$less(cost_gre, 300)).