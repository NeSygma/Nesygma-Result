fof(premise1, axiom, ! [X] : (works_student_job(X) => needs_money(X))).
fof(premise2, axiom, ! [X] : (orders_takeout_frequently(X) => works_student_job(X))).
fof(premise3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout_frequently(X) | enjoys_dining_hall(X)))).
fof(premise4, axiom, ! [X] : (enjoys_dining_hall(X) => ~picky_eater(X))).
fof(premise5, axiom, ! [X] : (enjoys_dining_hall(X) => spends_time_eating(X))).
fof(premise6, axiom, at_marys_school(hannah)).
fof(premise7, axiom, works_student_job(hannah)).
fof(premise8, axiom, ~picky_eater(hannah)).
fof(conclusion_negation, conjecture, ~needs_money(hannah)).