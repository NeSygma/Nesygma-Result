fof(rule1, axiom, ! [X] : ((at_mary_school(X) & works_student_job(X)) => needs_money(X))).
fof(rule2, axiom, ! [X] : ((at_mary_school(X) & orders_takeout_frequently(X)) => works_student_job(X))).
fof(rule3, axiom, ! [X] : (at_mary_school(X) => (orders_takeout_frequently(X) | enjoys_dining_hall(X)))).
fof(rule4, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall(X)) => not_picky(X))).
fof(rule5, axiom, ! [X] : ((at_mary_school(X) & enjoys_dining_hall(X)) => spends_time_eating(X))).
fof(fact1, axiom, at_mary_school(hannah)).
fof(fact2, axiom, works_student_job(hannah)).
fof(fact3, axiom, (needs_money(hannah) => (not_picky(hannah) & ~needs_money(hannah)))).
fof(goal, conjecture, (at_mary_school(hannah) & not_picky(hannah) & spends_time_eating(hannah))).