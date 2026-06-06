fof(p1, axiom, ! [X] : ((at_marys_school(X) & student_job(X)) => needs_money(X))).
fof(p2, axiom, ! [X] : ((at_marys_school(X) & orders_takeout(X)) => student_job(X))).
fof(p3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining(X)))).
fof(p4, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining(X)) => ~picky_eater(X))).
fof(p5, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining(X)) => eats_with_friends(X))).
fof(p6, axiom, at_marys_school(hannah)).
fof(p7, axiom, (student_job(hannah) & (needs_money(hannah) => (~picky_eater(hannah) & ~needs_money(hannah))))).
fof(goal, conjecture, needs_money(hannah)).