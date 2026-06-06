% Riders
rider(reynaldo; seamus; theresa; yuki).

% Bicycles
bicycle(f; g; h; j).

% Days
day(1; 2).

% Each rider tests exactly 1 bicycle per day
1 { assignment(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly 1 rider per day
1 { assignment(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle each day
:- assignment(R, B1, 1), assignment(R, B2, 2), B1 = B2.

% Condition 1: Reynaldo cannot test F
:- assignment(reynaldo, f, D), day(D).

% Condition 2: Yuki cannot test J
:- assignment(yuki, j, D), day(D).

% Condition 3: Theresa must test H at least once
1 { assignment(theresa, h, D) : day(D) } 1.

% Condition 4: Yuki's day 1 bike is tested by Seamus on day 2
:- assignment(yuki, B, 1), not assignment(seamus, B, 2).

% --- Check each option ---
% An option is possible if there exists an assignment satisfying all base constraints
% and the specific condition of that option.

% We model possibility by: if the conjunction is satisfiable, the option is possible.
% We use a choice rule to enable checking.

% Option A: Both Reynaldo and Seamus test J
option_a_condition :- assignment(reynaldo, j, _), assignment(seamus, j, _).

% Option B: Both Reynaldo and Theresa test J
option_b_condition :- assignment(reynaldo, j, _), assignment(theresa, j, _).

% Option C: Both Reynaldo and Yuki test G
option_c_condition :- assignment(reynaldo, g, _), assignment(yuki, g, _).

% Option D: Both Seamus and Theresa test G
option_d_condition :- assignment(seamus, g, _), assignment(theresa, g, _).

% Option E: Both Theresa and Yuki test F
option_e_condition :- assignment(theresa, f, _), assignment(yuki, f, _).

% We want to know which option condition CANNOT be true.
% Since we need exactly one answer, we need to reason which condition is impossible.
% We'll derive "possible" for each option when its condition holds.
% Then the answer is the one that is not possible.

possible_option(a) :- option_a_condition.
possible_option(b) :- option_b_condition.
possible_option(c) :- option_c_condition.
possible_option(d) :- option_d_condition.
possible_option(e) :- option_e_condition.

% Force each option to be tested: we want to see which ones can be true
% in some model. By default, Clingo finds one model. We need to see
% which option atoms appear in models.

#show assignment/3.
#show possible_option/1.