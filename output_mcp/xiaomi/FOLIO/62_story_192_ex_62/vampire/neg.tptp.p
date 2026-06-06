fof(international_has_visa, axiom, ! [X] : (international_student(X) => (has_f1_visa(X) | has_j1_visa(X)))).
fof(f1_work_needs_cpt_or_opt, axiom, ! [X] : ((international_student(X) & has_f1_visa(X) & wants_to_work(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(mike_international, axiom, international_student(mike)).
fof(mike_needs_cpt_if_work, axiom, wants_to_work(mike) => needs_cpt(mike)).
fof(goal, conjecture, ~has_j1_visa(mike)).