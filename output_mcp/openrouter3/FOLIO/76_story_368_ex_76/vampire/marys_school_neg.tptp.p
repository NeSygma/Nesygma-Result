% Mary's School Problem - Negative Version
% Premises
fof(premise_1, axiom, ! [X] : (person_at_school(X) & works_student_jobs(X) => needs_money_tuition(X))).
fof(premise_2, axiom, ! [X] : (person_at_school(X) & orders_takeout(X) => works_student_jobs(X))).
fof(premise_3, axiom, ! [X] : (person_at_school(X) => (orders_takeout(X) | enjoys_dining_hall(X)))).
fof(premise_4, axiom, ! [X] : (person_at_school(X) & enjoys_dining_hall(X) => ~picky_eater(X))).
fof(premise_5, axiom, ! [X] : (person_at_school(X) & enjoys_dining_hall(X) => spends_time_dining(X))).
fof(premise_6, axiom, person_at_school(hannah)).
fof(premise_7, axiom, (works_student_jobs(hannah) & (needs_money_tuition(hannah) => (~picky_eater(hannah) & ~needs_money_tuition(hannah))))).

% Distinctness
fof(distinct_hannah, axiom, hannah != marys_school).

% Negated conclusion
fof(goal_neg, conjecture, ~needs_money_tuition(hannah)).