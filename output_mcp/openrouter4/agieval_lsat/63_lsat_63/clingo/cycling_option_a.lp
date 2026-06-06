% Riders
rider(reynaldo; seamus; theresa; yuki).

% Bicycles
bike(f; g; h; j).

% Days
day(1; 2).

% Each rider tests exactly one bike per day
1 { test(R, B, D) : bike(B) } 1 :- rider(R), day(D).

% Each bike is tested by exactly one rider per day
1 { test(R, B, D) : rider(R) } 1 :- bike(B), day(D).

% Each rider tests different bicycles on the two days
:- rider(R), bike(B), test(R, B, 1), test(R, B, 2).

% Condition 1: Reynaldo cannot test F
:- test(reynaldo, f, _).

% Condition 2: Yuki cannot test J
:- test(yuki, j, _).

% Condition 3: Theresa must be one of the testers for H (on at least one day)
:- not test(theresa, h, 1), not test(theresa, h, 2).

% Condition 4: The bicycle that Yuki tests on day 1 must be tested by Seamus on day 2
:- test(yuki, B, 1), not test(seamus, B, 2).

% Option A: Reynaldo tests G on second day - force it to be true and check if possible
:- not test(reynaldo, g, 2).

% Show all assignments
#show test/3.