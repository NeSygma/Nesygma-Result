fof(premise1, axiom, ![X] : (international_student(X) => (f1_visa(X) | j1_visa(X)))).
fof(premise2, axiom, ![X] : ((international_student(X) & f1_visa(X) & wants_to_work_in_us(X)) => (cpt(X) | opt(X)))).
fof(premise3, axiom, international_student(mike)).
fof(premise4, axiom, (wants_to_work_in_us(mike) => cpt(mike))).
fof(conjecture, conjecture, ~f1_visa(mike)).