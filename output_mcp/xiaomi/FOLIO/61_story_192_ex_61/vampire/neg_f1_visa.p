fof(international_student_def, axiom, ! [X] : (international_student(X) => (f1_visa(X) | j1_visa(X)))).
fof(f1_work_rule, axiom, ! [X] : ((international_student(X) & f1_visa(X) & wants_to_work(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(mike_international, axiom, international_student(mike)).
fof(mike_cpt_rule, axiom, (wants_to_work(mike) => needs_cpt(mike))).
fof(goal, conjecture, ~f1_visa(mike)).