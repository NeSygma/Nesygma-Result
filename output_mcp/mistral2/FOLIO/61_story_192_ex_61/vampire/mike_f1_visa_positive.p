fof(premise1, axiom, ! [X] : (international_student(X) => (has_f1_visa(X) | has_j1_visa(X)))).
fof(premise2, axiom, ! [X] : ((international_student(X) & has_f1_visa(X) & wants_to_work(X)) => needs_cpt_or_opt(X))).
fof(premise3, axiom, international_student(mike)).
fof(premise4, axiom, (wants_to_work(mike) => needs_cpt(mike))).

fof(goal, conjecture, has_f1_visa(mike)).