% Domain facts
rider(reyaldo). rider(seamus). rider(theresa). rider(yuki).
bike(f). bike(g). bike(h). bike(j).
day(1). day(2).

% Assignment choice: each rider gets exactly one bike per day
{ assign(R,B,D) : bike(B) } 1 :- rider(R), day(D).
% Each bike gets exactly one rider per day
{ assign(R,B,D) : rider(R) } 1 :- bike(B), day(D).

% Constraints
% Reynaldo cannot test F
:- assign(reyaldo, f, D).
% Yuki cannot test J
:- assign(yuki, j, D).
% Theresa must test H on at least one day
:- not assign(theresa, h, 1), not assign(theresa, h, 2).
% Yuki's day1 bike must be tested by Seamus on day2
:- assign(yuki, B, 1), not assign(seamus, B, 2).
% Theresa tests G on day2 (given condition)
:- not assign(theresa, g, 2).

% Option rules
option(a) :- assign(reyaldo, h, 1).
option(b) :- assign(reyaldo, j, 1).
option(c) :- assign(theresa, h, 2).
option(d) :- assign(theresa, j, 1).
option(e) :- assign(yuki, h, 2).

% At most one option
:- option(a), option(b).
:- option(a), option(c).
:- option(a), option(d).
:- option(a), option(e).
:- option(b), option(c).
:- option(b), option(d).
:- option(b), option(e).
:- option(c), option(d).
:- option(c), option(e).
:- option(d), option(e).

% At least one option
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.