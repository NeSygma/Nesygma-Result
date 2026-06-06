% Riders
rider(reynaldo; seamus; theresa; yuki).

% Bicycles
bike(f; g; h; j).

% Days
day(1; 2).

% Assignment: each rider tests exactly one bike per day
{ assign(R, B, D) : bike(B) } 1 :- rider(R), day(D).

% Each bike is tested by exactly one rider per day
{ assign(R, B, D) : rider(R) } 1 :- bike(B), day(D).

% --- Constraints ---

% 1. Reynaldo cannot test F
:- assign(reynaldo, f, D), day(D).

% 2. Yuki cannot test J
:- assign(yuki, j, D), day(D).

% 3. Theresa must be one of the testers for H (at least one day)
theresa_tests_h :- assign(theresa, h, 1).
theresa_tests_h :- assign(theresa, h, 2).
:- not theresa_tests_h.

% 4. The bicycle that Yuki tests on the first day must be tested by Seamus on the second day.
:- assign(yuki, B, 1), not assign(seamus, B, 2).

% Option C: Seamus tests H on the first day
:- not assign(seamus, h, 1).

#show assign/3.