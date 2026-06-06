fof(p1, axiom, ! [X] : (intl_student(X) => (f1_visa(X) | j1_visa(X)))).
fof(p2, axiom, ! [X] : ((intl_student(X) & f1_visa(X) & wants_to_work(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(p3, axiom, intl_student(mike)).
fof(p4, axiom, wants_to_work(mike) => needs_cpt(mike)).
fof(goal, conjecture, ~f1_visa(mike)).