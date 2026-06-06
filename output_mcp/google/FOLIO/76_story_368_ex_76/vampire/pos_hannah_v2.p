fof(p1, axiom, ! [X] : ((at_marys_school(X) & works_student_job(X)) => needs_money(X))).
fof(p2, axiom, ! [X] : ((at_marys_school(X) & orders_takeout(X)) => works_student_job(X))).
fof(p3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining_hall(X)))).
fof(p4, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => ~picky(X))).
fof(p5, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => spends_time_dining_hall(X))).
fof(p6, axiom, at_marys_school(hannah)).
fof(p7, axiom, works_student_job(hannah)).
fof(p8, axiom, (needs_money(hannah) => (~picky(hannah) & ~needs_money(hannah)))).
fof(goal, conjecture, needs_money(hannah)).