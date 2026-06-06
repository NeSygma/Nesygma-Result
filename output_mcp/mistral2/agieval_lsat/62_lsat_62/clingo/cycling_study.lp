% Domain declarations
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Assignments for each day
% assignment(R, B, D) means rider R tests bicycle B on day D
1 { assignment(R, B, D) : bicycle(B) } 1 :- rider(R), day(D).

% Each bicycle is tested by exactly one rider per day
1 { assignment(R, B, D) : rider(R) } 1 :- bicycle(B), day(D).

% Constraints from the problem
% Reynaldo cannot test F
:- assignment(reynaldo, f, D), day(D).

% Yuki cannot test J
:- assignment(yuki, j, D), day(D).

% Theresa must test H
:- not assignment(theresa, h, D), day(D).

% The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
:- assignment(yuki, B, 1), not assignment(seamus, B, 2), bicycle(B).

% Ensure all riders test a different bicycle on the second day compared to the first day
:- assignment(R, B, 1), assignment(R, B, 2), rider(R), bicycle(B).

% --- Multiple Choice Evaluation ---
% Define conditions for each option

% Option A: Reynaldo tests J on the first day
option(a) :- assignment(reynaldo, j, 1).

% Option B: Reynaldo tests J on the second day
option(b) :- assignment(reynaldo, j, 2).

% Option C: Seamus tests H on the first day
option(c) :- assignment(seamus, h, 1).

% Option D: Yuki tests H on the first day
option(d) :- assignment(yuki, h, 1).

% Option E: Yuki tests H on the second day
option(e) :- assignment(yuki, h, 2).

#show option/1.