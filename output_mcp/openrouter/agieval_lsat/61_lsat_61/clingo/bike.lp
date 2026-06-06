% Domain definitions
rider(reynaldo). rider(seamus). rider(theresa). rider(yuki).
bike(f). bike(g). bike(h). bike(j).

% Each rider tests exactly one bike each day
1 { test(R,B,1) : bike(B) } 1 :- rider(R).
1 { test(R,B,2) : bike(B) } 1 :- rider(R).

% Each bike is tested by exactly one rider each day
1 { test(R,B,1) : rider(R) } 1 :- bike(B).
1 { test(R,B,2) : rider(R) } 1 :- bike(B).

% No rider repeats same bike across days
:- test(R,B,1), test(R,B,2).

% Constraints
:- test(reynaldo, f, 1).
:- test(reynaldo, f, 2).
:- test(yuki, j, 1).
:- test(yuki, j, 2).
% Theresa must test H at least one day
:- not test(theresa, h, 1), not test(theresa, h, 2).
% Yuki's day1 bike must be Seamus's day2 bike
:- test(yuki, B, 1), not test(seamus, B, 2).

% Premise: Theresa tests G on day2
test(theresa, g, 2).

% Option conditions
condA :- test(reynaldo, h, 1).
condB :- test(reynaldo, j, 1).
condC :- test(theresa, h, 2).
condD :- test(theresa, j, 1).
condE :- test(yuki, h, 2).

% Select exactly one option
1 { selected(a); selected(b); selected(c); selected(d); selected(e) } 1.
% Enforce that selected option's condition holds
:- selected(a), not condA.
:- selected(b), not condB.
:- selected(c), not condC.
:- selected(d), not condD.
:- selected(e), not condE.

% Map to output
option(a) :- selected(a).
option(b) :- selected(b).
option(c) :- selected(c).
option(d) :- selected(d).
option(e) :- selected(e).

#show option/1.