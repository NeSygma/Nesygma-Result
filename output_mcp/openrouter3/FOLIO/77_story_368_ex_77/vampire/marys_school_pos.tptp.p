% Premises about Mary's school
fof(premise_1, axiom, ! [X] : (person(X) & works_student_jobs(X) => needs_money_tuition(X))).
fof(premise_2, axiom, ! [X] : (person(X) & orders_takeout(X) => works_student_jobs(X))).
fof(premise_3, axiom, ! [X] : (person(X) => (orders_takeout(X) | enjoys_dining_hall(X)))).
fof(premise_4, axiom, ! [X] : (person(X) & enjoys_dining_hall(X) => ~picky_eater(X))).
fof(premise_5, axiom, ! [X] : (person(X) & enjoys_dining_hall(X) => spends_time_dining(X))).
fof(premise_6, axiom, person(hannah)).
fof(premise_7, axiom, (works_student_jobs(hannah) & (needs_money_tuition(hannah) => (~picky_eater(hannah) & ~needs_money_tuition(hannah))))).

% Conclusion to evaluate
fof(goal, conjecture, (person(hannah) & ~picky_eater(hannah) & spends_time_dining(hannah))).