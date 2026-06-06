fof(premise1, axiom, ! [X] : (international_student(X) => (f1_visa(X) | j1_visa(X)))).
fof(premise2, axiom, ! [X] : ((international_student(X) & f1_visa(X) & wants_work_us(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(premise3, axiom, international_student(mike)).
fof(premise4, axiom, (wants_work_us(mike) => needs_cpt(mike))).
fof(goal, conjecture, f1_visa(mike)).