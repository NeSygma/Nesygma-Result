fof(premise1, axiom, ! [X] : ((at_marys_school(X) & student_job(X)) => needs_money(X))).
fof(premise2, axiom, ! [X] : (at_marys_school(X) & takeout_frequently(X) => student_job(X))).
fof(premise3, axiom, ! [X] : (at_marys_school(X) => (takeout_frequently(X) | enjoys_dining_hall(X)))).
fof(premise4, axiom, ! [X] : (at_marys_school(X) & enjoys_dining_hall(X) => ~picky_eater(X))).
fof(premise5, axiom, ! [X] : (at_marys_school(X) & enjoys_dining_hall(X) => spends_time_dining(X))).
fof(premise6, axiom, at_marys_school(hannah)).
fof(premise7a, axiom, student_job(hannah)).
fof(premise7b, axiom, needs_money(hannah) => (~picky_eater(hannah) & ~enjoys_dining_hall(hannah))).

fof(conclusion, conjecture, at_marys_school(hannah) & (~picky_eater(hannah) | spends_time_dining(hannah))).