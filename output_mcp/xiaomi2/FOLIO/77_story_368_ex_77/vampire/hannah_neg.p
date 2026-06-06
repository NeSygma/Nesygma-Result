fof(p1, axiom, ! [X] : ((at_marys_school(X) & works_student_jobs(X)) => needs_money(X))).
fof(p2, axiom, ! [X] : ((at_marys_school(X) & orders_takeout(X)) => works_student_jobs(X))).
fof(p3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining(X)))).
fof(p4, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining(X)) => ~picky_eater(X))).
fof(p5, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining(X)) => spends_time_dining(X))).
fof(p6, axiom, at_marys_school(hannah)).
fof(p7, axiom, (works_student_jobs(hannah) & (needs_money(hannah) => (~picky_eater(hannah) & ~needs_money(hannah))))).
fof(goal, conjecture, ~(at_marys_school(hannah) & ~picky_eater(hannah) & spends_time_dining(hannah))).