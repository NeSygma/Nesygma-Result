fof(premise1, axiom, ! [X] : ((international_student(X) & in_us(X)) => (visa_f1(X) | visa_j1(X)))).
fof(premise2, axiom, ! [X] : ((international_student(X) & in_us(X) & visa_f1(X) & wants_to_work(X)) => (apply_cpt(X) | apply_opt(X)))).
fof(fact_mike_international, axiom, international_student(mike)).
fof(premise4_cpt, axiom, apply_cpt(mike) | ~wants_to_work(mike)).
fof(conclusion, conjecture, visa_j1(mike)).