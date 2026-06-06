% Positive version
fof(premise1, axiom, ! [X] : ( (at_school(X) & work_student_job(X)) => need_money(X) )).
fof(premise2, axiom, ! [X] : ( (at_school(X) & order_takeout(X)) => work_student_job(X) )).
fof(premise3, axiom, ! [X] : ( at_school(X) => (order_takeout(X) | enjoy_dining_hall(X)) )).
fof(premise4, axiom, ! [X] : ( (at_school(X) & enjoy_dining_hall(X)) => not_picky(X) )).
fof(premise5, axiom, ! [X] : ( (at_school(X) & enjoy_dining_hall(X)) => spend_time(X) )).
fof(premise6, axiom, at_school(hannah)).
fof(premise7a, axiom, work_student_job(hannah)).
fof(premise7b, axiom, need_money(hannah) => (not_picky(hannah) & ~need_money(hannah))).
fof(conclusion, conjecture, at_school(hannah) & ( not_picky(hannah) | (~not_picky(hannah) => spend_time(hannah)) )).