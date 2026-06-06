% Visa problem - positive version (conclusion: Mike has J1 visa)
fof(distinct_visa_types, axiom, (f1 != j1)).
fof(international_student_def, axiom, ! [X] : (international_student(X) => (has_visa(X, f1) | has_visa(X, j1)))).
fof(visa_exclusive, axiom, ! [X] : ~(has_visa(X, f1) & has_visa(X, j1))).
fof(f1_work_rule, axiom, ! [X] : ((international_student(X) & has_visa(X, f1) & wants_to_work(X)) => (needs_work_auth(X, cpt) | needs_work_auth(X, opt)))).
fof(mike_international, axiom, international_student(mike)).
fof(mike_needs_cpt, axiom, ! [X] : (wants_to_work(X) => needs_work_auth(X, cpt))).
fof(goal, conjecture, has_visa(mike, j1)).