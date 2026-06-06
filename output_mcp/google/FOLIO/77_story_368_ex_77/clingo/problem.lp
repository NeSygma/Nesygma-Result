% --- Premises ---
person(hannah).
at_marys(hannah).

% P1: If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
need_money(P) :- at_marys(P), work_campus(P).

% P2: If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
work_campus(P) :- at_marys(P), order_takeout(P).

% P3: People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
{ order_takeout(P) ; enjoy_dining(P) } :- at_marys(P).
:- at_marys(P), not order_takeout(P), not enjoy_dining(P).

% P4: If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
not_picky(P) :- at_marys(P), enjoy_dining(P).
picky(P) :- at_marys(P), not not_picky(P).

% P5: If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
spend_time_dining(P) :- at_marys(P), enjoy_dining(P).

% P7: Hannah works in student jobs on campus.
work_campus(hannah).

% P8: Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.
% We model the implication: need_money(hannah) -> (not_picky(hannah), not need_money(hannah))
% This is equivalent to: not need_money(hannah)
% Let's see if this is consistent with P1.
% P1: work_campus(hannah) -> need_money(hannah)
% Since work_campus(hannah) is true, need_money(hannah) is true.
% So we have need_money(hannah) AND not need_money(hannah).
% This is a contradiction.

% Let's define the conclusion:
% Conclusion: Hannah is at Mary's school and she is not a picky eater and spends a lot of her time eating and catching up with friends in the campus dining halls.
conclusion_true :- at_marys(hannah), not_picky(hannah), spend_time_dining(hannah).

% To define conclusion_false, we need to show it's definitely false.
% The conclusion is false if:
% not at_marys(hannah) OR picky(hannah) OR not spend_time_dining(hannah).
conclusion_false :- at_marys(hannah), picky(hannah).
conclusion_false :- at_marys(hannah), not spend_time_dining(hannah).

% Since the premises are contradictory, we should handle this.
% But the prompt says "Based STRICTLY on the premises".
% If the premises are contradictory, any conclusion is technically true.
% However, in these problems, we usually assume the premises are consistent.
% Let's re-read P8 again. Is there any other interpretation?
% "Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition."
% Maybe the "if" is not a material implication?
% What if it's a counterfactual? No.
% What if "needs to earn money" is not the same as "needs to earn money to help pay for her college tuition"?
% "needs to earn money" vs "needs to earn money to help pay for her college tuition".
% They are the same.

% Let's try to see if the conclusion is true in all models.
% If the premises are contradictory, there are no models.
% Let's check if there are models.
% If I remove the contradiction, are there models where the conclusion is true?
% Let's remove the contradiction by making P8 a rule that only applies if it doesn't contradict P1.
% No, that's not right.

% Let's just run it and see if it's UNSAT.
:- need_money(hannah), not need_money(hannah). % This is always false.
% Wait, the contradiction is:
% need_money(hannah) (from P1)
% not need_money(hannah) (from P8)
% So the program is UNSAT.

% Let's re-read the prompt. "Based STRICTLY on the premises, is the conclusion True, False, or Uncertain?"
% If it's UNSAT, maybe I should say "Inconsistent"?
% But the options are True, False, Uncertain.
% Let's re-read P8 again.
% "Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition."
% Maybe the "if" is: "if she needs to earn money..., then she is neither picky nor [does she need to earn money...]"
% This is (need_money -> (not_picky AND not need_money)).
% This is (not need_money).
% Is it possible that P1 is not a universal rule? "If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition."
% Maybe it's not "all people"?
% "If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition."
% This is a universal rule.

% Let's try to model it as:
% { need_money(P) } :- at_marys(P), work_campus(P).
% This would make it consistent.
% But P1 says "If... then...". That's a rule.

% Let's try to see if the conclusion is true in all models if I relax P1.
% No, that's not right.

% Let's assume the conclusion is "Uncertain" because of the contradiction.
% Or maybe the conclusion is "False"?
% Let's try to see if the conclusion is true in any model.
% If I remove the contradiction, the conclusion is true in some models.
% Let's see.
#show conclusion_true/0.
#show conclusion_false/0.