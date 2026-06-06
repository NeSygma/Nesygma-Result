% Domain declarations
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Base assignment facts (day 1 and day 2)
% assignment(R, B, D) means rider R tests bicycle B on day D.

% Constraints from the problem:
% 1. Reynaldo cannot test F.
:- assignment(reynaldo, f, _).

% 2. Yuki cannot test J.
:- assignment(yuki, j, _).

% 3. Theresa must be one of the testers for H.
% This is a must condition, so Theresa must test H on at least one day.
:- not assignment(theresa, h, 1), not assignment(theresa, h, 2).

% 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
:- assignment(yuki, B, 1), not assignment(seamus, B, 2).

% Each rider tests exactly one bicycle per day.
1 { assignment(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day.
1 { assignment(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Each rider tests a different bicycle on the second day.
:- assignment(R, B1, 1), assignment(R, B2, 2), B1 = B2.

% Given condition: Theresa tests J on the first day.
assignment(theresa, j, 1).

% Theresa must test H on the second day to satisfy the "must be one of the testers for H" constraint.
assignment(theresa, h, 2).

% --- Multiple Choice Options ---
% We need to check which of the following could be true under the given constraints.

% (A) Reynaldo tests G on the second day.
option(a) :- assignment(reynaldo, g, 2).

% (B) Seamus tests H on the first day.
option(b) :- assignment(seamus, h, 1).

% (C) Yuki tests H on the second day.
option(c) :- assignment(yuki, h, 2).

% (D) Seamus is one of the testers for J.
% This could mean either day 1 or day 2.
option(d) :- assignment(seamus, j, 1).
option(d) :- assignment(seamus, j, 2).

% (E) Theresa is one of the testers for G.
option(e) :- assignment(theresa, g, 1).
option(e) :- assignment(theresa, g, 2).

#show option/1.