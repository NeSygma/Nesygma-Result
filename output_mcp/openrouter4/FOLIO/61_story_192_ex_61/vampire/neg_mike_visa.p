% Negative run: try to prove Mike does NOT have an F1 visa
fof(premise_1, axiom, ! [X] : (international_student(X) => (f1_visa(X) | j1_visa(X)))).
fof(premise_2, axiom, ! [X] : ((international_student(X) & f1_visa(X) & wants_to_work(X)) => (apply_cpt(X) | apply_opt(X)))).
fof(premise_3, axiom, international_student(mike)).
fof(premise_4, axiom, (wants_to_work(mike) => apply_cpt(mike))).
fof(conclusion_neg, conjecture, ~f1_visa(mike)).