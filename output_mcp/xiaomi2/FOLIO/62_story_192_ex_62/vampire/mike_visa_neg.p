fof(international_student_mike, axiom, international_student(mike)).

fof(visa_type, axiom, ! [X] : (international_student(X) => (f1_visa(X) | j1_visa(X)))).

fof(f1_j1_exclusive, axiom, ! [X] : (f1_visa(X) => ~j1_visa(X))).

fof(f1_work_cpt_opt, axiom, ! [X] : ((international_student(X) & f1_visa(X) & wants_to_work(X)) => (needs_cpt(X) | needs_opt(X)))).

fof(mike_cpt_if_work, axiom, (wants_to_work(mike) => needs_cpt(mike))).

fof(goal, conjecture, ~j1_visa(mike)).