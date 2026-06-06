% Domain
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Each rider tests exactly one bicycle per day
1 { assign(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
1 { assign(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Constraints
% Reynaldo cannot test F
:- assign(reynaldo, f, D), day(D).

% Yuki cannot test J
:- assign(yuki, j, D), day(D).

% Theresa must be one of the testers for H (at least one day)
1 { assign(theresa, h, D) : day(D) } 1.

% The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
:- assign(yuki, B, 1), not assign(seamus, B, 2).

% Each rider tests a different bicycle on the second day than on the first day
:- assign(R, B, 1), assign(R, B, 2), rider(R), bicycle(B).

% Now evaluate each option

% (A) Reynaldo tests G on the second day
option(a) :- not possible_a.
possible_a :- assign(reynaldo, g, 2).

% (B) Seamus tests F on the first day
option(b) :- not possible_b.
possible_b :- assign(seamus, f, 1).

% (C) Theresa tests F on the second day
option(c) :- not possible_c.
possible_c :- assign(theresa, f, 2).

% (D) Reynaldo tests H on the first day
option(d) :- not possible_d.
possible_d :- assign(reynaldo, h, 1).

% (E) Yuki tests F on the second day
option(e) :- not possible_e.
possible_e :- assign(yuki, f, 2).

#show option/1.