fof(p1, axiom, ! [X] : ((at_marys_school(X) & works_on_campus(X)) => needs_money(X))).
fof(p2, axiom, ! [X] : ((at_marys_school(X) & orders_takeout(X)) => works_on_campus(X))).
fof(p3, axiom, ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining_hall(X)))).
fof(p4, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => ~picky(X))).
fof(p5, axiom, ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => spends_time_in_dining_hall(X))).
fof(p6, axiom, at_marys_school(hannah)).
fof(p7, axiom, works_on_campus(hannah)).
fof(p8, axiom, (needs_money(hannah) => (~picky(hannah) & ~needs_money(hannah)))).
fof(p9, axiom, ~needs_money(hannah)).
fof(goal, conjecture, (at_marys_school(hannah) & ~picky(hannah) & spends_time_in_dining_hall(hannah))).