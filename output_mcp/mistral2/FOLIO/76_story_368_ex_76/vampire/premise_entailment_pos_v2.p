fof(premise1, axiom, ! [X] : (works_in_student_jobs(X) => needs_to_arn_money(X))).
fof(premise2, axiom, ! [X] : (orders_takeout_frequently(X) => works_in_student_jobs(X))).
fof(premise3, axiom, ! [X] : (orders_takeout_frequently(X) | enjoys_dining_hall(X))).
fof(premise4, axiom, ! [X] : (enjoys_dining_hall(X) => ~is_picky_eater(X))).
fof(premise5, axiom, ! [X] : (enjoys_dining_hall(X) => spends_time_in_dining_hall(X))).
fof(premise6, axiom, at_marys_school(hannah)).
fof(premise7, axiom, works_in_student_jobs(hannah)).
fof(premise8, axiom, (needs_to_arn_money(hannah) => (~is_picky_eater(hannah) & ~needs_to_arn_money(hannah)))).

fof(goal, conjecture, needs_to_arn_money(hannah)).