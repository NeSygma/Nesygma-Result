fof(premise1, axiom, ! [X] : (works_student_job(X) => needs_money(X))).
fof(premise2, axiom, ! [X] : (orders_takeout(X) => works_student_job(X))).
fof(premise3, axiom, ! [X] : (orders_takeout(X) | enjoys_dining(X))).
fof(premise4, axiom, ! [X] : (enjoys_dining(X) => ~picky_eater(X))).
fof(premise5, axiom, ! [X] : (enjoys_dining(X) => spends_time_dining(X))).
fof(premise6, axiom, at_marys_school(hannah)).
fof(premise7, axiom, (works_student_job(hannah) & (needs_money(hannah) => (~picky_eater(hannah) & ~needs_money(hannah))))).
fof(goal, conjecture, at_marys_school(hannah) & (~picky_eater(hannah) | (picky_eater(hannah) => spends_time_dining(hannah)))).