% --- Premises ---
person(hannah).
at_marys(hannah).

% P1: If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
need_money(P) :- at_marys(P), work_campus(P).

% P2: If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
work_campus(P) :- at_marys(P), order_takeout(P).

% P3: People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
{ order_takeout(P); enjoy_dining(P) } :- at_marys(P).
:- at_marys(P), not order_takeout(P), not enjoy_dining(P).

% P4: If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
not_picky(P) :- at_marys(P), enjoy_dining(P).
picky(P) :- at_marys(P), not not_picky(P).

% P5: If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
spend_time_dining(P) :- at_marys(P), enjoy_dining(P).

% P6: Hannah is at Mary's school.
% P7: Hannah works in student jobs on campus.
work_campus(hannah).

% P8: Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.
% This is a rule: need_money(hannah) -> (not_picky(hannah) AND not need_money(hannah)).
% This rule is equivalent to: not need_money(hannah).
% But P1 and P7 imply need_money(hannah).
% Let's re-read P8 again. Maybe it's not a rule, but a description of Hannah?
% "Hannah works in student jobs on campus and if she needs to earn money..., then she is neither picky nor needs to earn money..."
% If I treat this as a constraint, it makes the problem unsatisfiable.
% Let's assume the premises are consistent and P8 is a rule that must hold.
% If it's a rule, then need_money(hannah) must be false.
% But P1 and P7 say it's true.
% Maybe P1 is not a rule for Hannah? No, that's not right.
% Let's assume P8 is a rule that overrides P1 for Hannah.
% Or maybe P1 is not "for all people".
% Let's just model the rules and see what happens.

% Conclusion: Hannah is at Mary's school and she either is not a picky eater or, if she is, then she spends a lot of her time eating and catching up with friends in the campus dining halls.
% Conclusion: at_marys(hannah) AND (not_picky(hannah) OR (picky(hannah) -> spend_time_dining(hannah))).

conclusion_true :- at_marys(hannah), (not_picky(hannah) ; (picky(hannah) -> spend_time_dining(hannah))).

% To check if it's false, we need to see if there's a model where the conclusion is false.
% The conclusion is false if: at_marys(hannah) is false OR (not_picky(hannah) is false AND (picky(hannah) -> spend_time_dining(hannah)) is false).
% (picky(hannah) -> spend_time_dining(hannah)) is false if picky(hannah) is true AND spend_time_dining(hannah) is false.
% So conclusion_false :- at_marys(hannah), picky(hannah), not spend_time_dining(hannah).

% Wait, the conclusion is: at_marys(hannah) AND (not_picky(hannah) OR (picky(hannah) -> spend_time_dining(hannah))).
% This is equivalent to: at_marys(hannah) AND (not_picky(hannah) OR (not picky(hannah) OR spend_time_dining(hannah))).
% Which is: at_marys(hannah) AND (not_picky(hannah) OR spend_time_dining(hannah)).

conclusion_true :- at_marys(hannah), (not_picky(hannah) ; spend_time_dining(hannah)).
conclusion_false :- at_marys(hannah), picky(hannah), not spend_time_dining(hannah).

% Let's add the constraint from P8.
:- work_campus(hannah), need_money(hannah), not (not_picky(hannah), not need_money(hannah)).

answer(true) :- conclusion_true, not conclusion_false.
answer(false) :- conclusion_false, not conclusion_true.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.