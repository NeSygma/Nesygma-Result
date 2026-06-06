fof(international_student_in_us, axiom, international_student_in_us(mike)).
fof(visa_rule, axiom, ! [X] : (international_student_in_us(X) => (f1_visa(X) | j1_visa(X)))).
fof(f1_rule, axiom, ! [X] : (international_student_in_us(X) & f1_visa(X) & wants_to_work_in_us(X) => (apply_cpt(X) | apply_opt(X)))).
fof(mike_rule, axiom, wants_to_work_in_us(mike) => apply_cpt(mike)).
fof(goal, conjecture, j1_visa(mike)).