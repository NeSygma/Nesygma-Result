% Negative version
fof(rule1, axiom, ! [X] : ((at_school(X) & work_job(X)) => need_money(X))).
fof(rule2, axiom, ! [X] : ((at_school(X) & order_takeout(X)) => work_job(X))).
fof(rule3, axiom, ! [X] : (at_school(X) => (order_takeout(X) | enjoy_dining_hall(X)))).
fof(rule4, axiom, ! [X] : ((at_school(X) & enjoy_dining_hall(X)) => not_picky(X))).
fof(rule5, axiom, ! [X] : ((at_school(X) & enjoy_dining_hall(X)) => spend_time_eating(X))).
fof(hannah_at, axiom, at_school(hannah)).
fof(hannah_work, axiom, work_job(hannah)).
fof(hannah_special, axiom, (need_money(hannah) => (not_picky(hannah) & ~need_money(hannah)))).
fof(goal_neg, conjecture, ~ (at_school(hannah) & not_picky(hannah) & spend_time_eating(hannah))).