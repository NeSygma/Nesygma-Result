fof(visa_type, axiom, ! [P] : (international_student(P) => (has_visa(P, f1_visa) | has_visa(P, j1_visa)))).
fof(f1_work_rule, axiom, ! [P] : ((has_visa(P, f1_visa) & wants_to_work(P)) => (needs_cpt(P) | needs_opt(P)))).
fof(mike_is_student, axiom, international_student(mike)).
fof(mike_work_cpt, axiom, (wants_to_work(mike) => needs_cpt(mike))).
fof(distinct_visas, axiom, f1_visa != j1_visa).
fof(goal_negation, conjecture, ~has_visa(mike, j1_visa)).