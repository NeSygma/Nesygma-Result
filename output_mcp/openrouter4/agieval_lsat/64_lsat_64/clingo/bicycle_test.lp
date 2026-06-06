% Domains
rider(reynaldo; seamus; theresa; yuki).
bike(f; g; h; j).
day(1; 2).

% Assignment: each rider on each day tests exactly one bike
1 { assigned(R, D, B) : bike(B) } 1 :- rider(R), day(D).

% Each bike on each day is tested by exactly one rider
1 { assigned(R, D, B) : rider(R) } 1 :- bike(B), day(D).

% Constraint: Reynaldo cannot test F
:- assigned(reynaldo, D, f), day(D).

% Constraint: Yuki cannot test J
:- assigned(yuki, D, j), day(D).

% Constraint: Theresa must be one of the testers for H (at least one day)
:- not 1 { assigned(theresa, D, h) : day(D) } 1.

% Constraint: Yuki's day1 bike is tested by Seamus on day2
:- assigned(yuki, 1, B), not assigned(seamus, 2, B).

% Condition for the question: Theresa tests J on day 1
assigned(theresa, 1, j).

% Choose exactly one option to explore
1 { explore_option(a); explore_option(b); explore_option(c); explore_option(d); explore_option(e) } 1.

% For each option, if we are exploring it, the option conditions must hold
option_holds :- explore_option(a), assigned(reynaldo, 2, g).
option_holds :- explore_option(b), assigned(seamus, 1, h).
option_holds :- explore_option(c), assigned(yuki, 2, h).
option_holds :- explore_option(d), 1 { assigned(seamus, D, j) : day(D) } 1.
option_holds :- explore_option(e), 1 { assigned(theresa, D, g) : day(D) } 1.

% The explored option must hold
:- explore_option(X), not option_holds.

% Derive the answer
option(a) :- explore_option(a).
option(b) :- explore_option(b).
option(c) :- explore_option(c).
option(d) :- explore_option(d).
option(e) :- explore_option(e).

#show option/1.