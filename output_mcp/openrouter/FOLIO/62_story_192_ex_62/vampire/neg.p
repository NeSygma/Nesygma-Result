% Negative test: does Mike NOT have a J1 visa?
fof(premise1, axiom, ! [X] : (international_student_us(X) => (f1_visa(X) | j1_visa(X)))).
fof(premise2, axiom, ! [X] : ((international_student_us(X) & f1_visa(X) & wants_work_us(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(premise3, axiom, international_student_us(mike)).
fof(premise4, axiom, (wants_work_us(mike) => needs_cpt(mike))).
fof(goal, conjecture, ~j1_visa(mike)).