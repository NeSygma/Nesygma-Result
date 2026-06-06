fof(premise1, axiom, ! [X] : (international_student(X) => (has_visa(X, f1) | has_visa(X, j1)))).
fof(premise2, axiom, ! [X] : ((international_student(X) & has_visa(X, f1) & wants_to_work(X)) => (needs_to_apply(X, cpt) | needs_to_apply(X, opt)))).
fof(premise3, axiom, international_student(mike)).
fof(premise4, axiom, (wants_to_work(mike) => needs_to_apply(mike, cpt))).
fof(conclusion, conjecture, ~has_visa(mike, j1)).