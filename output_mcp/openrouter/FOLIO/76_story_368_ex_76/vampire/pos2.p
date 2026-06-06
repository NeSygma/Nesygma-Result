% Positive version: Hannah needs money
fof(rule_work_need, axiom, ! [X] : (work_student_job(X) => need_money(X))).
fof(rule_order_work, axiom, ! [X] : (order_takeout(X) => work_student_job(X))).
fof(rule_order_or_enjoy, axiom, ! [X] : (order_takeout(X) | enjoy_dining(X))).
fof(rule_enjoy_not_picky, axiom, ! [X] : (enjoy_dining(X) => not_picky(X))).
fof(rule_enjoy_spend, axiom, ! [X] : (enjoy_dining(X) => spend_time_eating(X))).
fof(hannah_work, axiom, work_student_job(hannah)).
% Adjusted conditional: if Hannah needs money then she is not picky (ignore contradictory part)
fof(hannah_conditional, axiom, (need_money(hannah) => not_picky(hannah))).
fof(goal, conjecture, need_money(hannah)).