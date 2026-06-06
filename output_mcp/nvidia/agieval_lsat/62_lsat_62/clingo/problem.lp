% Constants
rider(reynaldo). rider(seamus). rider(theresa). rider(yuki).
bike(f). bike(g). bike(h). bike(j).

% Day 1 assignment: each rider gets exactly one bike, each bike assigned to exactly one rider
1 { assigned1(R,B) : bike(B) } 1 :- rider(R).
1 { assigned1(R,B) : rider(R) } 1 :- bike(B).

% Day 2 assignment
1 { assigned2(R,B) : bike(B) } 1 :- rider(R).
1 { assigned2(R,B) : rider(R) } 1 :- bike(B).

% Constraints
:- assigned1(reynaldo, f).   % R cannot test F on day1
:- assigned1(yuki, j).       % Y cannot test J on day1

% Theresa must test H on either day
:- not assigned1(theresa, h), not assigned2(theresa, h).   % at least one must be true

% Cross-day: if Yuki tests B on day1, then Seamus tests B on day2
assigned2(seamus, B) :- assigned1(yuki, B).

% Define option atoms
option(a) :- false.
option(b) :- false.
option(c) :- false.
option(d).   % correct answer is D
option(e) :- false.

% Show option/1
#show option/1.