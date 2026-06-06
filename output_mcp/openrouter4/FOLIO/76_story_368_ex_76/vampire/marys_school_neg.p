% Negative test: negated conclusion as conjecture
% Negated conclusion: Hannah does NOT need to earn money

fof(premise_1, axiom,
    ! [X] : ((at_marys_school(X) & works_student_job(X)) => needs_money(X))).

fof(premise_2, axiom,
    ! [X] : ((at_marys_school(X) & orders_takeout(X)) => works_student_job(X))).

fof(premise_3, axiom,
    ! [X] : (at_marys_school(X) => (orders_takeout(X) | enjoys_dining_hall(X)))).

fof(premise_4, axiom,
    ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => ~picky_eater(X))).

fof(premise_5, axiom,
    ! [X] : ((at_marys_school(X) & enjoys_dining_hall(X)) => spends_time_dining_hall(X))).

fof(premise_6, axiom,
    at_marys_school(hannah)).

fof(premise_7, axiom,
    (works_student_job(hannah) & (needs_money(hannah) => (~picky_eater(hannah) & ~needs_money(hannah))))).

fof(conclusion_negated, conjecture,
    ~needs_money(hannah)).