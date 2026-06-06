% Riders and bicycles
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Each rider tests exactly one bicycle per day
1 { tests(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
1 { tests(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Constraints
:- tests(reynaldo, f, D), day(D).  % Reynaldo cannot test F
:- tests(yuki, j, D), day(D).       % Yuki cannot test J
:- not tests(theresa, h, 1), not tests(theresa, h, 2).  % Theresa must test H on at least one day

% If Yuki tests B on day 1, Seamus must test B on day 2
:- tests(yuki, B, 1), bicycle(B), not tests(seamus, B, 2).

% Given condition: Theresa tests J on day 1
tests(theresa, j, 1).

% Each rider tests a different bicycle on day 2 than on day 1
:- tests(R, B, 1), tests(R, B, 2), rider(R), bicycle(B).

% Map options to conditions
% Option A: Reynaldo tests G on day 2
option(a) :- tests(reynaldo, g, 2).

% Option B: Seamus tests H on day 1
option(b) :- tests(seamus, h, 1).

% Option C: Yuki tests H on day 2
option(c) :- tests(yuki, h, 2).

% Option D: Seamus is one of the testers for J (on at least one day)
option(d) :- tests(seamus, j, 1).
option(d) :- tests(seamus, j, 2).

% Option E: Theresa is one of the testers for G (on at least one day)
option(e) :- tests(theresa, g, 1).
option(e) :- tests(theresa, g, 2).

#show option/1.