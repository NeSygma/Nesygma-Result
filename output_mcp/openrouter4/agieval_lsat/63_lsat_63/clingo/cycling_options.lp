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

% Check each option by forcing it to be true
% Option A: Reynaldo tests G on second day
:- test(reynaldo, g, 2), not possible_a.
possible_a :- test(reynaldo, g, 2).

% Option B: Seamus tests F on first day
:- test(seamus, f, 1), not possible_b.
possible_b :- test(seamus, f, 1).

% Option C: Theresa tests F on second day
:- test(theresa, f, 2), not possible_c.
possible_c :- test(theresa, f, 2).

% Option D: Reynaldo tests H on first day
:- test(reynaldo, h, 1), not possible_d.
possible_d :- test(reynaldo, h, 1).

% Option E: Yuki tests F on second day
:- test(yuki, f, 2), not possible_e.
possible_e :- test(yuki, f, 2).

#show possible_a/0.
#show possible_b/0.
#show possible_c/0.
#show possible_d/0.
#show possible_e/0.