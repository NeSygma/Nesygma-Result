fof(p1, axiom, ! [X] : (works_student_job(X) => needs_earn_money(X))).
fof(p2, axiom, ! [X] : (orders_takeout(X) => works_student_job(X))).
fof(p3, axiom, ! [X] : (orders_takeout(X) | enjoys_dining(X))).
fof(p4, axiom, ! [X] : (enjoys_dining(X) => ~picky_eater(X))).
fof(p5, axiom, ! [X] : (enjoys_dining(X) => time_eating_friends(X))).
fof(p6, axiom, at_marys_school(hannah)).
fof(p7, axiom, (works_student_job(hannah) & (needs_earn_money(hannah) => (~picky_eater(hannah) & ~needs_earn_money(hannah))))).
fof(goal, conjecture, (at_marys_school(hannah) & ~picky_eater(hannah) & time_eating_friends(hannah))).