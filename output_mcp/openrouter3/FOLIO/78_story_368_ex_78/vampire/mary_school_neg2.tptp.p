% Mary's School Problem - Negative Version 2
fof(distinct_constants, axiom, (hannah != school)).  % Ensure distinctness

% Premise 1: If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
fof(premise_1, axiom, ! [X] : (at_school(X, school) & works_student_job(X) => needs_money_tuition(X))).

% Premise 2: If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
fof(premise_2, axiom, ! [X] : (at_school(X, school) & orders_takeout(X) => works_student_job(X))).

% Premise 3: People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
fof(premise_3, axiom, ! [X] : (at_school(X, school) => (orders_takeout(X) | enjoys_dining_hall(X)))).

% Premise 4: If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
fof(premise_4, axiom, ! [X] : (at_school(X, school) & enjoys_dining_hall(X) => ~picky_eater(X))).

% Premise 5: If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
fof(premise_5, axiom, ! [X] : (at_school(X, school) & enjoys_dining_hall(X) => spends_time_dining(X))).

% Premise 6: Hannah is at Mary's school.
fof(premise_6, axiom, at_school(hannah, school)).

% Premise 7: Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.
% This creates a contradiction if needs_money_tuition(hannah) is true, so we deduce ~needs_money_tuition(hannah)
fof(premise_7a, axiom, works_student_job(hannah)).
fof(premise_7b, axiom, (needs_money_tuition(hannah) => (~picky_eater(hannah) & ~needs_money_tuition(hannah)))).

% From premise 7b, we can deduce that ~needs_money_tuition(hannah) must be true
fof(deduction_7, axiom, ~needs_money_tuition(hannah)).

% Negated Conclusion: Hannah is NOT at Mary's school OR she is a picky eater AND she does NOT spend a lot of her time eating and catching up with friends in the campus dining halls.
fof(goal, conjecture, (~at_school(hannah, school) | (picky_eater(hannah) & ~spends_time_dining(hannah)))).