% Domain declarations
rider(reynaldo; seamus; theresa; yuki).
bicycle(f; g; h; j).
day(1; 2).

% Assignments: assigned(R, B, D) means rider R tests bicycle B on day D
{ assigned(R, B, D) : rider(R), bicycle(B) } 1 :- day(D).

% Each bicycle is tested by exactly one rider per day
:- day(D), bicycle(B), not 1 { assigned(R, B, D) : rider(R) } 1.

% Each rider tests exactly one bicycle per day
:- day(D), rider(R), not 1 { assigned(R, B, D) : bicycle(B) } 1.

% Constraints from the problem statement
% Reynaldo cannot test F on the first day
:- assigned(reynaldo, f, 1).

% Yuki cannot test J on the first day
:- assigned(yuki, j, 1).

% Theresa must test H on at least one day (either day 1 or day 2)
:- day(D), not assigned(theresa, h, D).

% The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
:- assigned(yuki, B, 1), not assigned(seamus, B, 2).

% Ensure each rider tests a different bicycle on the second day than on the first day
:- rider(R), bicycle(B), assigned(R, B, 1), assigned(R, B, 2).

% --- Check each option ---
% Option A: Reynaldo tests G on the second day
option(a) :- assigned(reynaldo, g, 2), not option(b), not option(c), not option(d), not option(e).

% Option B: Seamus tests F on the first day
option(b) :- assigned(seamus, f, 1), not option(a), not option(c), not option(d), not option(e).

% Option C: Theresa tests F on the second day
option(c) :- assigned(theresa, f, 2), not option(a), not option(b), not option(d), not option(e).

% Option D: Reynaldo tests H on the first day
option(d) :- assigned(reynaldo, h, 1), not option(a), not option(b), not option(c), not option(e).

% Option E: Yuki tests F on the second day
option(e) :- assigned(yuki, f, 2), not option(a), not option(b), not option(c), not option(d).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

% Show the selected option
#show option/1.