% Positive test: Is "Mike has J1 visa" entailed?
fof(premise1, axiom, ! [X] : (intl_student_in_us(X) => (has_f1(X) | has_j1(X)))).
fof(premise2, axiom, ! [X] : ((intl_student_in_us(X) & has_f1(X) & wants_work(X)) => (needs_cpt(X) | needs_opt(X)))).
fof(premise3, axiom, intl_student_in_us(mike)).
fof(premise4, axiom, (wants_work(mike) => needs_cpt(mike))).
fof(goal, conjecture, has_j1(mike)).