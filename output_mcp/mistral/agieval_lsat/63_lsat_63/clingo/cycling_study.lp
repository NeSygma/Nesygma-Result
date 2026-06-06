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

% Choose exactly one answer option
1 { answer(a;b;c;d;e) } 1.

% If answer is X, then option X cannot be true
:- answer(a), tests("Reynaldo", "G", 2).
:- answer(b), tests("Seamus", "F", 1).
:- answer(c), tests("Theresa", "F", 2).
:- answer(d), tests("Reynaldo", "H", 1).
:- answer(e), tests("Yuki", "F", 2).

% Map answer to option
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.