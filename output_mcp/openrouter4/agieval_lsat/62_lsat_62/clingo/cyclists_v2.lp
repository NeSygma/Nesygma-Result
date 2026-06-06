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

% --- Option Conditions ---

% Option A: Reynaldo tests J on the first day
optA_holds :- assign(reynaldo, j, 1).

% Option B: Reynaldo tests J on the second day
optB_holds :- assign(reynaldo, j, 2).

% Option C: Seamus tests H on the first day
optC_holds :- assign(seamus, h, 1).

% Option D: Yuki tests H on the first day
optD_holds :- assign(yuki, h, 1).

% Option E: Yuki tests H on the second day
optE_holds :- assign(yuki, h, 2).

% Show all option conditions to see which appear in valid assignments
#show optA_holds/0.
#show optB_holds/0.
#show optC_holds/0.
#show optD_holds/0.
#show optE_holds/0.
#show assign/3.