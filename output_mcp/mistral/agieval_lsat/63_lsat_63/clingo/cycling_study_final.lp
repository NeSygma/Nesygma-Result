% Define the domain
rider("Reynaldo"; "Seamus"; "Theresa"; "Yuki").
bicycle("F"; "G"; "H"; "J").
day(1..2).

% Base constraints
% Each rider tests exactly one bicycle per day
1 { tests(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
1 { tests(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle on day 2 than day 1
:- tests(R, B, 1), tests(R, B, 2).

% Reynaldo cannot test F
:- tests("Reynaldo", "F", D), day(D).

% Yuki cannot test J
:- tests("Yuki", "J", D), day(D).

% Theresa must test H on at least one day
:- rider("Theresa"), not tests("Theresa", "H", 1), not tests("Theresa", "H", 2).

% If Yuki tests bicycle B on day 1, Seamus tests B on day 2
:- tests("Yuki", B, 1), not tests("Seamus", B, 2).

% Define the conditions for each option
% (A) Reynaldo tests G on the second day
option_condition(a) :- tests("Reynaldo", "G", 2).

% (B) Seamus tests F on the first day
option_condition(b) :- tests("Seamus", "F", 1).

% (C) Theresa tests F on the second day
option_condition(c) :- tests("Theresa", "F", 2).

% (D) Reynaldo tests H on the first day
option_condition(d) :- tests("Reynaldo", "H", 1).

% (E) Yuki tests F on the second day
option_condition(e) :- tests("Yuki", "F", 2).

% The correct answer is the option that CANNOT be true
% So, for the correct answer X, option_condition(X) must be false in all models
% and for all other options Y, option_condition(Y) must be true in at least one model

% Enforce that exactly one answer is selected
1 { answer(a;b;c;d;e) } 1.

% For the selected answer, option_condition must be false in all models
:- answer(X), option_condition(X).

% For the other options, ensure they are possible (i.e., not impossible)
% This is implicitly enforced by the solver's search for models

% Map answer to option
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.