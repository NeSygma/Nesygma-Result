% Riders and bicycles
rider(reynaldo).
rider(seamus).
rider(theresa).
rider(yuki).

bicycle(f).
bicycle(g).
bicycle(h).
bicycle(j).

% Days
day(1).
day(2).

% Each rider tests exactly one bicycle per day
1 { tests(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
1 { tests(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Constraints
% Reynaldo cannot test F
:- tests(reynaldo, f, D).

% Yuki cannot test J
:- tests(yuki, j, D).

% Theresa must test H (on at least one day)
:- rider(theresa), not tests(theresa, h, 1), not tests(theresa, h, 2).

% If Yuki tests B on day 1, then Seamus tests B on day 2
:- tests(yuki, B, 1), not tests(seamus, B, 2).

% Given condition: Theresa tests G on the second day
tests(theresa, g, 2).

% Each rider must test a different bicycle on day 2 than on day 1
:- tests(R, B, 1), tests(R, B, 2).

% Map answer choices to conditions
% (A) Reynaldo tests H on the first day
option(a) :- tests(reynaldo, h, 1).

% (B) Reynaldo tests J on the first day
option(b) :- tests(reynaldo, j, 1).

% (C) Theresa tests H on the second day
option(c) :- tests(theresa, h, 2).

% (D) Theresa tests J on the first day
option(d) :- tests(theresa, j, 1).

% (E) Yuki tests H on the second day
option(e) :- tests(yuki, h, 2).

#show option/1.