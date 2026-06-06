% Domain definitions
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Generate assignments: each rider gets exactly one bicycle per day,
% and each bicycle is assigned to exactly one rider per day.
1 { assign(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).
1 { assign(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% No rider tests the same bicycle on both days.
:- assign(R, B, 1), assign(R, B, 2).

% Condition 1: Reynaldo cannot test F on any day.
:- assign(reynaldo, f, D).

% Condition 2: Yuki cannot test J on any day.
:- assign(yuki, j, D).

% Condition 3: Theresa must test H on at least one day.
assign(theresa, h, 1) | assign(theresa, h, 2).

% Condition 4: The bicycle Yuki tests on day 1 must be tested by Seamus on day 2.
assign(seamus, B, 2) :- assign(yuki, B, 1).

% Given condition: Theresa tests G on day 2.
assign(theresa, g, 2).

% Derive answer options based on the model(s).
option(a) :- assign(reynaldo, h, 1).
option(b) :- assign(reynaldo, j, 1).
option(c) :- assign(theresa, h, 2).
option(d) :- assign(theresa, j, 1).
option(e) :- assign(yuki, h, 2).

#show option/1.
#show assign/3.