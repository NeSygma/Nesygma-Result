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
% This is not possible because Reynaldo cannot test F, and the only remaining bicycle for Reynaldo on day 2 would be G, but this would require Theresa to not test H on day 2, which violates the constraint.
% So, we do not derive option(a).

% (B) Seamus tests H on the first day.
% This is possible. If Seamus tests H on day 1, then:
% Day 1: Seamus tests H, Theresa tests J, Reynaldo tests G, Yuki tests F.
% Day 2: Seamus tests F (since Yuki tests F on day 1), Theresa tests H, Reynaldo tests J, Yuki tests G.
% This satisfies all constraints.
option(b) :- assignment(seamus, h, 1).

% (C) Yuki tests H on the second day.
% Not possible because Theresa already tests H on day 2.

% (D) Seamus is one of the testers for J.
% Not possible because Theresa tests J on day 1, and no other rider can test J on day 2 (since all bicycles must be tested each day, and J is already tested by Theresa on day 1).

% (E) Theresa is one of the testers for G.
% Not possible because Theresa tests J on day 1 and H on day 2, leaving no room for G.

#show option/1.